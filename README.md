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
ros2 topic list | grep -E '^/fused_tracks|^/audit/events|^/scout_eyes|^/safety_gate_status|^/effector/|^/cognitive_ew_commands|^/proposed_actions|^/digital_twin_result'
ros2 service list | grep -E '/ancile_aeris_operator_copilot/query'
```

The basic demo also brings up the non-kinetic effector stack and a thin
cognitive selection chain by default (toggle via `features.effectors.enabled`
and `features.cognitive_demo_chain.enabled` in `payload_selector.yaml`):

- `/effector/selected_plan` — layered non-kinetic plan with XAI rationale
  (multi-sensor deception, cognitive jamming, GNSS/link spoofing, HPM-class
  denial, authorized control-link takeover; monitor-only by default).
- `/effector/status` — per-mode readiness telemetry.
- `/proposed_actions` -> `/digital_twin_result` -> `/cognitive_ew_commands` —
  cognitive selection chain that ingests the effector plan and surfaces the
  human-vetted recommendation.

Run two mesh mothership simulators (shared heartbeat topic, distinct IDs):

```bash
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-001 -p enable_mesh_publish:=true
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-002 -p enable_mesh_publish:=true
ros2 topic pub /mesh/mothership_peers/heartbeat std_msgs/msg/String '{"data":"{\"mothership_id\":\"mhs-002\"}"}' -1
ros2 topic echo /mesh/mothership_swarm_status
```

## Repository layout notes

- Payload selector file path: `src/ancile_aeris_bringup/config/payload_selector.yaml`.
- LRBAA core packages (`scout_mothership`, `baby_interceptor`) live at `src/scout_mothership/` and `src/baby_interceptor/` (`ament_cmake` + `install(PROGRAMS …)`). Mesh ISR topics publish under `/mesh/...`. Additional roadmap cognitive modules remain under `src/ancile_aeris_cognitive/`.
- LRBAA submission artifacts live under `submission/`.

## Cross-platform Docker note (Windows bind mounts)

When `/opt/ancile_aeris_ws` is bind-mounted from Windows, Python entry scripts can pick up CRLF line endings and fail on Linux with `OSError: [Errno 8] Exec format error`. The Docker Compose command strips `\\r` from `src/**/*.py` before building, and the basic demo launch files run Python nodes under `python3` for additional hardening.

If you are fixing wrappers manually, Python nodes (`scout_mothership_node`, `baby_interceptor_node`) install via CMake `install(PROGRAMS …)` under `install/<pkg>/lib/<pkg>/`. Launches prepend `python3` to survive Docker bind-mount CRLF quirks.

## Mission

Ancile Aeris delivers layered, trustworthy, human-on-the-loop defense against drone threats in dense urban environments, **mass gatherings**, **critical infrastructure**, and homeland security perimeter operations — interoperable with modernization threads seen across **Anduril Lattice**, **JIATF-401 Marketplace** sourcing constructs, kinetic catch envelopes such as **Fortem Technologies DroneHunter F700-class** systems, high-power microwave concepts comparable to **Epirus Leonidas**, acquisition velocity doctrines exemplified by **Replicator 2**, and oversight models championed by the **U.S. DHS Program Executive Office for UAS/C-UAS**.

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
- `submission/Ancile_Aeris_Concept_Paper.md`
- `submission/Ancile_Aeris_Quad_Chart.md`
- `submission/Video_Script.md`
- SUBMISSION_CHECKLIST.md

## Ownership

Ancile Aeris is the exclusive property of Fratres X AI. All rights reserved.
