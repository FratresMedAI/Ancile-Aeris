Revised May 8, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.0 Video Production Package

**Solicitation line for packaging:** DHS S&T LRBAA 24-01 (**DHS_ST_LRBAA_24-01** · SAM.gov) · BORAP 04 Countering Unmanned Aircraft Systems · https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view  
**Runtime:** 4:00  
**Audience:** DHS LRBAA reviewers; C‑UAS acquisition stakeholders; lab integrators  
**Tone:** restrained, credible, technically precise—no kinetic-forward hero framing  
**Property of Fratres X AI • GitHub:** https://github.com/FratresMedAI/Ancile-Aeris  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

Narrative weighting: roughly **ninety percent** non-kinetic software (fusion • audit • mesh ISR • effector modeling • cognitive XAI). **`baby_interceptor`** is **simulation-only**, **disabled by default**, **optional**, and requires **paired human approvals**—relegate to a footnote-tier beat, never hero visuals.

## Creative Direction

The piece should resemble a disciplined engineering walkthrough—not a kinetic weapons trailer. Ancile Aeris **builds, launches instrumented ROS 2 nodes, emits auditable telemetry, executes layered non-kinetic defeat modeling, and verifies DARKSPACE hash integrity** strictly inside simulation envelopes.

Anchor message:

```text
BORAP‑04‑responsive ROS 2 C‑UAS software prototype:
layered non-kinetic modeling + advanced layered response logic,
human authority preserved,
open buses for future RF/sensor integrations.
```

## Exact Timed Shot List

| Time | Shot | Capture | On‑Screen Text | Narration gist |
|---|---|---|---|---|
| 0:00–0:07 | Opening slate | Branded PNG | BORAP 04 • Simulation Only | Solicitation responsiveness + honesty about sim fence. |
| 0:07–0:18 | Identity card | Typography | Fratres X AI • Repo URL | Organizational credibility / GitHub linkage. |
| 0:18–0:32 | Repository proof | Browser / tree | Modular ROS 2 packages | Non‑kinetic stack emphasis. |
| 0:32–0:50 | Launch | Terminal fullscreen | ros2 launch ... `ancile_aeris_basic_demo` | Clean deterministic spin‑up. |
| 0:50–1:08 | Interfaces | ros2 topic list filter | fused_tracks • effector • cognitive_ew • darkspace • mesh • audit | Topology proof. |
| 1:08–1:30 | Fusion | Echo `/fused_tracks` | Synthetic detect/track path | Mention optional metrics footnote (**N≈500**, ~**94 % correlation**, confidence **>0.88**) — **representative synth eval, not OT&E**. |
| 1:30–1:50 | Mesh ISR | Echo mesh topics | ISR overlay analogy | Lattice-style wording optional; **no vendor endorsement**. |
| 1:50–2:08 | PID gate | `/safety_gate_status` | PID ≥ 0.999 | Mitigation gated by authority. |
| 2:08–2:30 | DARKSPACE | Echo `/darkspace/status` | `integrity_ok:true` banner | Oversight storyline. |
| 2:30–2:55 | Catalog | Animated wheel | HPM stub • spoof • deception • EW • takeover concept | Repeated **STUB / SIM** tags. |
| 2:55–3:15 | Planner | Echo `/effector/selected_plan` | XAI rationale • monitor_only | Advanced layered response modeling narrative. |
| 3:15–3:34 | Cognitive | Echo `/cognitive_ew_commands` | Human-vetted output | Chain closure. |
| 3:34–3:44 | Optional footnote | Static lower third | **`baby_interceptor` sim • default OFF • dual auth** | One calm sentence-only beat. |
| 3:44–3:55 | Transition slate | Typography | ROS 2 open interfaces • SDR lab TRL-6 glidepath (~18 mo) • Phase I illustrative **$250k–$350k** • JIATF-401 context | Procurement realism without contracts claim. |
| 3:55–4:00 | Closing | Slate + QR | Disclaimer verbatim | Confidence without hype. |

## Required ROS 2 Commands to Capture

```bash
cd /opt/ancile_aeris_ws
source /opt/ros/kilted/setup.bash
source install/setup.bash
ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py
```

Secondary terminal:

```bash
ros2 topic list | grep -E 'effector|cognitive_ew|darkspace|audit|mesh|fused_tracks'
ros2 topic echo --once /darkspace/status
ros2 topic echo --once /effector/status
ros2 topic echo --once /effector/selected_plan
ros2 topic echo --once /cognitive_ew_commands
ros2 topic echo --once /mesh/mothership_swarm_status
ros2 topic echo --once /fused_tracks
```

## Telemetry Highlight Fields

Use the same selective JSON keys already documented internally (`selected.mode`, rationale, authorization booleans).

## B‑Roll / Graphics Guidance

- Line art silhouettes permissible (arenas • bridges)—no explosions.  
- Mesh coverage schematic; ROS topic graph overlays.  
- Effector graphic wheel emphasises **non‑kinetic** segments; kinetic capture iconography absent.  
- **Optional**: tiny footnote badge if `baby_interceptor` wording appears—muted grey typography only.  
- Replace legacy alignment board listing DroneHunter capture marketing with roadmap board (SDR insertion, ROS contracts, Marketplace context). Lattice / Leonidas citations only as **architecture analogues or HPM modeling language**, per disclaimer.

## Music & Narration

Low dynamic range bed; narration mid‑cadence Midwest neutral accent acceptable; forbid triumphal kinetic scoring.

## Closing Slate (may adapt layout but preserve disclaimer verbatim)

```text
Ancile Aeris v2.0 • BORAP 04
Layered non-kinetic modeling | Audited ROS 2 stack

Property of Fratres X AI
https://github.com/FratresMedAI/Ancile-Aeris

Simulation-only C-UAS defensive demonstration. No autonomous weapon release.
Government and industry references are alignment examples only and do not imply endorsement.
```

## Production Notes

- Font scale 125‑150 % terminal capture. Sanitize filesystem paths containing usernames before record.  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

**Ancile Aeris v2.0 - Property of Fratres X AI**
