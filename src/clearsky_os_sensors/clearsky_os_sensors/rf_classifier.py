"""RF emitter cueing: spectral peak heuristic + optional ONNX CNN.

Operates on complex baseband IQ (real/imag interleaved lists) or synthetic IQ.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class RfResult:
    confidence: float
    center_freq_hz: float
    bandwidth_hz: float
    modulation_guess: str
    backend: str
    class_label: str
    features: dict[str, float]


def synthetic_iq(
    n_samples: int = 1024,
    sample_rate_hz: float = 20e6,
    center_offset_hz: float = 0.0,
    tick: int = 0,
    present: bool = True,
) -> list[complex]:
    """Deterministic OFDM-ish baseband burst for sim / offline eval."""
    out: list[complex] = []
    phase = 0.05 * tick
    for i in range(n_samples):
        t = i / sample_rate_hz
        noise = 0.08 * cmath.exp(1j * (11.0 * t + phase))
        if present:
            # Multi-tone OFDM-like carriers around DC
            sig = (
                0.4 * cmath.exp(1j * (2.0 * math.pi * (center_offset_hz + 1.0e6) * t))
                + 0.3 * cmath.exp(1j * (2.0 * math.pi * (center_offset_hz - 0.5e6) * t + phase))
                + 0.2 * cmath.exp(1j * (2.0 * math.pi * (center_offset_hz + 2.5e6) * t))
            )
        else:
            sig = 0j
        out.append(sig + noise)
    return out


def spectral_features(
    iq: Sequence[complex],
    sample_rate_hz: float = 20e6,
) -> dict[str, float]:
    n = len(iq)
    if n == 0:
        return {"peak_power": 0.0, "mean_power": 0.0, "peak_to_mean": 0.0, "occupied_bins": 0.0}
    # Naive DFT magnitude at a coarse grid (pure Python, CI-safe)
    n_bins = min(64, n)
    powers: list[float] = []
    for k in range(n_bins):
        acc = 0j
        for i, z in enumerate(iq):
            angle = -2.0 * math.pi * k * i / n
            acc += z * cmath.exp(1j * angle)
        powers.append(abs(acc) ** 2 / n)
    peak = max(powers) if powers else 0.0
    mean = sum(powers) / max(1, len(powers))
    thresh = mean * 3.0
    occupied = sum(1 for p in powers if p >= thresh)
    peak_bin = powers.index(peak) if powers else 0
    # Map bin → approximate offset Hz
    offset_hz = (peak_bin / n_bins - 0.5) * sample_rate_hz
    return {
        "peak_power": peak,
        "mean_power": mean,
        "peak_to_mean": peak / (mean + 1e-12),
        "occupied_bins": float(occupied),
        "peak_offset_hz": offset_hz,
        "sample_rate_hz": sample_rate_hz,
    }


def classify_spectral(
    iq: Sequence[complex],
    *,
    sample_rate_hz: float = 20e6,
    rf_center_hz: float = 2.437e9,
) -> RfResult:
    feats = spectral_features(iq, sample_rate_hz)
    peak = float(feats["peak_power"])
    mean = float(feats["mean_power"])
    occupied = float(feats["occupied_bins"])
    # Absolute power separates OFDM-like bursts from weak single-tone noise
    # synthetic present peak~140 / mean~2.6; absent peak~6.5 / mean~0.1
    power_term = min(1.0, peak / 40.0)
    mean_term = min(1.0, mean / 1.0)
    occ_term = min(1.0, occupied / 3.0)
    score = max(0.05, min(0.90, 0.06 + 0.50 * power_term + 0.25 * mean_term + 0.15 * occ_term))
    mod = "ofdm" if occupied >= 2 and peak >= 40.0 else "narrowband_or_noise"
    bw = min(sample_rate_hz * 0.8, max(1.0e6, occupied * (sample_rate_hz / 64.0)))
    return RfResult(
        confidence=score,
        center_freq_hz=rf_center_hz + float(feats.get("peak_offset_hz", 0.0)),
        bandwidth_hz=bw,
        modulation_guess=mod,
        backend="heuristic_spectral_peak",
        class_label="uas_control_link_candidate" if score >= 0.45 else "noise_or_weak",
        features={k: float(v) for k, v in feats.items()},
    )


def classify_onnx(
    iq: Sequence[complex],
    weights: Path,
    *,
    sample_rate_hz: float = 20e6,
    rf_center_hz: float = 2.437e9,
) -> RfResult | None:
    try:
        import numpy as np
        import onnxruntime as ort
    except ImportError:
        return None
    if not weights.is_file():
        return None
    try:
        sess = ort.InferenceSession(str(weights), providers=["CPUExecutionProvider"])
        arr = np.asarray([[z.real, z.imag] for z in iq], dtype=np.float32)
        # [1, 2, N]
        x = arr.T[np.newaxis, ...]
        inp = sess.get_inputs()[0]
        shape = list(inp.shape)
        if len(shape) == 3 and isinstance(shape[-1], int) and shape[-1] > 0:
            n = shape[-1]
            if x.shape[-1] < n:
                pad = np.zeros((1, x.shape[1], n - x.shape[-1]), dtype=np.float32)
                x = np.concatenate([x, pad], axis=-1)
            else:
                x = x[..., :n]
        out = sess.run(None, {inp.name: x})[0]
        conf = float(np.asarray(out).reshape(-1)[0])
        conf = max(0.0, min(1.0, conf))
        return RfResult(
            confidence=conf,
            center_freq_hz=rf_center_hz,
            bandwidth_hz=20.0e6,
            modulation_guess="ofdm",
            backend="onnx_rf_cnn",
            class_label="uas_control_link_candidate" if conf >= 0.45 else "noise_or_weak",
            features={"onnx_logit": conf, "sample_rate_hz": sample_rate_hz},
        )
    except Exception:
        return None


def classify_rf(
    iq: Sequence[complex] | None = None,
    *,
    sample_rate_hz: float = 20e6,
    rf_center_hz: float = 2.437e9,
    onnx_path: str | Path | None = None,
    tick: int = 0,
    force_heuristic: bool = False,
) -> RfResult:
    if iq is None:
        iq = synthetic_iq(tick=tick, present=True, sample_rate_hz=sample_rate_hz)
    if not force_heuristic and onnx_path:
        onnx_res = classify_onnx(
            iq, Path(onnx_path), sample_rate_hz=sample_rate_hz, rf_center_hz=rf_center_hz
        )
        if onnx_res is not None:
            return onnx_res
    return classify_spectral(iq, sample_rate_hz=sample_rate_hz, rf_center_hz=rf_center_hz)


def result_as_dict(result: RfResult) -> dict[str, Any]:
    return {
        "confidence": result.confidence,
        "center_freq_hz": result.center_freq_hz,
        "bandwidth_hz": result.bandwidth_hz,
        "modulation_guess": result.modulation_guess,
        "backend": result.backend,
        "class_label": result.class_label,
        "features": dict(result.features),
    }
