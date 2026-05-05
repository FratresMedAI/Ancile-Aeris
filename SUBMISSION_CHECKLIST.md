# LRBAA Submission Checklist (BORAP 04)

## Topic Metadata Block

- Topic Number: BORAP 04
- Topic Title: Countering Unmanned Aircraft Systems
- Solicitation: DHSST-LRBAA 24-01
- Research Types: Type II and Type III
- Mission Area: Secure U.S. Borders and Approaches
- Open Date: 6/18/2024, 1:00:00 PM EDT
- Close Date: 5/31/2029, 11:59:59 PM EDT
- Registration Deadline: 5/31/2029, 11:59:59 PM EDT
- SAM.gov Notice: https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view

## 3-Page Concept Paper Outline

1. Problem and mission relevance to BORAP 04 objective.
2. Technical approach for detect, track, identify, and mitigation workflows.
3. Innovation and differentiators versus baseline approaches.
4. Operational transition path for DHS users and T&E readiness.
5. Cost reasonableness and milestone framing.

## Quad Chart Checklist

- Project title.
- DHS impact and mission fit.
- Technical approach graphic and key capabilities.
- Cost and milestones.

Template placeholder: `artifacts/quad_chart/quad_chart_template.md`

## Optional Demo Video Checklist (<=4 minutes)

- Non-proprietary and unclassified.
- Simulation mode only.
- Shows dense-urban and mass-gathering detect/track/fusion flow.
- Includes operator safety gates and audit/XAI visibility.
- Hosted as unlisted YouTube link in submission packet.

Video placeholder: `artifacts/demo_video/demo_video_notes.md`

## Cognitive Defensive Shield v2.0 Evidence

- Positioning language:
  - Ancile Aeris 2.0 is a Cognitive Autonomous Defensive Shield for DHS/DoD rapid prototyping audiences, including JIATF-401-style C-UAS experimentation.
  - It combines neuromorphic perception, adversarial resilience, agentic multi-agent C2, cognitive EW recommendations, digital-twin what-if simulation, federated learning hooks, and verifiable safety.
  - It also includes causal XAI, constrained continual learning, defensive swarm coordination, privacy-preserving interagency threat sharing, resilient PNT, and generative red-team simulation.
  - It remains defensive-only, human-on-the-loop, XAI-first, and immutable-audit-ready.
- Include simulation outputs for:
  - `agent_orchestrator` proposed actions with monitor-safe fallback behavior.
  - `adversarial_defense` sensor health and spoof/anomaly alerts.
  - `digital_twin` effectiveness and collateral risk outputs (<200 ms target).
  - `cognitive_ew` adaptive RF strategy recommendation stubs.
  - `federated_learning` model update service acceptance/rejection traces.
  - `causal_xai` counterfactual explanation traces for operator and reviewer trust.
  - `continual_learning` bounded-update status with safety-lock behavior.
  - `defensive_swarm_coordinator` recommendation-only friendly swarm plans.
  - `zero_knowledge_sharing` privacy-tiered threat intel sharing traces.
  - `resilient_pnt` GNSS-denied fallback navigation estimates.
  - `generative_red_team` synthetic future threat scenario generation.
  - `verification` runtime safety violations and verified action evidence.
  - `neuromorphic_sim` event stream outputs.
  - Supporting package traces from `video_analytics`, `swarm_orchestrator`, and `copilot`.
- Attach report: `reports/borap04_urban_mass_gathering_report.json`.
- Generate report locally with: `python scripts/demo_borap04_urban_mass_gathering.py`.

## Portal Submission Flow

- Submit initial 3-page concept plus quad chart and optional video to DHS S&T LRBAA portal.
- Wait for invitation before virtual pitch.
- Wait for second invitation before full written proposal.

## Compliance Guardrails

- No offensive autonomous kill-chain content.
- Non-monitor outputs are recommendations requiring human authorization and final safety-gate approval.
- No classified or controlled sensitive data.
- No unreleasable hardware details in public artifacts.
