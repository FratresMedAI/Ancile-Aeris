Revised May 8, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.1 Four-Minute Video Script

**Solicitation:** DHS S&T LRBAA **24-01** (Notice ID **DHS_ST_LRBAA_24-01**) · **BORAP 04 — Countering Unmanned Aircraft Systems** (Type II / Type III).  
**Property of Fratres X AI** · **GitHub:** https://github.com/Fratres-X-AI/Ancile-Aeris  
**Target Runtime:** 4:00  
**Tone:** calm, measured, evidence-led, credible to federal reviewers

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

The primary storyline is **non-kinetic-first** modeling: sensing, fusion, DARKSPACE audit, safety gates, a **Mothership FOB Swarm**, modular micro-drone payload simulation, cognitive XAI outputs, and gated effector recommendations. The **kamikaze ram** is the only kinetic-energy simulation path, is **disabled in default policy**, and requires **double human authorization** when enabled.

## Narration + Visual Script

| Time | Narration | On-Screen Visual |
|---|---|---|
| 0:00-0:15 | "Ancile Aeris v2.1 is a ROS 2 counter-UAS software demonstration for DHS S&T LRBAA 24-01 and BORAP 04. It addresses detect, track, identify, and mitigate workflows for dense urban venues, mass gatherings, critical infrastructure, and border-adjacent contexts in simulation only." | Title slate: Ancile Aeris v2.1 • BORAP 04 • Simulation Only. |
| 0:15-0:30 | "The current build adds a mothership forward operating base swarm. Two to four scout motherships operate as mobile FOBs inside one operational area." | Clean map graphic with 3 FOB nodes and mesh links. |
| 0:30-0:48 | "Each mothership carries a representative ten-to-twelve-slot micro-drone bay. Payloads are modular: sensor pod, acoustic disruptor, kevlar web deployer, cognitive EW pod, and a reserved kamikaze ram slot." | Micro-payload catalog: five cards, all marked simulation. |
| 0:48-1:08 | "The authoritative launch remains the Docker-only ROS 2 demo: `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`." | Terminal-style launch slate. |
| 1:08-1:28 | "Simulated modality evidence fuses into `/fused_tracks`, giving operators machine-readable confidence, modality coverage, and track state without asserting field sensor performance." | Fusion pipeline: sensors to `/fused_tracks`. |
| 1:28-1:48 | "FOB coordination is visible on `/mesh/fob_status` and `/payload/micro_deployment`, including advisory effector-alignment hints tied to the selected plan." | Topic cards for `/mesh/fob_status` and `/payload/micro_deployment`. |
| 1:48-2:08 | "Non-kinetic-first doctrine remains central: monitor, deception, cognitive jamming, GNSS or link spoofing concepts, HPM-class denial stub, and dual-authorized takeover concept are preferred before any kinetic simulation." | Effector hierarchy: non-kinetic bands first. |
| 2:08-2:28 | "The kamikaze ram is explicitly a last-resort kinetic-energy simulation. It is off in default policy and requires safety predicates plus paired human authorization before any notional release narrative." | Gated kinetic panel: double authorization locks. |
| 2:28-2:48 | "DARKSPACE records the trust story through audit events and publishes `/darkspace/status` with integrity fields such as `integrity_ok` and `chain_gap_count`." | DARKSPACE status screen with clean JSON. |
| 2:48-3:08 | "`/effector/selected_plan` publishes the modeled response: mode, rationale, authorization state, and monitor-only flag. This is advanced layered response modeling, not autonomous engagement." | Selected-plan JSON excerpt. |
| 3:08-3:28 | "`/cognitive_ew_commands` carries comparable XAI fields for the cognitive path, keeping operator review and auditability visible." | Cognitive EW command path. |
| 3:28-3:45 | "The transition path is disciplined: open ROS 2 interfaces now, SDR laboratory integration later, and marketplace-style modular packaging for government evaluation." | Roadmap slate: ROS 2 → SDR lab → TRL 6 bench. |
| 3:45-4:00 | "Ancile Aeris v2.1 is simulation-honest, human-governed, auditable, and ready for LRBAA reviewer inspection." | Closing slate with disclaimer and GitHub URL. |

## Required Live Commands

```bash
cd /opt/ancile_aeris_ws
./clean-build.sh
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

In a second terminal:

```bash
ros2 topic list | grep -E 'effector|cognitive_ew|darkspace|audit|mesh|fused_tracks|fob_status|micro_deployment|kamikaze'
ros2 topic echo /darkspace/status std_msgs/msg/String --once
ros2 topic echo --once /mesh/fob_status
ros2 topic echo --once /payload/micro_deployment
ros2 topic echo --once /effector/selected_plan
```

## On-Screen Text Candidates

- BORAP 04 • Detect • Track • Identify • Mitigate
- Mothership FOB Swarm: 2-4 mobile FOBs
- Modular micro-drone bay: 10-12 slots per mothership
- Non-kinetic-first doctrine
- Kamikaze ram: simulation only • last resort • double authorization
- DARKSPACE: `integrity_ok=true`, `chain_gap_count=0`
- Human-on-the-loop; no autonomous weapon release

## Standard Disclaimer

Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

**Ancile Aeris v2.1 - Property of Fratres X AI**
