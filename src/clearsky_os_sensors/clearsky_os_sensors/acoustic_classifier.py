"""Acoustic UAS cueing: mel-band energy heuristic + optional ONNX CRNN.

When no ONNX weights are present, uses a labeled band-energy heuristic on a
synthetic or provided waveform — not a fake high-confidence CRNN score.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class AcousticResult:
    confidence: float
    estimated_bearing_deg: float
    frequency_band_hz: list[float]
    backend: str
    class_label: str
    features: dict[str, float]


def _goertzel_power(samples: Sequence[float], sample_rate_hz: float, freq_hz: float) -> float:
    """Single-bin Goertzel power for a target frequency."""
    n = len(samples)
    if n == 0 or sample_rate_hz <= 0.0:
        return 0.0
    k = int(0.5 + (n * freq_hz) / sample_rate_hz)
    w = (2.0 * math.pi * k) / n
    cosine = math.cos(w)
    coeff = 2.0 * cosine
    s0 = s1 = s2 = 0.0
    for x in samples:
        s0 = float(x) + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return s1 * s1 + s2 * s2 - coeff * s1 * s2


def synthetic_rotor_waveform(
    n_samples: int = 2048,
    sample_rate_hz: float = 16000.0,
    tick: int = 0,
    present: bool = True,
) -> list[float]:
    """Deterministic synthetic mic-array frame for sim / offline eval."""
    out: list[float] = []
    # Slight bearing drift via phase offset across ticks
    phase0 = 0.15 * tick
    for i in range(n_samples):
        t = i / sample_rate_hz
        noise = 0.05 * math.sin(17.0 * t + phase0) + 0.03 * math.sin(41.0 * t)
        if present:
            # Broadband rotor-ish energy in 120–1800 Hz
            sig = (
                0.35 * math.sin(2.0 * math.pi * 180.0 * t + phase0)
                + 0.25 * math.sin(2.0 * math.pi * 420.0 * t)
                + 0.15 * math.sin(2.0 * math.pi * 900.0 * t)
                + 0.10 * math.sin(2.0 * math.pi * 1400.0 * t)
            )
        else:
            sig = 0.0
        out.append(sig + noise)
    return out


def band_energy_features(
    samples: Sequence[float],
    sample_rate_hz: float = 16000.0,
) -> dict[str, float]:
    bands = {
        "band_low_120_400": (120.0, 400.0),
        "band_mid_400_900": (400.0, 900.0),
        "band_high_900_1800": (900.0, 1800.0),
        "band_out_3000_5000": (3000.0, 5000.0),
    }
    feats: dict[str, float] = {}
    for name, (lo, hi) in bands.items():
        mid = 0.5 * (lo + hi)
        # Sample a few tones across the band
        powers = [
            _goertzel_power(samples, sample_rate_hz, f)
            for f in (lo, mid, hi)
        ]
        feats[name] = sum(powers) / max(1.0, float(len(powers)))
    total = sum(max(0.0, v) for v in feats.values()) + 1e-9
    feats["in_band_ratio"] = (
        feats["band_low_120_400"] + feats["band_mid_400_900"] + feats["band_high_900_1800"]
    ) / total
    rms = math.sqrt(sum(x * x for x in samples) / max(1, len(samples)))
    feats["rms"] = rms
    return feats


def classify_band_energy(
    samples: Sequence[float],
    sample_rate_hz: float = 16000.0,
    bearing_hint_deg: float = 35.0,
) -> AcousticResult:
    feats = band_energy_features(samples, sample_rate_hz)
    # Absolute in-band energy (not ratio-of-tiny-bins) separates signal from noise
    in_band = (
        float(feats["band_low_120_400"])
        + float(feats["band_mid_400_900"])
        + float(feats["band_high_900_1800"])
    )
    rms = float(feats["rms"])
    # Tuned on synthetic_rotor_waveform: present ~14k energy / 0.33 rms; absent ~0.05 / 0.04
    energy_term = min(1.0, in_band / 2000.0)
    rms_term = min(1.0, rms / 0.25)
    score = max(0.05, min(0.92, 0.08 + 0.55 * energy_term + 0.30 * rms_term))
    label = "uas_acoustic_candidate" if score >= 0.45 else "ambient_or_weak"
    feats["in_band_energy"] = in_band
    return AcousticResult(
        confidence=score,
        estimated_bearing_deg=bearing_hint_deg,
        frequency_band_hz=[120.0, 1800.0],
        backend="heuristic_band_energy",
        class_label=label,
        features={k: float(v) for k, v in feats.items()},
    )


def classify_onnx(
    samples: Sequence[float],
    weights: Path,
    sample_rate_hz: float = 16000.0,
    bearing_hint_deg: float = 35.0,
) -> AcousticResult | None:
    """Run ONNX CRNN if onnxruntime + weights are available."""
    try:
        import numpy as np
        import onnxruntime as ort
    except ImportError:
        return None
    if not weights.is_file():
        return None
    try:
        sess = ort.InferenceSession(str(weights), providers=["CPUExecutionProvider"])
        # Expect input [1, 1, n] or [1, n]; feed normalized waveform
        arr = np.asarray(list(samples), dtype=np.float32)
        arr = arr / (np.linalg.norm(arr) + 1e-6)
        inp = sess.get_inputs()[0]
        shape = list(inp.shape)
        if len(shape) == 3:
            x = arr.reshape(1, 1, -1)
        else:
            x = arr.reshape(1, -1)
        # Pad/truncate to declared length when static
        if isinstance(shape[-1], int) and shape[-1] > 0:
            n = shape[-1]
            if x.shape[-1] < n:
                pad = np.zeros((*x.shape[:-1], n - x.shape[-1]), dtype=np.float32)
                x = np.concatenate([x, pad], axis=-1)
            else:
                x = x[..., :n]
        out = sess.run(None, {inp.name: x})[0]
        conf = float(np.asarray(out).reshape(-1)[0])
        conf = max(0.0, min(1.0, conf))
        return AcousticResult(
            confidence=conf,
            estimated_bearing_deg=bearing_hint_deg,
            frequency_band_hz=[120.0, 1800.0],
            backend="onnx_crnn",
            class_label="uas_acoustic_candidate" if conf >= 0.45 else "ambient_or_weak",
            features={"onnx_logit": conf},
        )
    except Exception:
        return None


def classify_acoustic(
    samples: Sequence[float] | None = None,
    *,
    sample_rate_hz: float = 16000.0,
    bearing_hint_deg: float = 35.0,
    onnx_path: str | Path | None = None,
    tick: int = 0,
    force_heuristic: bool = False,
) -> AcousticResult:
    if samples is None:
        samples = synthetic_rotor_waveform(tick=tick, present=True)
    if not force_heuristic and onnx_path:
        onnx_res = classify_onnx(
            samples, Path(onnx_path), sample_rate_hz, bearing_hint_deg
        )
        if onnx_res is not None:
            return onnx_res
    return classify_band_energy(samples, sample_rate_hz, bearing_hint_deg)


def result_as_dict(result: AcousticResult) -> dict[str, Any]:
    return {
        "confidence": result.confidence,
        "estimated_bearing_deg": result.estimated_bearing_deg,
        "frequency_band_hz": list(result.frequency_band_hz),
        "backend": result.backend,
        "class_label": result.class_label,
        "features": dict(result.features),
    }
