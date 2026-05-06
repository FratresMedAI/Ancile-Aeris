# Ancile Aeris — Four-Minute Demo Video Script & Storyboard (Mesh Mothership CT Focus)

**Ancile Aeris — Property of Fratres X AI**

| Time | Narration | Visual / Shot |
|---|---|---|
| **0:00–0:25** | “Ancile Aeris is Fratres X AI’s ROS 2 counter-UAS shield—mesh-aware, audit-heavy, and laser-focused on homeland mass-gathering plus critical infrastructure defense. Human operators stay in charge; this is not an autonomous kill suite.” | Title plates with DHS Program Executive Office for UAS/C-UAS iconography (stylized only) + quick montage of Lattice + DroneHunter + Leonidas name callouts as **reference systems**, not endorsements. |
| **0:25–0:55** | “One launch command boots the BORAP-ready slice: sensing, fusion, DARKSPACE hooks, PID safety gate, mesh mothership overlays, and operator copilot—all aligned to Replicator 2-style speed-to-field thinking.” | Terminal: `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`; `ros2 node list` emphasizing `scout_mothership` + `fusion`. |
| **0:55–1:35** | “Fusion JSON on `/fused_tracks` preserves track ID, velocity, confidence, and now **counter-terror arson precursor** simulation fields—clearly tagged as sim so evaluators know it is a defensive classifier stub, not a kinetic order.” | Split panes: `ros2 topic echo /fused_tracks` highlighting `counterterror_threat_signals`. |
| **1:35–2:10** | “Our mesh mothership channel mirrors Anduril Lattice-style situational awareness—each platform reports coordinated sectors, peer heartbeats, redundancy, and latency budgets on `/mesh/mothership_swarm_status`.” | Echo `/mesh/mothership_swarm_status`; optional second terminal showing `ros2 topic pub` once on `/mesh/mothership_peers/heartbeat` JSON to light up peer table. |
| **2:10–2:45** | “Every mesh or fusion event can be replayed in `/audit/events`; DARKSPACE philosophy means no ghost data—blocked actions get the same treatment as detections.” | Scrolling audit stream; highlight `mesh_swarm_publish`. |
| **2:45–3:15** | “PID gates at 0.999 keep high-consequence narratives honest; operators see `/safety_gate_status` before anything downstream even pretends to cue a DroneHunter catch team or Leonidas-style HPM mission.” | Annotated JSON with `allow:false` vs `allow:true` hypothetical. |
| **3:15–3:45** | “Copilot `QueryCopilot` services answer bounded questions so JIATF-401 integrators can graft policy text without inventing capabilities.” | Service list + sample call to `/ancile_aeris_operator_copilot/query`. |
| **3:45–4:00** | “Optional interceptor simulation demonstrates double-human consent—just like cautious employment of attritable catch assets; default remains off for safe demos.” | Launch clip with `enable_baby_interceptor:=true`; show `/interceptor_status` hold state; closing slate “Ancile Aeris — Property of Fratres X AI”. |

**Production note:** When narrating **Fortem DroneHunter F700**, **Epirus Leonidas**, **Anduril Lattice**, **JIATF-401 Marketplace**, **Replicator 2**, and **DHS Program Executive Office for UAS/C-UAS**, treat them as **credibility references** for integration storytelling—on-screen disclaimer: *simulation only; not government endorsement.*

**Ancile Aeris — Property of Fratres X AI**
