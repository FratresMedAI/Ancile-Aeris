# Models

Weight files are **not** committed. Download / export them locally:

```bash
python scripts/download_visual_weights.py
python scripts/model_export.py --weights models/visual/yolo11n.pt --format onnx
# On Jetson / CUDA host (device-specific):
# python scripts/model_export.py --weights models/visual/yolo11n.pt --format engine
```

Default layout:

```text
models/
  visual/
    yolo11n.pt          # Ultralytics YOLO11n (auto-downloaded)
    yolo11n.onnx        # from model_export.py
  acoustic/
    crnn_melspec.onnx   # optional; band-energy heuristic used if absent
  rf/
    drone_rf_cnn.onnx   # optional; spectral heuristic used if absent
```

Set `CLEARSKY_SIM_MODE=false` and mount `models/` (Jetson compose does this) to run real / ONNX inference.
See `requirements-ml.txt` and `requirements-ml-jetson.txt`.
