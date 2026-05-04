# Ancile-Aeris

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

## Next-Gen Cognitive Layer

Ancile-Aeris now includes additive BORAP-oriented modules under `src/`:
- `video_analytics_node`: video-as-a-sensor enrichment and behavior tags.
- `swarm_intent_node`: collective-intent assessment and layered recommendation outputs.
- `operator_copilot_node`: offline query service for operator summaries (`template` or optional `ollama` backend).
- `sensor_resilience_node`: cross-modal anomaly alerts for contested sensing environments.

These modules remain simulation-safe and feed existing hard safety gates, XAI outputs, and immutable audit pathways.

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
- `docs/TESTING.md`
- `SUBMISSION_CHECKLIST.md`
