#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def export_plan(model_name: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = {
        "model": model_name,
        "exports": [
            {"format": "onnx", "path": f"{model_name}.onnx"},
            {"format": "tensorrt", "path": f"{model_name}.engine"},
        ],
        "target": "jetson_orin",
    }
    out = output_dir / f"{model_name}_export_plan.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--output-dir", default="/tmp/counterdrone_exports")
    args = parser.parse_args()

    out = export_plan(args.model, Path(args.output_dir))
    print(f"Export plan generated: {out}")


if __name__ == "__main__":
    main()
