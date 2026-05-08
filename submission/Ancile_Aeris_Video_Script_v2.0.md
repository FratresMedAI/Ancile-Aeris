Revised May 8, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.0 Four-Minute Video Script

**Solicitation:** DHS S&T LRBAA **24-01** (Notice ID **DHS_ST_LRBAA_24-01**) · **BORAP 04 — Countering Unmanned Aircraft Systems** (Type II / Type III). SAM.gov: https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view  
**LRBAA Counter-UAS / Anti-Terror Defensive System**  
**Property of Fratres X AI**  
**GitHub:** https://github.com/FratresMedAI/Ancile-Aeris  
**Target Runtime:** 4:00  
**Tone:** calm, measured, evidence-led, credible to federal reviewers  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

Approximately ninety percent of the story is **non-kinetic modeling** (fusion, audit, mesh ISR, layered effector stubs, cognitive XAI outputs). **`baby_interceptor`** is simulation-only, **off by default**, **optional**, and requires **dual human authorization** when enabled—not demonstrated in the primary cut.

## Narration + Visual Script

| Time | Narration | On-Screen Visual |
|---|---|---|
| 0:00–0:15 | "Ancile Aeris v2.0 is ROS 2 counter-UAS software framed for DHS Science and Technology Long Range Broad Agency Announcement twenty-four-zero-one—the active notice is on SAM-dot-gov—and Topic BORAP zero-four, Countering Unmanned Aircraft Systems. We address detection through mitigation in dense urban venues, mass gatherings, critical infrastructure, and border-adjacency contexts **in simulation only**." | Title: Ancile Aeris v2.0 • BORAP 04 • Layered non-kinetic modeling. Small persistent **Simulation only** watermark. |
| 0:15–0:30 | "GitHub carries the audited slice: sensing, deterministic fusion on `/fused_tracks`, scout mesh ISR, safety gates at PID greater than or equal to zero-point-nine-nine-nine, DARKSPACE status, cognitive EW stubs, and the non-kinetic effector planner—our main technical storyline." | Repo view; emphasize `ancile_aeris_effectors`, `ancile_aeris_darkspace_integration`, `ancile_aeris_bringup`, `scout_mothership`. |
| 0:30–0:50 | "Launch the authoritative basic demo stack." | Terminal: `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`. |
| 0:50–1:12 | "Simulated modality evidence is fused into machine-readable tracks—supporting operator situational awareness, not asserting field sensor performance." | Echo `/fused_tracks`; caption: Multi-modal sensing → fused track records. Optional lower-third one line only: Representative synthetic batch (**N≈500** scenarios): **~94%** fused-track correlation metric; mean effector-selection confidence **>0.88** under stated assumptions—**not OT&E**. |
| 1:12–1:28 | "PID bounded safety context gates higher-consequence options; monitor posture persists until deliberate authorization aligns." | Echo `/safety_gate_status`; caption: PID ≥ 0.999 • Human authority preserved. |
| 1:28–1:55 | "Mesh-coordinated mothership ISR topics mirror common-picture overlays without endorsing vendor platforms." | Echo `/mesh/mothership_swarm_status`, `/scout_eyes`; schematic mesh overlay. |
| 1:55–2:15 | "DARKSPACE reports clean demonstration integrity—`integrity_ok: true`, `chain_gap_count: zero`, consistent with final verification collateral." | Echo `/darkspace/status`; caption DARKSPACE clean. |
| 2:15–2:50 | "**Layered non-kinetic defeat modeling** spanning monitor, deception, cognitive jamming, GNSS-slash-link spoofing concepts, HPM-class denial **stub**, and dual-authorized takeover **concept**, each labeled simulation." | Echo `/effector/status`; restrained catalog graphic; highlight **STUB / SIMULATION** tags. |
| 2:50–3:15 | "`/effector/selected_plan` publishes the modeled response: mode selection, rationale, authorization, monitor-only state—**advanced layered response modeling**, not autonomous release." | Echo `/effector/selected_plan`; zoom `selected.mode`, `xai.rationale`, `authorized`, `monitor_only`. |
| 3:15–3:32 | "`/cognitive_ew_commands` surfaces the cognitive chain output with comparable explainability fields—closing the loop operator-side." | Echo `/cognitive_ew_commands`. |
| 3:32–3:43 | "**Transparency**: optional `baby_interceptor` scaffolding exists purely in simulation—it is disabled in this demonstration, gated if ever used, and always requires paired human approvals—outside the ninety-percent narrative focus." | One-line supers; no flashy graphics. |
| 3:43–3:55 | "Acquisition posture references open ROS 2 interfaces today, phased **SDR laboratory** coupling toward Technology Readiness Level six, illustrative Phase I cost roughly two hundred fifty to three hundred fifty thousand dollars, and packaging concepts consistent with **JIATF–401 Marketplace** interoperability—government references contextual only." | Typographic roadmap slate; abbreviated **$250k–$350k Phase I**. |
| 3:55–4:00 | "**Ancile Aeris stays simulation-honest while presenting audited, layered, non-kinetic software for evaluator review.**" | Closing slate; GitHub path; verbatim disclaimer footer. |

## Required Live Commands

```bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

In a second terminal:

```bash
ros2 topic list | grep -E 'effector|cognitive_ew|darkspace|audit|mesh|fused_tracks'
ros2 topic echo --once /darkspace/status
ros2 topic echo --once /effector/status
ros2 topic echo --once /effector/selected_plan
ros2 topic echo --once /cognitive_ew_commands
ros2 topic echo --once /mesh/mothership_swarm_status
```

## On-Screen Text Candidates

- BORAP 04 • Detect • Track • Identify • Mitigate (simulation context)  
- Layered non-kinetic defeat modeling / advanced layered response modeling  
- DARKSPACE: `integrity_ok=true`, `chain_gap_count=0`  
- Human-on-the-loop; no autonomous weapon release  
- ROS 2 open interfaces • JIATF–401 roadmap context  

## Standard Disclaimer

Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Production Notes

- Record 1080p or higher; large monospace; dark theme preferred.  
- Dual terminal layout: launch left, proof right.  
- Avoid combat imagery; keep motion graphics minimal.  
- Display the **standard disclaimer** at open (title card) and close (full-screen footer).  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

**Ancile Aeris v2.0 - Property of Fratres X AI**
