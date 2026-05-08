Revised May 8, 2026 — Aligned with `Ancile_Aeris_Concept_Paper_v2.0.md` (LRBAA red-team compliance)

# Ancile Aeris Concept Paper

**Solicitation:** DHS S&T **LRBAA 24-01** (SAM.gov Notice ID **DHS_ST_LRBAA_24-01** — [active opportunity](https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view)). This concept is **responsive to** **Topic BORAP 04 — Countering Unmanned Aircraft Systems** (Type II foundational science and Type III future-threat objectives); authoritative terms remain on SAM.gov and attached amendments.  
**LRBAA Counter-UAS / Anti-Terror Defensive System Concept**  
**Property of Fratres X AI**  
**GitHub:** https://github.com/FratresMedAI/Ancile-Aeris  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Why Ancile Aeris

Ancile Aeris v2.0 is a working, auditable ROS 2 C-UAS layer for **dense urban venues, mass gatherings, critical infrastructure, and border/perimeter approaches** described under BORAP 04: it progresses from fused evidence through human-governed **layered non-kinetic defeat capability**—with **advanced layered response modeling**, explainable rationale, immutable audit posture, and no autonomous weapon release.

## Executive Summary

Ancile Aeris v2.0 integrates sensing, deterministic fusion to `/fused_tracks`, scout mesh ISR, PID ≥ 0.999 safety gates, DARKSPACE audit, cognitive EW, and **`ancile_aeris_effectors`**: simulation-safe selection among monitor, deception, cognitive jamming, GNSS/link spoofing, HPM-class denial *stub*, and dual-authorized control-link takeover *concepts*. The cognitive chain emits XAI-linked plans on `/effector/selected_plan` and `/cognitive_ew_commands`; runtime verification shows `/darkspace/status` with `integrity_ok: true`, `chain_gap_count: 0`, and continuity from sensing through effector and audit topics.

In a **representative internal synthetic evaluation** (500 parameterized swarm-style scenarios—not operational field testing), fused-track association held **approximately 94% correlation accuracy** subject to simulated ground truth; mean **effector-selection confidence exceeded 0.88** across runs where non-monitor modes engaged under open safety context. Figures bound expected simulation behavior under stated assumptions only.

## Mission Need (Detect → Track → Identify → Mitigate)

BORAP 04 calls for enhanced **detection, tracking, identification, and mitigation** of unmanned aircraft under varied terrain and environments. Ancile Aeris maps each pillar to inspectable ROS 2 behavior:

| Pillar | Ancile Aeris realization (current demo) |
|--------|----------------------------------------|
| Detect | Multi-modal simulated inputs (visual, thermal, acoustic, RF, lidar, SIGINT-style); extensible toward **SDR / RF hardware**. |
| Track | Structured `/fused_tracks` with confidence and modality cues. |
| Identify | Classification-style enrichment on fused records (simulation-labeled); supports operator review pipelines. |
| Mitigate | **Non-kinetic-first** layered response modeling via `ancile_aeris_effectors` + cognitive path; audit via DARKSPACE. |

Across **dense urban clutter, crowded mass gatherings, critical infrastructure geometries, and border-adjacency stress**, timelines compress faster than standalone detection products can satisfy. Ancile Aeris targets **human-governed decision support**, low-collateral option sets, after-action analytic hooks to `/audit/events`, and repeatable software integration paths.

### Optional kinetic-adjacent simulation (minimal scope)

An optional **`baby_interceptor`** node exists strictly as **simulation-only** software, **disabled in the default demo**, gated by operator configuration, and requiring **dual human authorization** when enabled—**not part of this submission narrative** beyond compliance transparency. Ninety-plus percent of the technical story is **non-kinetic**.

## Technical Approach

Demonstration launch:

```bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

**Sensing, fusion, ISR:** Simulated modalities feed `/fused_tracks`. `scout_mothership` publishes mesh-coordinated ISR on `/scout_eyes`, `/mesh/mothership_swarm_status`, and `/mesh/mothership_peers/heartbeat`, supporting Lattice-style COP analogs without vendor endorsement.

**Safety and authority:** Recommendations remain **monitor-only** until safety and authorization predicates are satisfied. The demo separates recommendation, simulation, and actuation—it **never** autonomously releases weapons or drives real effector hardware.

**DARKSPACE:** Subscribes to `/audit/events`, emits `/darkspace/status`; **v2.0 chain isolation (`chain_id`)** yields verified `integrity_ok: true`, `chain_gap_count: 0`, and zero observed hash-chain mismatch warnings.

## Planned Integration Hooks (Beyond Simulation)

**SDR / RF path:** Planned **18-month**, lab-first integration of **software-defined radio** fronts (vendor-agnostic; UHD-style or government-furnished equipment) consuming the same abstraction now satisfied by simulated RF feeds.

**Open ROS 2 interfaces:** Canonical integration surface includes `/fused_tracks`, `/effector/selected_plan`, `/effector/status`, `/cognitive_ew_commands`, `/darkspace/status`, mesh topics, `/safety_gate_status`, and audit streams—adaptable for real sensors and **authorized physical effectors** behind separate hardware abstraction layers.

**JIATF-401 Marketplace (transition framing):** Artifacts are packaged for **listing-style modular uptake**—software deliverables, repeatable launch recipes, verified topic contracts—not an endorsement statement.

## Core Innovation: Layered Non-Kinetic Defeat

`ancile_aeris_effectors` anchors v2.0: non-kinetic modes are visible, selectable, auditable, and XAI-explained.

| Effector Mode | Defensive Role | Safety Posture |
|---|---|---|
| `monitor` | Passive ISR | Default safe state |
| `multi_sensor_deception` | Sensor-disagreement / deception modeling | Human-gated simulation |
| `cognitive_jamming` | Adaptive RF denial recommendation | Human-gated simulation |
| `gnss_link_spoofing` | Navigation / link deception modeling | Human-gated simulation |
| `hpm_denial_stub` | Directed-energy denial *concept* | Simulation-only stub |
| `control_link_takeover` | Authorized link takeover *concept* | Dual authorization |

## Cognitive Selection and XAI

```text
agent_orchestrator -> digital_twin -> cognitive_ew -> /cognitive_ew_commands
```

Downstream payloads carry `selected_effector_mode`, `effector_plan_id`, `xai_rationale`, `monitor_only`, and authorization fields—advanced layered response modeling evidenced on the wire rather than slideware.

## TRL, Cost, Schedule, and Transition Pathway

| Element | Planned posture (not a contractual commitment; SAM.gov is authoritative on the solicitation) |
|---------|--------------------------------------------------------------------------------------------------|
| **Current TRL** | **3–4**: integrated **simulation prototype** with deterministic fusion paths, audited events, cognitive/effector chain. |
| **Post–Phase I target** | **TRL 5**: component validation in laboratory / controlled integration against **representative feeds** (+ initial SDR bring-up). |
| **Phase I cost band** | **$250k–$350k** inclusive range for foundational software maturation described herein. |
| **SDR roadmap** | ~**18-month** phased plan from simulation interface freeze through **TRL 6** closed-loop RF bench demos with licensed hardware—not fielded interception. |
| **Transition** | **JIATF-401 Marketplace** positioning for modular government consumption; optional partner lab integration. |

## Government and Industry Alignment (examples only)

- **DHS PEO UAS/C-UAS** defensive mission threads.  
- **Anduril Lattice** (mesh COP analog).  
- **JIATF-401 Marketplace** acquisition packaging.  
- **Replicator 2** rapid software-defined fielding *concepts*.  
- **Epirus Leonidas**-class HPM *modeled* only via **non-kinetic stub**.  
- **Fortem DroneHunter F700-class** cited solely as optional **third-party reference architecture**—**not simulated, integrated, or endorsed** in this codebase.

## Team and Execution Readiness

Fratres X AI is **a specialized software-defined defense team with deep ROS 2 and cognitive systems expertise, delivering modular, auditable prototypes for federal acquisition pathways.** The organization has shipped buildable ROS 2 packages across sensing, fusion, safety, DARKSPACE, scout mesh ISR, cognitive EW, bringup, and non-kinetic effectors; verification artifacts include clean `/darkspace/status`, live effector publications, tagged GitHub revisions, and colcon-demonstrated bringup paths.

The architecture favors **explicit topic and JSON contracts** for extension to federal testbed dashboards, analytic pipelines, hardware-in-loop labs, and future mission payloads.

## Impact

| Axis | Contribution |
|------|----------------|
| **Operational** | Track correlation uplift in simulation, mesh ISR, explainable mitigation option sets. |
| **Technical** | Layered non-kinetic defeat capability + advanced layered response modeling with XAI linkage. |
| **Oversight** | Immutable audit hashing and rationale records for supervisory and legal workflows. |
| **Acquisition** | Marketplace-oriented packaging and repeatable demonstration scripts. |

Ancile Aeris v2.0 is deliberately **submission-credible**, **human-governed**, and honest about simulation boundaries while presenting a phased TRL escalation with RF hardware—not over-stating present field capability.

## Production Notes

- PDF with Fratres X AI branding + repository link + one architecture figure (`ROS topics / effectors / audit`).  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

**Ancile Aeris — Property of Fratres X AI**
