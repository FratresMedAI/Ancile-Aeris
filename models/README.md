# Models

Weight files are **not** committed. Download them locally:

```bash
python scripts/download_visual_weights.py
```

Default layout:

```text
models/
  visual/
    yolo11n.pt          # Ultralytics YOLO11n (auto-downloaded)
  acoustic/             # Phase 2
  rf/                   # Phase 2
```

Set `CLEARSKY_SIM_MODE=false` and point `visual_node` at these weights to run real inference.
See `requirements-ml.txt` for Python deps.
