#!/usr/bin/env python3
"""Export ClearSky OS perception weights to ONNX (and optional TensorRT engine).

Examples:
  python scripts/model_export.py --weights models/visual/yolo11n.pt
  python scripts/model_export.py --weights models/visual/yolo11n.pt --format engine --device 0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def export_yolo(weights: Path, out_dir: Path, imgsz: int, fmt: str, device: str) -> Path:
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "ultralytics is required. Install with: pip install -r requirements-ml.txt"
        ) from exc

    if not weights.is_file():
        raise SystemExit(f"Weights not found: {weights}")

    out_dir.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(weights))
    exported = model.export(
        format=fmt,
        imgsz=imgsz,
        device=device if fmt == "engine" else "cpu",
        half=(fmt == "engine"),
    )
    exported_path = Path(str(exported))
    # Normalize into models/visual when possible
    target = out_dir / exported_path.name
    if exported_path.resolve() != target.resolve():
        target.write_bytes(exported_path.read_bytes())
        print(f"Copied export to {target}")
    else:
        print(f"Exported {target}")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ClearSky OS model export (ONNX / TensorRT)")
    parser.add_argument(
        "--weights",
        type=Path,
        default=Path("models/visual/yolo11n.pt"),
        help="Source Ultralytics .pt weights",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("models/visual"),
        help="Directory for exported artifacts",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Export image size")
    parser.add_argument(
        "--format",
        choices=("onnx", "engine"),
        default="onnx",
        help="onnx for portable ORT; engine for TensorRT on Jetson/CUDA hosts",
    )
    parser.add_argument(
        "--device",
        default="0",
        help="CUDA device id for TensorRT engine export (ignored for onnx)",
    )
    args = parser.parse_args(argv)

    path = export_yolo(args.weights, args.out_dir, args.imgsz, args.format, args.device)
    print(f"OK: {path}")
    if args.format == "onnx":
        print("Tip: set visual_node onnx_path / CLEARSKY_SIM_MODE=false to use ONNX Runtime CUDA on Jetson.")
    else:
        print("Tip: TensorRT .engine is device-specific; rebuild on the target Jetson.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
