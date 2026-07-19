# Ancile Aeris Architecture

Module topology for the simulation-first ROS 2 workspace.

```mermaid
flowchart LR
  payloadSelector[payload_selector.yaml] --> bringup[ancile_aeris_bringup]
  bringup --> sensors[ancile_aeris_sensors]
  bringup --> fusion[ancile_aeris_fusion]
  bringup --> safetyGate[ancile_aeris_safety_gate]
  bringup --> cognitiveLayer[ancile_aeris_cognitive]
  sensors --> fusion
  fusion --> fusedTracks[/fused_tracks/]
  fusedTracks --> cognitiveLayer
  safetyGate --> safetyStatus[/safety_gate_status/]
  safetyStatus --> cognitiveLayer
  cognitiveLayer --> audit[/audit/events/]
  cognitiveLayer --> xai[/xai_explanation/]
```

## Node responsibilities

- `ancile_aeris_sensors`: visual, acoustic, and RF sensor stubs
- `ancile_aeris_fusion`: multimodal confidence fusion and `/fused_tracks` publication
- `ancile_aeris_safety_gate`: policy gate state on `/safety_gate_status`
- `ancile_aeris_bringup`: unified launch orchestration for all capabilities
- `ancile_aeris_cognitive/*`: cognitive defensive adjuncts (roadmap + demo-enabled subset)
- `ancile_aeris_darkspace_integration`: audit / immutable hashing spine
- `ancile_aeris_operator_copilot`: operator query interface
- `ancile_aeris_effectors`: non-kinetic-first effector planning (simulation)
- `scout_mothership` + `ancile_aeris_micro_payloads`: FOB swarm + modular micro-payload sim

## Safety invariants

- Human-on-the-loop authority is required for mitigation modeling
- Kinetic / last-resort simulation paths remain **policy-off by default**
- No autonomous weapon release pathway

See also [`COGNITIVE_ARCHITECTURE.md`](COGNITIVE_ARCHITECTURE.md) and the root [`README.md`](../README.md).
