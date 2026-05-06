from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SensorWeights:
    visual: float = 0.24
    thermal: float = 0.24
    acoustic: float = 0.16
    rf: float = 0.18
    lidar: float = 0.18


class FusionNode:
    def __init__(self, weights: SensorWeights | None = None) -> None:
        self.weights = weights or SensorWeights()

    def fuse(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        signals = {
            "visual": float(sample.get("visual_score", 0.0)),
            "thermal": float(sample.get("thermal_score", 0.0)),
            "acoustic": float(sample.get("acoustic_score", 0.0)),
            "rf": float(sample.get("rf_score", 0.0)),
            "lidar": float(sample.get("lidar_score", 0.0)),
        }

        confidence = (
            signals["visual"] * self.weights.visual
            + signals["thermal"] * self.weights.thermal
            + signals["acoustic"] * self.weights.acoustic
            + signals["rf"] * self.weights.rf
            + signals["lidar"] * self.weights.lidar
        )
        confidence = max(0.0, min(1.0, confidence))

        dominant_signal = max(signals, key=signals.get)

        return {
            "target_id": sample.get("target_id", "unknown"),
            "fused_confidence": confidence,
            "signals": signals,
            "dominant_signal": dominant_signal,
        }
