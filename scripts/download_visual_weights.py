#!/usr/bin/env python3
"""Download default YOLO weights into models/visual/."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="Ultralytics model name or path (default: yolo11n.pt)",
    )
    parser.add_argument(
        "--out-dir",
        default="models/visual",
        help="Destination directory",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "ultralytics is required. Install with: pip install -r requirements-ml.txt"
        ) from exc

    print(f"Downloading {args.model} ...")
    model = YOLO(args.model)
    # Ultralytics caches weights; copy/export path into models/visual
    src = Path(getattr(model, "ckpt_path", None) or args.model)
    dest = out_dir / Path(args.model).name
    if src.is_file() and src.resolve() != dest.resolve():
        dest.write_bytes(src.read_bytes())
        print(f"Wrote {dest}")
    else:
        # Trigger a predict so cache materializes, then locate
        model.predict(source=None, imgsz=32, verbose=False)
        cache = Path.home() / ".cache" / "ultralytics"  # may vary
        print(f"Model ready: {args.model}")
        print(f"Place/copy weights into {dest} if not already present.")
        if dest.is_file():
            print(f"Found {dest}")
        elif cache.exists():
            print(f"Check Ultralytics cache under {cache}")


if __name__ == "__main__":
    main()
