# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for tagged releases.

## [Unreleased]

### Added

- Constant-velocity EKF fusion library + production tests (`clearsky_os_fusion.cv_ekf`)
- Analytic digital twin physics with `/digital_twin/veto` ownership
- YOLO visual inference path (`CLEARSKY_SIM_MODE=false`) with honest synthetic sim mode
- `requirements-ml.txt`, `scripts/download_visual_weights.py`, `scripts/eval_fusion_offline.py`
- Acoustic band-energy + RF spectral classifiers (optional ONNX); `scripts/eval_acoustic_rf_offline.py`
- Analytic effector envelopes (Friis / success probability) on `/effector/status` and plan XAI
- Real `scripts/model_export.py` (ONNX / TensorRT) and `docker/Dockerfile.jetson`
- Phase 3: `clearsky_os_sim` Gazebo-compatible truth bridge + SDF world
- Twin `gazebo_rollout` backend; multimodal fusion adapters; learned association shadow topic
- `scripts/eval_fusion_learned_offline.py`

### Removed

- LRBAA / BORAP / DHS solicitation materials, reviewer videos, and submission tooling
- Government-name-drop narrative from docs and payload READMEs

### Changed

- Scout mothership enriches fused tracks only; no longer invents PID-passing `/fused_tracks`
- Jetson compose profile builds ML image and mounts `models/`
- Fusion/twin launches load YAML params; fusion node name aligned with config

- README and docs repositioned for [Fratres X AI](https://fratres-x.com) — physics-first research stack, honest maturity
- Sensor stubs no longer publish fake 0.999 “model” confidence
- Demo context no longer owns twin veto by default
- Canonical site link: https://fratres-x.com
- Canonical repository: https://github.com/Fratres-X-AI/ClearSky-OS

## [2.1.0] - 2026-05

### Added

- Basic demo chain: sensors → fusion → audit → safety gate → scout / micro-payload sim → operator copilot → non-kinetic-first effectors

### Notes

- Kinetic `kamikaze_ram` remains policy-off by default

## [2.0.0] - 2026-05

### Added

- Docker-first ROS 2 Kilted workspace and CI build/test workflow

[Unreleased]: https://github.com/Fratres-X-AI/ClearSky-OS/compare/v2.0-lrbaa...HEAD
[2.1.0]: https://github.com/Fratres-X-AI/ClearSky-OS/releases/tag/v2.0-lrbaa
[2.0.0]: https://github.com/Fratres-X-AI/ClearSky-OS/releases/tag/v2.0-lrbaa
