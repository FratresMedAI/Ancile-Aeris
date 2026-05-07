Revised May 7, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.0 Concept Paper

**LRBAA Counter-UAS / Anti-Terror Defensive System Concept**  
**Property of Fratres X AI**  
**GitHub:** https://github.com/FratresMedAI/Ancile-Aeris

## Why Ancile Aeris

Ancile Aeris v2.0 gives DHS evaluators a working, auditable C-UAS software layer that moves beyond detection into human-governed, layered non-kinetic defeat. It demonstrates the exact operational balance required for homeland defense: decisive effect selection, clean auditability, and no autonomous weapon release.

## Executive Summary

Ancile Aeris v2.0 is a fully integrated ROS 2 counter-UAS (C-UAS) and anti-terror defensive platform for mass-gathering security, critical infrastructure defense, and modular federal acquisition pathways. The verified stack combines multi-modal sensing, deterministic fusion, mesh-coordinated scout mothership ISR, PID >= 0.999 safety gates, clean DARKSPACE audit status, cognitive EW recommendation logic, and a full layered non-kinetic defeat stack.

The central innovation is `ancile_aeris_effectors`: a simulation-safe effector selection layer modeling HPM-class denial, cognitive jamming, GNSS/link spoofing, authorized control-link takeover, multi-sensor deception, and monitor mode. The cognitive chain selects among these options and publishes explainable AI (XAI) rationale, producing a lethally effective but human-governed defensive architecture.

Final verification confirms a clean demonstration posture: `/darkspace/status` reports `integrity_ok: true` and `chain_gap_count: 0`; `/effector/selected_plan`, `/effector/status`, and `/cognitive_ew_commands` publish live; and the system demonstrates sensing-to-fusion-to-effectors-to-audit continuity.

## Mission Need

Adversarial small UAS threats compress response timelines around stadiums, transit nodes, energy infrastructure, ports, public events, and national special security activities. Operators need more than detection: they need defensible decision support that can correlate evidence, recommend low-collateral defeat options, preserve human authority, and generate audit artifacts suitable for after-action review.

Ancile Aeris answers that need as a system-of-systems software layer: sensing, fusion, safety, mesh ISR, cognitive selection, non-kinetic effect modeling, XAI, and audit all operate together through ROS 2 topic contracts.

## Technical Approach

Ancile Aeris v2.0 is organized as a modular ROS 2 workspace. The LRBAA demonstration slice launches with:

```bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

### Sensing, Fusion, and ISR

The platform simulates visual, thermal, acoustic, RF, lidar, and SIGINT-style inputs. These feed `/fused_tracks`, producing structured track records with confidence, modality coverage, and simulation-labeled counter-terror cues.

The `scout_mothership` package adds mesh-coordinated ISR through:

- `/scout_eyes`
- `/mesh/mothership_swarm_status`
- `/mesh/mothership_peers/heartbeat`

This supports an Anduril Lattice-style common operating picture: distributed coverage, sector assignment, resilient awareness, and defensive handoff logic.

### Safety Gates and Human Authority

PID >= 0.999 safety context constrains downstream recommendations. High-consequence options remain monitor-only unless configured human approval paths are satisfied. Control-link takeover concepts require dual-authorization semantics. The demo separates recommendation, simulation, and actuation: it recommends layered defensive responses but never autonomously releases a weapon or drives real effector hardware.

### DARKSPACE Audit

DARKSPACE subscribes to `/audit/events` and publishes `/darkspace/status`. The v2.0 audit fix isolates hash chains per emitting process using `chain_id`, preventing independent publishers from being evaluated as one chain. Final verification showed:

- `integrity_ok: true`
- `chain_gap_count: 0`
- zero `darkspace hash-chain mismatch observed` warnings

This gives evaluators a clean oversight narrative: each major event is observable, traceable, and suitable for compliance review.

## Core Innovation: Layered Non-Kinetic Defeat

`ancile_aeris_effectors` is the v2.0 differentiator. It makes non-kinetic defeat visible, selectable, auditable, and explainable.

| Effector Mode | Defensive Role | Safety Posture |
|---|---|---|
| `monitor` | Passive ISR and no-action state | Default safe state |
| `multi_sensor_deception` | Deception / sensor disagreement modeling | Human-gated simulation |
| `cognitive_jamming` | Adaptive RF denial recommendation | Human-gated simulation |
| `gnss_link_spoofing` | Navigation / link deception modeling | Human-gated simulation |
| `hpm_denial_stub` | HPM-class non-kinetic denial concept | Simulation-only |
| `control_link_takeover` | Authorized recovered-link takeover concept | Dual authorization required |

The package publishes `/effector/selected_plan` and `/effector/status`. Each selected plan includes track ID, selected mode, family, score, authorization state, monitor-only status, catalog considered, and XAI rationale.

## Cognitive Selection and XAI

Ancile Aeris v2.0 connects effectors into the cognitive EW path:

```text
agent_orchestrator -> digital_twin -> cognitive_ew -> /cognitive_ew_commands
```

The cognitive output includes `selected_effector_mode`, `effector_family`, `effector_plan_id`, `xai_rationale`, `monitor_only`, and RF recommendation parameters. This proves the platform is not simply listing effects; it is selecting a defensible non-kinetic option and explaining why.

## Government and Industry Alignment

Ancile Aeris v2.0 aligns with DHS and defense modernization priorities:

- **DHS Program Executive Office for UAS/C-UAS:** defensive C-UAS, event protection, and critical infrastructure security.
- **Anduril Lattice:** mesh ISR and common operating picture analogs.
- **JIATF-401 Marketplace:** modular acquisition and integration pathway.
- **Fortem DroneHunter F700-class:** low-collateral intercept/capture reference for optional simulation pathways.
- **Epirus Leonidas:** HPM-class non-kinetic effect framing represented as a safe software stub.
- **Replicator 2:** rapid software-defined defense fielding posture.

Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Team and Execution Readiness

Fratres X AI has delivered a working, auditable ROS 2 defense-tech prototype with buildable packages across sensing, fusion, safety, audit, scout ISR, cognitive EW, bringup, and non-kinetic effectors. The repository is live, tagged, and verified with clean runtime outputs for DARKSPACE status, effector selection, cognitive EW, and topic-level proof points.

The architecture is intentionally modular: each capability exposes clear ROS 2 topics and JSON contracts, making Ancile Aeris extensible to future sensors, dashboards, decision models, and integration testbeds.

## Impact

Ancile Aeris v2.0 gives DHS evaluators a concrete, inspectable software layer for next-generation defensive C-UAS:

- **Operational:** faster track correlation, mesh ISR, and layered response recommendations.
- **Technical:** non-kinetic effectors are visible, selectable, auditable, and explainable.
- **Oversight:** DARKSPACE status and XAI outputs support review and legal defensibility.
- **Acquisition:** the stack maps cleanly to modular marketplace and rapid-fielding pathways.

Ancile Aeris v2.0 demonstrates a C-UAS system that is lethally effective in defeat logic while remaining human-governed, simulation-safe, and submission-credible.

## Production Notes

- Convert to PDF with Fratres X AI branding, repository link, and one architecture figure.
- Recommended visuals: ROS 2 topic graph, effector catalog, DARKSPACE status screenshot, and mesh ISR diagram.
- Use the standard disclaimer verbatim in the footer or final page.

Ancile Aeris v2.0 is ready for evaluation, integration discussions, and acquisition pathway alignment.

**Ancile Aeris v2.0 - Property of Fratres X AI**
