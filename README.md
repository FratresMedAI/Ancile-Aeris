<p align="center">
  <img src="assets/ancile-aeris-logo.png" alt="Ancile-Aeris logo" width="480"/>
</p>

# Ancile Aeris 2.0

## Cognitive Autonomous Defensive Shield with Neuromorphic Perception, Agentic Multi-Agent C2, and Verifiable Trust

Ancile-Aeris unifies CounterDroneOS and EcoSentinel (Naturaii X) as a single defensive, simulation-first ROS 2 Kilted platform.

## BORAP 04 Objective Alignment

The BORAP 04 objective is to "develop enhanced technologies and methods that allow for the detection, tracking, identification, and mitigation of unmanned aircraft systems under varied terrains and environmental conditions."

Ancile-Aeris explicitly validates these conditions:
- dense urban environments
- mass gatherings
- critical infrastructure
- mobile platforms
- remote terrain

## Payload Architecture

- `payloads/cuas`: C-UAS detection, fusion, and C2 defensive workflows.
- `payloads/conservation`: EcoSentinel conservation and anti-poaching derived workflows.
- `payloads/generic`: shared safety, explainability, and immutable audit components.
- `payloads/generic/darkspace_rule_guard.py`: DARKSPACE-derived offline safeguard classifier for prompt/tool trace abuse signals.
- `config/payload_selector.yaml`: runtime payload profile selector.

## Cognitive Autonomous Defensive Shield v2.0

Ancile-Aeris now includes a full v2.0 skeleton under `src/ancile_aeris_cognitive/` organized into Perception, Cognition, Decision, Action/Resilience, and Verification/Trust layers:
- Perception: `video_analytics`, `neuromorphic_sim`, and uncertainty-aware `fusion_node` ingestion.
- Cognition: `adversarial_defense`, `agent_orchestrator`, and `cognitive_ew`.
- Decision: `digital_twin` and `swarm_orchestrator`.
- Action/Resilience: `copilot` and `federated_learning`.
- Verification/Trust: `verification`, immutable audit hooks, XAI outputs, and final hard gating through the existing safety gate.

All actionable outputs remain safety-gated, monitor-safe by default, and audit-friendly.

## Max-Defensive Safety Gates

- PID gate `>= 0.999` with required multi-modal evidence before any non-monitor action.
- Human-on-the-loop authorization for non-monitor commands.
- Friendly IFF veto and digital-twin veto for soldier-safety preservation.
- Immutable HMAC hash-chain audit events on `/audit/events`.
- XAI decision outputs on `/xai_explanation`.
- No offensive autonomous kill-chain behavior.

## Quick Start

```bash
docker compose -f docker/docker-compose.yml build ancile-aeris
docker compose -f docker/docker-compose.yml up ancile-aeris
```

Or with PowerShell payload selection:

```powershell
./scripts/run_all.ps1 -Payload cuas -SimMode true
```

## Documentation

- `docs/LRBAA_BORAP_04_MAPPING.md`
- `docs/ARCHITECTURE.md`
- `docs/COGNITIVE_ARCHITECTURE.md`
- `docs/TESTING.md`
- `SUBMISSION_CHECKLIST.md`
