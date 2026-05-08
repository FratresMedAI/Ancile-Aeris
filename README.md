# Ancile Aeris

**Property of Fratres X AI**

**Solicitation context:** Responsive to **DHS S&T LRBAA 24-01** (SAM.gov Notice ID **DHS_ST_LRBAA_24-01** · [official notice](https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view)), **BORAP 04 — Countering Unmanned Aircraft Systems** (Type II foundational modeling + Type III emerging-threat extensibility). Software-first simulation today; phased RF laboratory path described in Concept Paper—not field weaponization.

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

Layered **`ancile_aeris_effectors`** stack models **advanced layered response** pathways—deception, cognitive jamming **recommendations**, GNSS/link deception concepts, HPM-class denial **stub**, dual-authorized takeover **concept**—all **simulation stubs** honoring **layered non-kinetic defeat capability** semantics in policy code.

Fratres X AI is **a specialized software-defined defense team with deep ROS 2 and cognitive systems expertise, delivering modular, auditable prototypes for federal acquisition pathways.**

**Prototype maturity (illustrative, not contractual):** current **Technology Readiness Level 3–4** integrated simulation; an indicative **Phase I** cost band of roughly **$250k–$350k** matches the foundational hardening described in [`submission/Ancile_Aeris_Concept_Paper_v2.0.md`](submission/Ancile_Aeris_Concept_Paper_v2.0.md); an **~18-month** laboratory **Software Defined Radio (SDR)** integration path toward **TRL 6** bench demos is a roadmap statement—not fielded weapons.

In **representative internal synthetic evaluations** (**N≈500** parameterized swarm scenarios, **not OT&E**) the materials cite approximately **94% fused-track correlation** and **effector-selection confidence greater than 0.88** under stated assumptions. These are **benchmark context** for reviewers, not operational test results.

## Basic Demo

The v2.0 basic demonstration is the LRBAA slice: sensors • fusion • DARKSPACE audit • safety gate • high-altitude scout mothership • operator copilot • **non-kinetic effectors**.

Docker:

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

**Optional** **`baby_interceptor`** (pure simulation scaffolding—**never default on**, **paired human approvals** mandated by policy when enabled):

```bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py enable_baby_interceptor:=true
```

Representative subscriber proof:

```bash
ros2 topic list | grep -E '^/fused_tracks|^/audit/events|^/scout_eyes|^/safety_gate_status|^/effector/|^/cognitive_ew_commands|^/proposed_actions|^/digital_twin_result'
ros2 service list | grep -E '/ancile_aeris_operator_copilot/query'
```

The basic demo enables the non-kinetic planner and thin cognitive traverse by default via **`features.effectors.enabled`** and **`features.cognitive_demo_chain.enabled`** in **`src/ancile_aeris_bringup/config/payload_selector.yaml`**.

- **`/effector/selected_plan`** — JSON plan (monitor-only unless authorized safety context).  
- **`/effector/status`** — per-mode readiness.  
- **`/proposed_actions`→`/digital_twin_result`→`/cognitive_ew_commands`** — XAI-bearing cognitive EW echo.

Twin mothership shim example:

```bash
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-001 -p enable_mesh_publish:=true
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-002 -p enable_mesh_publish:=true
ros2 topic pub /mesh/mothership_peers/heartbeat std_msgs/msg/String '{"data":"{\"mothership_id\":\"mhs-002\"}"}' -1
ros2 topic echo /mesh/mothership_swarm_status
```

## Repository layout notes

- Payload selector **`src/ancile_aeris_bringup/config/payload_selector.yaml`**.  
- LRBAA packages **`src/scout_mothership/`** • **`src/baby_interceptor/`** (`ament_cmake` wrappers). Expanded cognitive modules **`src/ancile_aeris_cognitive/`**.  
- Formal narrative PDF sources live under **`submission/`** (**`Ancile_Aeris_*_v2.0*.md`** etc.).

## Cross-platform Docker (Windows bind-mount CRLF)

Bind mounts can poison shebangs (**`Exec format error`**). Compose strips `\r`; launch files prepend **`python3`** for resilience against CRLF quirks on Python entrypoints.

## Mission

Provide auditable ROS 2 **detect → track → identify → mitigate modeling** emphasizing **dense urban congestion**, **mass gatherings**, **critical infrastructure**, plus **Secure Borders and Approaches** mission framings under BORAP narrative—paired with interoperability **context references** (**Anduril Lattice**‑style overlays, **JIATF‑401 Marketplace** sourcing idiom, **Replicator 2 velocity** doctrine analogue, lightweight **Leonidas‑class HPM wording** confined to modeled stub—not hardware, **Fortem DroneHunter naming** purely **optional third‑party illustrative capture geometry** absent any integration endorsement).

### Integration hooks roadmap

Public ROS buses (`/fused_tracks`, `/effector/*`, `/darkspace/status`, `/cognitive_ew_commands`, mesh topics) support future **government-furnished sensors**, **approved non-kinetic effector adapters**, and **SDR laboratory** integration as described in the Concept Paper.

## Core Philosophy

- Max-defensive safety gates (**PID ≥ 0.999** plus multi-modal evidence)  
- Strict human‑on‑the‑loop; **never** latent kill automation  
- DARKSPACE immutable hashing for oversight / analytic replay  
- XAI overlays on selectable modeling outcomes  
- **Layered posture:** ground sensing → mothership ISR → **non‑kinetic** modes first (**optional kinetic‑adjacent sim code path** explicitly rare & heavily gated)

## Cognitive architecture snapshot

Twenty‑plus modular cognitive adjuncts—including digital twin EW rehearsal, causal XAI, adversarial hardening—for roadmap expansion; mothership ISR primary today; kinetic capture **never** marketed.

## Documentation

- `docs/COGNITIVE_ARCHITECTURE.md`  
- `docs/LRBAA_BORAP_04_MAPPING.md`  
- `submission/Ancile_Aeris_Concept_Paper_v2.0.md`  
- `submission/Ancile_Aeris_Quad_Chart_v2.0.md`  
- `submission/Ancile_Aeris_Video_Script_v2.0.md`  
- `submission/Video_Production_Package.md`  
- `SUBMISSION_CHECKLIST.md`

## Ownership

Ancile Aeris is the exclusive property of Fratres X AI. All rights reserved.

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.
