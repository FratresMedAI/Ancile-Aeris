# Ancile Aeris

## ✅ Basic Demo Now Working — Fusion + DARKSPACE + Safety Gates + Scout + Copilot

Run the full basic demo stack with:

```bash
ANCILE_LAUNCH_FILE=ancile_aeris_basic_demo.launch.py docker compose -f docker/docker-compose.yml up --build
```

**Ancile Aeris** is the definitive cognitive autonomous defensive shield platform — a unified, simulation-first ROS 2 system designed to dominate the counter-unmanned aircraft systems mission space.

**Property of Fratres X AI**

## Repository layout notes

- Payload selector file path: `config/payload_selector.yaml` (workspace root inside this repo folder).
- Some cognitive capabilities live under `src/ancile_aeris_cognitive/`, including:
  - `src/ancile_aeris_cognitive/scout_mothership/`
  - `src/ancile_aeris_cognitive/baby_interceptor/`

## Cross-platform Docker note (Windows bind mounts)

When `/opt/ancile_aeris_ws` is bind-mounted from Windows, Python entry scripts can pick up CRLF line endings and fail on Linux with `OSError: [Errno 8] Exec format error`. The Docker Compose command strips `\\r` from `src/**/*.py` before building, and the basic demo launch files run Python nodes under `python3` for additional hardening.

If you are fixing wrappers manually, the installed script names match the ROS executables, for example:

- `install/ancile_aeris_safety_gate/lib/ancile_aeris_safety_gate/ancile_aeris_safety_gate_node`
- `install/ancile_aeris_operator_copilot/lib/ancile_aeris_operator_copilot/ancile_aeris_operator_copilot_node`

## Mission

Ancile Aeris delivers layered, trustworthy, human-on-the-loop defense against drone threats in dense urban environments, mass gatherings, critical infrastructure, and remote terrain — while maintaining full dual-use capability for conservation and wildlife protection.

## Core Philosophy

- Max-Defensive Safety Gates (PID ≥ 0.999 + multi-modal evidence)
- Human-on-the-Loop (no autonomous kill-chain)
- DARKSPACE Immutable Audit (HMAC hash-chain on every event)
- Explainable AI (XAI) on every recommendation
- Layered Defensive Architecture (Ground Sensors → High-Altitude Scout → Deployable Kinetic Interceptors)
- Zero Trust + Adversarial Resilience

## 21-Capability Cognitive Architecture

Ancile Aeris integrates 21 advanced capabilities including neuromorphic perception, cognitive electronic warfare, agentic multi-agent C2, generative digital twin, causal XAI, adversarial defense, high-altitude scout mothership with deployable kinetic interceptors, and more. All capabilities are modular and fully integrated with DARKSPACE and safety gates.

## Quick Start

```bash
ANCILE_LAUNCH_FILE=ancile_aeris_basic_demo.launch.py docker compose -f docker/docker-compose.yml up --build
```

Native workspace launch:

```bash
source /opt/ros/kilted/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

## Documentation

- docs/COGNITIVE_ARCHITECTURE.md
- docs/LRBAA_BORAP_04_MAPPING.md
- SUBMISSION_CHECKLIST.md

## Ownership

Ancile Aeris is the exclusive property of Fratres X AI. All rights reserved.
