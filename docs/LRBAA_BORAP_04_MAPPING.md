# LRBAA BORAP 04 Mapping

## Solicitation Metadata

- Topic Number: BORAP 04
- Topic Title: Countering Unmanned Aircraft Systems
- Solicitation: DHSST-LRBAA 24-01
- Research Type: Type II and Type III
- Mission Area: Secure U.S. Borders and Approaches
- SAM.gov Notice: https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view

## Objective Keywords To Capability Mapping

- `detect`: `sensor_nodes` visual/acoustic/rf ingest and `fusion_node`.
- `detect` (video enhanced): `video_analytics_node` overlays EO/IR-style analytics on visual tracks.
- `track`: `fusion_node` fused tracks and `trajectory_node` prediction.
- `identify` and `classify`: `cyber_node` identity assessment and C2 threat classification.
- `mitigation`: `c2_decision_node` monitor/jam/spoof recommendation with hard safety gates.
- `sensor` and `situational awareness`: dashboard bridge and Streamlit dashboard state views.
- `analysis` and `data analytics`: fused confidence scoring, trajectory estimates, and scenario reports.
- `test & evaluation` and `forensics`: soldier safety and conservation scenario outputs plus immutable audit logs.
- `security`: DARKSPACE-derived stateless rule guard screens operator text and tool traces for injection, exfiltration, and unsafe override patterns.
- `critical infrastructure`, `securing aviation`, `securing borders`, `border protection`: scenario labels and mission templates in payload selector and reports.
- `autonomous-but-vetted response`: `swarm_intent_node` recommendations are advisory and remain constrained by C2 human authorization and veto gates.

## BORAP 04 Environmental Conditions

- Dense urban environments: monitor-safe gating prevents unsafe non-monitor actions in high-collision contexts.
- Mass gatherings: digital-twin and operator authorization enforce conservative intervention.
- Critical infrastructure: PID and identity gates reduce false-positive escalation.
- Mobile platforms: payload selector supports portable profile switching at launch.
- Remote terrain: conservation payload reuses detect/track analytics in low-connectivity workflows.

## Keyword Coverage Checklist

- Algorithms: weighted fusion + ROE logic + policy-assisted selection.
- Analysis/Data Analytics: confidence scoring, track state, trajectory projection.
- Detect/Track/UAS: multimodal detection and fused tracking pipeline.
- Classify/Forensics: identity disposition and auditable decision traces.
- Mitigation/Prevention/Preventing Terrorism/Security: monitor-first ROE, human authorization, IFF and digital twin vetoes.
- Test & Evaluation: documented simulation scenarios and reproducible report generation.
- Swarm and intent analysis: `swarm_intent_node` with non-kinetic layered recommendations.
- Human-machine teaming: `operator_copilot_node` plus dashboard copilot panel for auditable operator queries.
- Sensor resilience: `sensor_resilience_node` cross-modal mismatch alerts for degraded or spoofed inputs.
