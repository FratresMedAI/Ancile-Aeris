<p align="center">
  <img src="assets/clearsky-os-logo.png" alt="ClearSky OS" width="280" />
</p>

<h1 align="center">ClearSky OS</h1>

<p align="center">
  <strong>ROS 2 counter-UAS research stack from <a href="https://fratres-x.com">Fratres X AI</a></strong><br />
  Physics-first sensing, fusion, and autonomy scaffolding — reviewable, gated, and honest about maturity
</p>

<p align="center">
  <a href="https://github.com/Fratres-X-AI/ClearSky-OS/actions/workflows/ci.yml"><img src="https://github.com/Fratres-X-AI/ClearSky-OS/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License" /></a>
  <a href="https://docs.ros.org/en/kilted/"><img src="https://img.shields.io/badge/ROS%202-Kilted-22314E.svg" alt="ROS 2 Kilted" /></a>
  <a href="docker/"><img src="https://img.shields.io/badge/runtime-Docker-2496ED.svg" alt="Docker" /></a>
  <a href="https://fratres-x.com"><img src="https://img.shields.io/badge/Fratres%20X-fratres--x.com-0B1F2A.svg" alt="Fratres X" /></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#maturity">Maturity</a> ·
  <a href="docs/ARCHITECTURE.md">Docs</a> ·
  <a href="https://fratres-x.com">fratres-x.com</a>
</p>

---

**ClearSky OS** is the open ROS 2 workspace behind Fratres X AI’s counter-UAS research thread: multimodal sensing → fusion → safety gates → operator-facing decision support, with an immutable audit spine.

Built the Fratres X way — [physics first, conservative claims, systems built for scrutiny](https://fratres-x.com). No AI magic. No inflated readiness.

> **Safety:** No autonomous weapon release. Kinetic / last-resort simulation paths stay **policy-off by default**. Human-on-the-loop is required for mitigation recommendations.

## Why this repo

| Focus | What you get |
|--------|----------------|
| **Integration skeleton** | Docker-first ROS 2 Kilted workspace with CI on every push |
| **Reviewable control path** | Detect → track → fuse → gate → plan, with inspectable topics |
| **Safety-encoded posture** | Confidence gates, human veto, IFF lockout, kinetic defaults off |
| **Audit spine** | Hash-chained event trail for after-action replay |
| **Honest boundaries** | Stub vs production adapters called out in docs — replace, don’t pretend |

## Quick start

**Supported method: Docker only.**

```bash
CLEARSKY_LAUNCH_FILE=clearsky_os_basic_demo.launch.py \
  docker compose -f docker/docker-compose.yml up --build
```

Inside the container:

```bash
cd /opt/clearsky_os_ws
source /opt/ros/kilted/setup.bash
./clean-build.sh
ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py
```

Smoke-check:

```bash
ros2 topic list | grep -E '^/fused_tracks|^/audit/events|^/safety_gate_status|^/effector/'
```

See [`docs/TESTING.md`](docs/TESTING.md).

## Architecture

```mermaid
flowchart LR
  payloadSelector[payload_selector.yaml] --> bringup[clearsky_os_bringup]
  bringup --> sensors[sensors]
  bringup --> fusion[fusion]
  bringup --> safetyGate[safety_gate]
  bringup --> cognitive[cognitive]
  sensors --> fusion
  fusion --> fusedTracks[/fused_tracks/]
  fusedTracks --> cognitive
  safetyGate --> safetyStatus[/safety_gate_status/]
  safetyStatus --> cognitive
  cognitive --> audit[/audit/events/]
  cognitive --> xai[/xai_explanation/]
```

Default demo chain: sensors → fusion → audit → safety gate → scout / micro-payload sim → operator copilot → non-kinetic-first effector planning.

## Maturity

ClearSky OS is an **active research / prototype workspace**, not a fielded product.

| Layer today | Status |
|-------------|--------|
| Topic contracts, bringup, Docker, CI | Stable scaffolding |
| Safety / effector policy gates | Real software logic |
| Visual perception | **YOLO path** when `CLEARSKY_SIM_MODE=false` + weights; labeled synthetic tracks in sim mode |
| Fusion | **Constant-velocity EKF** with Mahalanobis association (`cv_ekf`) |
| Digital twin | **Analytic** point-mass risk → `/digital_twin/veto` |
| Acoustic / RF | Band-energy / spectral heuristics; optional ONNX when weights present |
| Thermal | Labeled synthetic stub |
| Scout mothership | Enrichment of fused tracks (coverage/mesh) — does not invent PID tracks |
| Effector envelopes | Analytic Friis / success probability on `/effector/status` + plan XAI |
| Effector / swarm inventory pubs | Simulation status publishers — not hardware actuation |

```bash
# Real vision (requires: pip install -r requirements-ml.txt && python scripts/download_visual_weights.py)
CLEARSKY_SIM_MODE=false CLEARSKY_VISUAL_SOURCE=/path/to/video.mp4 \
  docker compose -f docker/docker-compose.yml up --build

# Export YOLO → ONNX (Jetson: --format engine on the target)
python scripts/model_export.py --weights models/visual/yolo11n.pt

# Jetson profile (NVIDIA runtime + ML image)
docker compose -f docker/docker-compose.yml --profile jetson up --build

# Offline fusion / acoustic-RF metrics
python scripts/eval_fusion_offline.py
python scripts/eval_acoustic_rf_offline.py
```

If you need production sensing, fusion, or autonomy work, talk to us at [fratres-x.com](https://fratres-x.com).

## Repository map

```text
├── src/        # ROS 2 packages
├── docker/     # Supported runtime
├── config/     # Shared YAML
├── launch/     # Top-level launches
├── docs/       # Architecture + testing
├── k8s/        # Example edge manifests
├── scripts/    # Scenario / HIL helpers
└── assets/     # Branding
```

## Documentation

| Doc | Purpose |
|-----|---------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Module topology & data flow |
| [`docs/COGNITIVE_ARCHITECTURE.md`](docs/COGNITIVE_ARCHITECTURE.md) | Cognitive adjunct roadmap |
| [`docs/TESTING.md`](docs/TESTING.md) | Build, test, smoke validation |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Dev setup & PR expectations |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting |

## Contributing

PRs that harden physics adapters, fusion tests against production modules, and safety-gate regressions are especially welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Copyright © 2026 [Fratres X AI](https://fratres-x.com).

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE).
