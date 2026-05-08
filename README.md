# Ancile Aeris

**Property of Fratres X AI**

## Build Instructions – ONLY SUPPORTED METHOD

**Ancile Aeris is ONLY supported inside the official Docker container** (see the [`docker/`](docker/) folder). Do **not** run `colcon build` natively on Windows: mixed Linux (`/opt/ancile_aeris_ws`) and Windows bind-mount caches produce broken `CMakeCache.txt`, missing `gmake`, and `WinError 1920` on symlinked `local_setup.bash`.

From the repository root on the **host**, start the stack (builds inside Linux):

```bash
ANCILE_LAUNCH_FILE=ancile_aeris_basic_demo.launch.py docker compose -f docker/docker-compose.yml up --build
```

**Inside the running container**, use this **four-command** clean build sequence whenever you need a fresh tree:

```bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
rm -rf build/ install/ log/
colcon build --symlink-install --packages-up-to ancile_aeris_bringup
```

Or run the same steps with the helper script (`chmod +x clean-build.sh` is applied in the Docker image build; on Linux hosts you may `chmod +x` once at the repo root). The script sources `/opt/ros/kilted/setup.bash` before `colcon` so non-interactive shells have the right `PATH`.

```bash
./clean-build.sh
```

After a successful run, the workspace is already sourced inside the script; in a new shell use `source install/setup.bash`, then e.g. `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`.

---

**Solicitation context:** Responsive to **DHS S&T LRBAA 24-01** (SAM.gov Notice ID **DHS_ST_LRBAA_24-01** · [official notice](https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view)), **BORAP 04 — Countering Unmanned Aircraft Systems** (Type II foundational modeling + Type III emerging-threat extensibility). Software-first simulation today; phased RF laboratory path described in Concept Paper—not field weaponization.

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

Layered **`ancile_aeris_effectors`** stack models **advanced layered response** pathways—deception, cognitive jamming **recommendations**, GNSS/link deception concepts, HPM-class denial **stub**, dual-authorized takeover **concept**—all **simulation stubs** honoring **layered non-kinetic defeat capability** semantics in policy code.

Fratres X AI is **a specialized software-defined defense team with deep ROS 2 and cognitive systems expertise, delivering modular, auditable prototypes for federal acquisition pathways.**

**Prototype maturity (illustrative, not contractual):** current **Technology Readiness Level 3–4** integrated simulation; an indicative **Phase I** cost band of roughly **$250k–$350k** matches the foundational hardening described in [`submission/Ancile_Aeris_Concept_Paper_v2.1.md`](submission/Ancile_Aeris_Concept_Paper_v2.1.md); an **~18-month** laboratory **Software Defined Radio (SDR)** integration path toward **TRL 6** bench demos is a roadmap statement—not fielded weapons.

In **representative internal synthetic evaluations** (**N≈500** parameterized swarm scenarios, **not OT&E**) the materials cite approximately **94% fused-track correlation** and **effector-selection confidence greater than 0.88** under stated assumptions. These are **benchmark context** for reviewers, not operational test results.

## Basic Demo (v2.1)

The default **basic demonstration** is the BORAP slice: sensors • fusion • DARKSPACE audit • safety gate • **mothership forward operating base (FOB) swarm** with **modular micro-drone payload simulation** • operator copilot • **non-kinetic-first effectors** (`kamikaze_ram` exists only as **simulation**, **off in default policy**, **last resort**).

```bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

Representative subscriber proof:

```bash
ros2 topic list | grep -E '^/fused_tracks|^/audit/events|^/scout_eyes|^/safety_gate_status|^/mesh/fob_status|^/payload/micro_deployment|^/effector/|^/cognitive_ew_commands|^/kamikaze_status|^/proposed_actions|^/digital_twin_result'
ros2 service list | grep -E '/ancile_aeris_operator_copilot/query'
```

The default profile is **`mothership_fob_standard`** in **`src/ancile_aeris_bringup/config/payload_selector.yaml`**: **2–4** FOB carriers (scout motherships) and **10–12** modular micro slots per FOB (sensor pod, acoustic disruptor, kevlar web, cognitive EW pod, kamikaze ram slot). **`features.effectors.enabled`** and **`features.cognitive_demo_chain.enabled`** turn on the planner and cognitive traverse.

- **`/mesh/fob_status`** — JSON fleet + per-FOB micro inventory (simulation).  
- **`/payload/micro_deployment`** — advisory deployment views; includes **`effector_alignment`** hints from `/effector/selected_plan`.  
- **`/effector/selected_plan`** — JSON plan (**non-kinetic-first** unless kinetic family enabled in policy).  
- **`/effector/kamikaze_authorized`** — kinetic ram authorization telemetry when policy allows **`kamikaze_ram`** (default: not authorized).  
- **`/proposed_actions`→`/digital_twin_result`→`/cognitive_ew_commands`** — XAI-bearing cognitive EW echo.

**Optional legacy** **`baby_interceptor`** (not included in the default launch graph; simulation-only if built/run separately).

Twin mothership shim example (manual spot-check beyond FOB swarm):

```bash
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-001 -p enable_mesh_publish:=true
ros2 run scout_mothership scout_mothership_node --ros-args -p mothership_id:=mhs-002 -p enable_mesh_publish:=true
ros2 topic pub /mesh/mothership_peers/heartbeat std_msgs/msg/String '{"data":"{\"mothership_id\":\"mhs-002\"}"}' -1
ros2 topic echo /mesh/mothership_swarm_status
```

## Repository layout notes

- Payload selector **`src/ancile_aeris_bringup/config/payload_selector.yaml`**.  
- LRBAA packages **`src/scout_mothership/`** • **`src/ancile_aeris_micro_payloads/`** (five micro payload sim nodes + kamikaze ram) • optional **`src/baby_interceptor/`**. Expanded cognitive modules **`src/ancile_aeris_cognitive/`**.  
- Formal LRBAA narrative and quad chart (latest) live under **`submission/`** (**`*_v2.1.*`** — see [`submission/LRBAA_Submission_Package_v2.1.md`](submission/LRBAA_Submission_Package_v2.1.md)). Older `*_v2.0.*` filenames are retained for history.

## Cross-platform Docker (Windows bind-mount CRLF)

Bind mounts can poison shebangs (**`Exec format error`**). Compose strips `\r`; launch files prepend **`python3`** for resilience against CRLF quirks on Python entrypoints.

## Mission

Provide auditable ROS 2 **detect → track → identify → mitigate modeling** emphasizing **dense urban congestion**, **mass gatherings**, **critical infrastructure**, plus **Secure Borders and Approaches** mission framings under BORAP narrative—paired with interoperability **context references** (**Anduril Lattice**‑style overlays, **JIATF‑401 Marketplace** sourcing idiom, **Replicator 2 velocity** doctrine analogue, lightweight **Leonidas‑class HPM wording** confined to modeled stub—not hardware, **Fortem DroneHunter naming** purely **optional third‑party illustrative capture geometry** absent any integration endorsement).

### Integration hooks roadmap

Public ROS buses (`/fused_tracks`, `/effector/*`, `/darkspace/status`, `/cognitive_ew_commands`, mesh topics, **`/mesh/fob_status`**, **`/payload/micro_deployment`**) support future **government-furnished sensors**, **approved non-kinetic effector adapters**, and **SDR laboratory** integration as described in the Concept Paper.

## Core Philosophy

- Max-defensive safety gates (**PID ≥ 0.999** plus multi-modal evidence)  
- Strict human‑on‑the‑loop; **never** latent kill automation  
- DARKSPACE immutable hashing for oversight / analytic replay  
- XAI overlays on selectable modeling outcomes  
- **Layered posture:** ground sensing → **FOB mothership swarm** → **modular micro payloads (sim)** → **non‑kinetic** ship modes first; optional **`kamikaze_ram`** sim is **last resort** and **policy-off** by default (**legacy `baby_interceptor`** off-demo)

## Cognitive architecture snapshot

Twenty‑plus modular cognitive adjuncts—including digital twin EW rehearsal, causal XAI, adversarial hardening—for roadmap expansion; **FOB swarm and micro payload simulation** primary in v2.1; kinetic narratives **never** marketed as default.

## Documentation

- `docs/COGNITIVE_ARCHITECTURE.md`  
- `docs/LRBAA_BORAP_04_MAPPING.md`  
- [`submission/LRBAA_Submission_Package_v2.1.md`](submission/LRBAA_Submission_Package_v2.1.md) — **master index for v2.1 LRBAA filing**  
- `submission/Ancile_Aeris_Concept_Paper_v2.1.md`  
- `submission/Ancile_Aeris_Quad_Chart_v2.1.md`  
- `submission/Ancile_Aeris_Video_Script_v2.1.md`  
- `submission/Video_Production_Package_v2.1.md`  
- `submission/Ancile_Aeris_Voiceover_Narration_v2.1.md`  
- `SUBMISSION_CHECKLIST.md`  
- Regenerate Word exports: `python tools/export_submission_docx.py`

## Ownership

Ancile Aeris is the exclusive property of Fratres X AI. All rights reserved.

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.
