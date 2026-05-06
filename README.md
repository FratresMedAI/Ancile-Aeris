# Ancile Aeris

**Property of Fratres X AI**

Ancile Aeris is a simulation-first ROS 2 cognitive defensive shield platform for **counter-UAS, anti-terrorism perimeter security, mass-gathering protection, and critical infrastructure defense**. It is built around defensive-only operations, DARKSPACE auditability, explainable recommendations, and human-on-the-loop safety gates.

## Basic Demo

The v2.0 basic demo is the authoritative LRBAA slice: sensors, fusion, DARKSPACE audit, safety gate, high-altitude scout mothership, and operator copilot.

Run the full basic demo stack with:

```bash
ANCILE_LAUNCH_FILE=ancile_aeris_basic_demo.launch.py docker compose -f docker/docker-compose.yml up --build
```

Native workspace launch:

```bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
colcon build --symlink-install --packages-up-to ancile_aeris_bringup
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

Enable the simulation-only baby interceptor path only when explicitly needed:

```bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py enable_baby_interceptor:=true
```

Expected live interfaces:

```bash
ros2 topic list | grep -E '^/fused_tracks|^/audit/events|^/scout_eyes|^/safety_gate_status'
ros2 service list | grep -E '/ancile_aeris_operator_copilot/query'
```

## Repository layout notes

- Payload selector file path: `src/ancile_aeris_bringup/config/payload_selector.yaml`.
- LRBAA core packages (`scout_mothership`, `baby_interceptor`) live at `src/scout_mothership/` and `src/baby_interceptor/` (`ament_cmake` + `install(PROGRAMS …)`). Mesh ISR topics publish under `/mesh/...`. Additional roadmap cognitive modules remain under `src/ancile_aeris_cognitive/`.
- LRBAA submission artifacts live under `submission/`.

## Cross-platform Docker note (Windows bind mounts)

When `/opt/ancile_aeris_ws` is bind-mounted from Windows, Python entry scripts can pick up CRLF line endings and fail on Linux with `OSError: [Errno 8] Exec format error`. The Docker Compose command strips `\\r` from `src/**/*.py` before building, and the basic demo launch files run Python nodes under `python3` for additional hardening.

If you are fixing wrappers manually, Python nodes (`scout_mothership_node`, `baby_interceptor_node`) install via CMake `install(PROGRAMS …)` under `install/<pkg>/lib/<pkg>/`. Launches prepend `python3` to survive Docker bind-mount CRLF quirks.

## Mission

Ancile Aeris delivers layered, trustworthy, human-on-the-loop defense against drone threats in dense urban environments, **mass gatherings**, **critical infrastructure**, and homeland security perimeter operations — interoperable with modernization threads seen across **Anduril Lattice**, **JIATF-401 marketplace** sourcing constructs, kinetic catch envelopes such as **Fortem Technologies DroneHunter F700-class** systems, high-power microwave concepts comparable to **Epirus Leonidas**, acquisition velocity doctrines exemplified by **Replicator**, and oversight models championed by the **U.S. DHS Program Executive Office for UAS/C-UAS**.

## Core Philosophy

- Max-Defensive Safety Gates (PID ≥ 0.999 + multi-modal evidence)
- Human-on-the-Loop (no autonomous kill-chain)
- DARKSPACE Immutable Audit (HMAC hash-chain on every event)
- Explainable AI (XAI) on every recommendation
- Layered Defensive Architecture (Ground Sensors → High-Altitude Scout → Deployable Kinetic Interceptors)
- Zero Trust + Adversarial Resilience

## 21-Capability Cognitive Architecture

Ancile Aeris integrates 21 advanced capabilities including neuromorphic perception, cognitive electronic warfare, agentic multi-agent C2, generative digital twin, causal XAI, adversarial defense, high-altitude scout mothership with deployable kinetic interceptors, and more. All capabilities are modular and fully integrated with DARKSPACE and safety gates.

## Documentation

- docs/COGNITIVE_ARCHITECTURE.md
- docs/LRBAA_BORAP_04_MAPPING.md
- `submission/Ancile_Aeris_LRBAA_Concept_Paper.md`
- `submission/Ancile_Aeris_Quad_Chart.md`
- `submission/Demo_Video_Script.md`
- SUBMISSION_CHECKLIST.md

## Ownership

Ancile Aeris is the exclusive property of Fratres X AI. All rights reserved.
