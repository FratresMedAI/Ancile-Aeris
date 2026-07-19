"""Convert multimodal sensor JSON into EKF position measurements."""

from __future__ import annotations

import math
from typing import Any, Iterable

from clearsky_os_fusion.cv_ekf import Measurement


def _xy_from_range_bearing(range_m: float, bearing_deg: float) -> tuple[float, float]:
    rad = math.radians(float(bearing_deg))
    return float(range_m) * math.cos(rad), float(range_m) * math.sin(rad)


def adapt_position_tracks(
    tracks: Iterable[dict[str, Any]],
    *,
    confidence_scale: float = 1.0,
    image_scale_m: float = 200.0,
) -> list[Measurement]:
    out: list[Measurement] = []
    for trk in tracks:
        frame = str(trk.get("position_frame", "image_norm"))
        x = float(trk.get("x", 0.0))
        y = float(trk.get("y", 0.0))
        if frame != "map":
            # Legacy normalized/image coords → soft map meters for demos
            x *= float(image_scale_m)
            y *= float(image_scale_m)
        out.append(
            Measurement(
                x=x,
                y=y,
                confidence=float(trk.get("confidence", 0.0)) * confidence_scale,
                track_id=str(trk.get("track_id", "")),
                modality=str(trk.get("source", "position")),
            )
        )
    return out


def adapt_lidar(detections: Iterable[dict[str, Any]]) -> list[Measurement]:
    out: list[Measurement] = []
    for det in detections:
        rng = float(det.get("range_m", 0.0))
        brg = float(det.get("bearing_deg", 0.0))
        x, y = _xy_from_range_bearing(rng, brg)
        out.append(
            Measurement(
                x=x,
                y=y,
                confidence=float(det.get("confidence", 0.0)),
                track_id=str(det.get("id", "")),
                modality="lidar",
            )
        )
    return out


def adapt_bearing_only(
    detections: Iterable[dict[str, Any]],
    *,
    range_hint_m: float,
    modality: str,
    bearing_key: str = "estimated_bearing_deg",
    id_key: str = "detection_id",
    confidence_scale: float = 0.85,
) -> list[Measurement]:
    """Project bearing onto a range hint (EKF range or default)."""
    r = max(5.0, float(range_hint_m))
    out: list[Measurement] = []
    for det in detections:
        if bearing_key not in det and "bearing_deg" not in det:
            continue
        brg = float(det.get(bearing_key, det.get("bearing_deg", 0.0)))
        x, y = _xy_from_range_bearing(r, brg)
        out.append(
            Measurement(
                x=x,
                y=y,
                confidence=float(det.get("confidence", 0.0)) * confidence_scale,
                track_id=str(det.get(id_key, det.get("emitter_id", ""))),
                modality=modality,
            )
        )
    return out


def collect_all_measurements(
    *,
    visual_payload: dict[str, Any] | None,
    thermal_payload: dict[str, Any] | None,
    acoustic_payload: dict[str, Any] | None,
    rf_payload: dict[str, Any] | None,
    lidar_payload: dict[str, Any] | None,
    ekf_range_m: float,
    image_scale_m: float = 200.0,
) -> list[Measurement]:
    measurements: list[Measurement] = []
    if visual_payload and visual_payload.get("tracks"):
        measurements.extend(
            adapt_position_tracks(
                visual_payload["tracks"], image_scale_m=image_scale_m
            )
        )
    if thermal_payload and thermal_payload.get("tracks"):
        measurements.extend(
            adapt_position_tracks(
                thermal_payload["tracks"],
                confidence_scale=0.9,
                image_scale_m=image_scale_m,
            )
        )
    if lidar_payload and lidar_payload.get("detections"):
        measurements.extend(adapt_lidar(lidar_payload["detections"]))
    if acoustic_payload and acoustic_payload.get("detections"):
        measurements.extend(
            adapt_bearing_only(
                acoustic_payload["detections"],
                range_hint_m=ekf_range_m,
                modality="acoustic",
            )
        )
    if rf_payload and rf_payload.get("fingerprints"):
        measurements.extend(
            adapt_bearing_only(
                rf_payload["fingerprints"],
                range_hint_m=ekf_range_m,
                modality="rf",
                id_key="emitter_id",
                confidence_scale=0.8,
            )
        )
    return measurements
