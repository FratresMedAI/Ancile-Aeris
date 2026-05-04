#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def build_training_plan(dataset_manifest: Path, output_plan: Path) -> None:
    plan = {
        "visual": {
            "model": "yolo26s",
            "datasets": ["VisDrone", "Anti-UAV", str(dataset_manifest)],
            "epochs": 80,
        },
        "acoustic": {
            "model": "crnn_melspec",
            "datasets": ["DroneAudioDataset"],
            "epochs": 60,
        },
        "rf": {
            "model": "rf_cnn",
            "datasets": ["DroneRF"],
            "epochs": 50,
        },
        "trajectory": {
            "model": "transformer_small",
            "epochs": 40,
        },
    }
    output_plan.parent.mkdir(parents=True, exist_ok=True)
    with open(output_plan, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-manifest", required=True)
    parser.add_argument("--output-plan", default="/tmp/counterdrone_training_plan.json")
    args = parser.parse_args()

    build_training_plan(Path(args.dataset_manifest), Path(args.output_plan))
    print(f"Training plan generated: {args.output_plan}")


if __name__ == "__main__":
    main()
