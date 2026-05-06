from __future__ import annotations

from typing import Any, Dict


class DetectionNode:
    CLASSES = ["victim", "non_victim", "unknown"]

    def detect(self, fused: Dict[str, Any], frame_meta: Dict[str, Any]) -> Dict[str, Any]:
        conf = float(fused.get("fused_confidence", 0.0))
        thermal_peak = float(frame_meta.get("thermal_peak", 0.0))
        motion = float(frame_meta.get("motion_score", 0.0))

        victim_score = min(1.0, 0.55 * conf + 0.30 * thermal_peak + 0.15 * motion)

        if victim_score >= 0.7:
            label = "victim"
        elif victim_score >= 0.4:
            label = "unknown"
        else:
            label = "non_victim"

        return {
            "label": label,
            "victim_score": victim_score,
            "bbox": frame_meta.get("bbox", [0.1, 0.1, 0.2, 0.2]),
            "class_probs": {
                "victim": victim_score,
                "unknown": max(0.0, 1.0 - abs(victim_score - 0.5) * 2),
                "non_victim": 1.0 - victim_score,
            },
        }
