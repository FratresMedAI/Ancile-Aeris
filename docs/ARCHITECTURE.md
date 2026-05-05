# Ancile Aeris Architecture`r`n`r`n**Property of Fratres X AI**

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

## Node Responsibilities

- `ancile_aeris_sensors`: visual, acoustic, and RF sensor stubs
- `ancile_aeris_fusion`: multimodal confidence fusion and `/fused_tracks` publication
- `ancile_aeris_safety_gate`: policy gate state on `/safety_gate_status`
- `ancile_aeris_bringup`: unified launch orchestration for all capabilities
- `ancile_aeris_cognitive/*`: 21-capability cognitive defensive stack

