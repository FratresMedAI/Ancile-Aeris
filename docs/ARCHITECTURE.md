# Ancile-Aeris Architecture

```mermaid
flowchart LR
  PS[payload_selector.yaml] --> LS[counterdrone_core full_system launch]
  LS --> CUAS[C-UAS payload]
  LS --> CONS[Conservation payload]
  LS --> GEN[Generic safety payload]
  V[visual_node] --> F[fusion_node]
  A[acoustic_node] --> F
  R[rf_node] --> F
  R --> CY[cyber_node]

  F --> T[trajectory_node]
  F --> C2[c2_decision_node]
  T --> C2
  CY --> C2
  SIM[swarm_sim_node] --> C2

  C2 --> TH[/threats/]
  C2 --> EC[/effector_commands/]
  C2 --> AU[/audit/events/]

  F --> DB[dashboard_bridge_node]
  TH --> DB
  EC --> DB
  AU --> DB
  DB --> DS[/dashboard/state/]
  DS --> ST[Streamlit UI]
  GEN --> AU
  CONS --> F
```

## Node Responsibilities

- `sensor_nodes`: visual/acoustic/rf observations
- `fusion_node`: confidence voting + EKF-style fused tracks
- `trajectory_node`: short-horizon trajectory projection
- `cyber_node`: passive identity/fingerprint assessment
- `swarm_sim_node`: simulation swarm tracks + RL recommendations
- `c2_decision_node`: threat scoring, ROE gating, command and audit generation
- `dashboard_node`: state aggregation and operator display

## Payload Profiles

- `cuas`: full defensive C-UAS launch graph.
- `conservation`: conservation and anti-poaching node set with shared monitor-safe governance.
- `generic`: safety, fusion, audit, and dashboard baseline for cross-domain T&E.

## Deployment Modes

- `sim_mode=true`: simulation-safe test mode for all payloads.
- `sim_mode=false`: non-monitor outputs remain constrained by operator and safety guardrails.
