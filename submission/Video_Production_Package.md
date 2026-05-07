Revised May 7, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.0 Video Production Package

**Runtime:** 4:00  
**Audience:** DHS LRBAA reviewers, C-UAS acquisition stakeholders, defense technology evaluators  
**Tone:** professional, confident, technically credible, defense-tech  
**Property of Fratres X AI**  
**GitHub:** https://github.com/FratresMedAI/Ancile-Aeris

## Creative Direction

The video should feel like a polished defense technology demonstration: restrained, operational, and evidence-driven. The story is direct: Ancile Aeris v2.0 builds, launches, publishes live ROS 2 proof, selects layered non-kinetic effectors, and reports clean DARKSPACE audit status.

Core message:

```text
Ancile Aeris v2.0 is a working, auditable, human-governed ROS 2 C-UAS platform with a full layered non-kinetic defeat stack and intelligent cognitive selection.
```

## Exact Timed Shot List

| Time | Shot | Capture | On-Screen Text | Narration |
|---|---|---|---|---|
| 0:00-0:08 | Title slate | Full-screen graphic | "Ancile Aeris v2.0" / "Layered Non-Kinetic C-UAS Defense" | "This is Ancile Aeris v2.0, a working ROS 2 counter-UAS and anti-terror defensive platform." |
| 0:08-0:18 | System identity | Architecture graphic | "Property of Fratres X AI" / "GitHub: FratresMedAI/Ancile-Aeris" | "It is built for auditable, human-governed protection of mass gatherings and critical infrastructure." |
| 0:18-0:32 | Repository proof | GitHub repo or file tree | "Live on GitHub" / "ROS 2 modular packages" | "The platform is integrated and live on GitHub with sensing, fusion, DARKSPACE audit, scout ISR, cognitive EW, and effectors." |
| 0:32-0:50 | Clean launch | Terminal | `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py` | "The LRBAA demo launches the complete basic stack in ROS 2." |
| 0:50-1:08 | Topic proof | Terminal | `ros2 topic list` filtered output | "The live interfaces include DARKSPACE audit, effector planning, cognitive EW, mesh ISR, and fused tracks." |
| 1:08-1:28 | Multi-modal fusion | Terminal + overlay | `/fused_tracks` | "Simulated visual, thermal, acoustic, RF, lidar, and SIGINT-style evidence is fused into machine-readable tracks." |
| 1:28-1:48 | Mesh scout ISR | Terminal + map graphic | `/mesh/mothership_swarm_status` | "The scout mothership layer provides mesh-coordinated ISR and sector awareness." |
| 1:48-2:08 | Safety gate | Terminal | `/safety_gate_status` / "PID >= 0.999" | "Safety gates constrain downstream actions with PID >= 0.999 and human-on-the-loop authority." |
| 2:08-2:30 | DARKSPACE audit | Terminal highlight | `/darkspace/status` / `integrity_ok: true` / `chain_gap_count: 0` | "DARKSPACE audit is clean, with integrity confirmed and zero hash-chain mismatch warnings." |
| 2:30-2:52 | Effector catalog | Graphic + terminal | "HPM | cognitive jamming | GNSS spoofing | takeover | deception | monitor" | "The v2.0 differentiator is the full layered non-kinetic defeat stack." |
| 2:52-3:14 | Selected plan | Terminal | `/effector/selected_plan` | "The effector policy selects a track-specific plan and publishes rationale, authorization state, and monitor-only status." |
| 3:14-3:34 | Cognitive EW | Terminal | `/cognitive_ew_commands` | "The cognitive EW chain turns the plan into an explainable, human-vetted recommendation." |
| 3:34-3:48 | Government alignment | Graphic slate | "DHS PEO UAS/C-UAS | JIATF-401 | Replicator 2" | "Ancile Aeris v2.0 is aligned to DHS C-UAS needs and modular acquisition pathways." |
| 3:48-3:56 | Industry alignment | Graphic slate | "Lattice-style mesh | DroneHunter-class capture | Leonidas-style HPM" | "It references leading integration concepts while remaining vendor-neutral and simulation-safe." |
| 3:56-4:00 | Closing slate | Branded slate | "Ancile Aeris v2.0 - Submission Ready - Property of Fratres X AI" | "Ancile Aeris v2.0: layered, auditable, non-kinetic, and human-governed." |

## Required ROS 2 Commands to Capture

Launch:

```bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

Proof commands in a second terminal:

```bash
ros2 topic list | grep -E 'effector|cognitive_ew|darkspace|audit|mesh|fused_tracks'
ros2 topic echo --once /darkspace/status
ros2 topic echo --once /effector/status
ros2 topic echo --once /effector/selected_plan
ros2 topic echo --once /cognitive_ew_commands
ros2 topic echo --once /mesh/mothership_swarm_status
ros2 topic echo --once /fused_tracks
```

## Fields to Highlight

### `/darkspace/status`

```text
integrity_ok: true
chain_gap_count: 0
```

### `/effector/selected_plan`

```text
selected.mode
selected.family
selected.authorized
selected.monitor_only
xai.rationale
catalog_considered
```

### `/cognitive_ew_commands`

```text
selected_effector_mode
effector_family
xai_rationale
requires_human_authorization
monitor_only
```

### `/mesh/mothership_swarm_status`

```text
coordinated_coverage
members
mesh_quality
```

## Suggested B-Roll and Graphics

- Stadium perimeter and critical infrastructure line art with drone silhouettes.
- Mesh network showing scout mothership nodes and coverage sectors.
- Effector catalog wheel: monitor, deception, cognitive jamming, GNSS/link spoofing, HPM-class denial, control-link takeover.
- DARKSPACE audit shield with "integrity_ok=true."
- Human authorization gate graphic with "Human-on-the-loop."
- GitHub repository and ROS 2 package tree.
- Alignment slate: DHS PEO UAS/C-UAS, JIATF-401 Marketplace, Replicator 2, Anduril Lattice-style mesh, Fortem DroneHunter F700-class, Epirus Leonidas-style HPM.

## Music and Narration

Use a restrained defense-tech bed: low confident pulse, minimal percussion, no alarm sounds, and no aggressive combat cues. Narration should be calm, senior, technical, and evidence-driven. Emphasize verified runtime proof, non-kinetic defeat, human-governed response, and monitor-only behavior unless authorized.

## Closing Slate

Use this exact closing text:

```text
Ancile Aeris v2.0
Layered Non-Kinetic C-UAS Defense
DARKSPACE Clean | Cognitive EW | Mesh Scout ISR | Human-on-the-Loop

Property of Fratres X AI
GitHub: https://github.com/FratresMedAI/Ancile-Aeris

Alignment Context:
DHS PEO UAS/C-UAS | JIATF-401 Marketplace | Replicator 2
Anduril Lattice-style mesh | Fortem DroneHunter F700-class | Epirus Leonidas-style HPM
```

## Standard Disclaimer

Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Production Notes

- Record terminal at 1920x1080 or higher with 125-150 percent font scaling.
- Use two terminal panes: one for launch, one for topic proof.
- Pre-copy proof commands into a notes file to avoid typing delays.
- Keep all terminal evidence readable for PDF/video reviewers.
- Do not show secrets, credentials, or unrelated local paths.
- Keep the standard disclaimer visible in the final slate or closing sequence.

**Ancile Aeris v2.0 - Property of Fratres X AI**
