Revised May 7, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.0 Four-Minute Video Script

**LRBAA Counter-UAS / Anti-Terror Defensive System**  
**Property of Fratres X AI**  
**GitHub:** https://github.com/FratresMedAI/Ancile-Aeris  
**Target Runtime:** 4:00  
**Tone:** professional, confident, defense-tech, submission-ready

## Narration + Visual Script

| Time | Narration | On-Screen Visual |
|---|---|---|
| 0:00-0:15 | "Ancile Aeris v2.0 is a working ROS 2 counter-UAS and anti-terror defensive platform for mass-gathering security, critical infrastructure protection, and auditable human-governed response." | Title slate: "Ancile Aeris v2.0 - Layered Non-Kinetic C-UAS Defense" with Fratres X AI branding. |
| 0:15-0:30 | "The system is live on GitHub and demonstrates the full defensive pipeline: sensing, fusion, DARKSPACE audit, safety gates, mesh scout ISR, cognitive EW, and layered non-kinetic effectors." | Repo page or package tree; highlight `ancile_aeris_effectors`, `ancile_aeris_bringup`, `scout_mothership`, and `ancile_aeris_darkspace_integration`. |
| 0:30-0:50 | "We begin with a clean ROS 2 launch of the LRBAA demo stack." | Terminal: `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`. |
| 0:50-1:10 | "The platform fuses simulated visual, thermal, acoustic, RF, lidar, and SIGINT-style evidence into machine-readable tracks on `/fused_tracks`." | Echo `/fused_tracks`; overlay: "Multi-modal evidence -> fused C-UAS track." |
| 1:10-1:30 | "A PID >= 0.999 safety context constrains downstream recommendations. High-consequence actions remain monitor-only unless authorization is satisfied." | Echo `/safety_gate_status`; overlay: "PID >= 0.999 | Human authority preserved." |
| 1:30-1:55 | "The scout mothership layer provides mesh ISR, coordinated coverage, and Lattice-style situational awareness analogs." | Echo `/mesh/mothership_swarm_status` and `/scout_eyes`; show simple mesh map graphic. |
| 1:55-2:20 | "DARKSPACE audit is clean. The verified status is `integrity_ok: true`, `chain_gap_count: 0`, with zero hash-chain mismatch warnings." | Echo `/darkspace/status`; overlay: "DARKSPACE Clean." |
| 2:20-2:55 | "The core v2.0 innovation is the layered non-kinetic defeat stack: HPM-class denial, cognitive jamming, GNSS/link spoofing, control-link takeover, multi-sensor deception, and monitor mode." | Echo `/effector/status`; animated effector catalog. |
| 2:55-3:20 | "The platform selects an effector plan for the current track and publishes decision logic, authorization state, monitor-only status, and XAI rationale on `/effector/selected_plan`." | Echo `/effector/selected_plan`; zoom on `selected.mode`, `xai.rationale`, `monitor_only`, `authorized`. |
| 3:20-3:40 | "The cognitive EW chain converts the plan into a human-vetted recommendation on `/cognitive_ew_commands`, preserving explainability and operator control." | Echo `/cognitive_ew_commands`; highlight `selected_effector_mode`, `effector_family`, `xai_rationale`. |
| 3:40-3:52 | "Ancile Aeris v2.0 aligns with DHS PEO UAS/C-UAS priorities and integration pathways associated with Anduril Lattice, JIATF-401 Marketplace, Fortem DroneHunter F700-class systems, Epirus Leonidas-style non-kinetic concepts, and Replicator 2 rapid fielding." | Logo-neutral alignment slate. |
| 3:52-4:00 | "Ancile Aeris v2.0 is submission-ready: layered, auditable, non-kinetic, and human-governed." | Closing slate: "Ancile Aeris v2.0 - Property of Fratres X AI - GitHub: FratresMedAI/Ancile-Aeris." |

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

## On-Screen Text

- "Full layered non-kinetic defeat stack"
- "HPM-class denial | cognitive jamming | GNSS/link spoofing | control-link takeover | multi-sensor deception"
- "Cognitive selection with XAI rationale"
- "DARKSPACE clean: integrity_ok=true, chain_gap_count=0"
- "Human-on-the-loop: no autonomous weapon release"
- "DHS PEO UAS/C-UAS | JIATF-401 Marketplace | Replicator 2"
- "Property of Fratres X AI"

## Standard Disclaimer

Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Production Notes

- Record in 1080p or higher with a large terminal font and dark theme.
- Keep two terminal panes: launch on the left, topic proof on the right.
- Use restrained motion graphics for the pipeline, effector catalog, DARKSPACE status, and mesh ISR.
- Music should be modern, confident, and controlled; avoid aggressive combat cues.
- Narration should be calm, senior, technical, and evidence-driven.

**Ancile Aeris v2.0 - Property of Fratres X AI**
