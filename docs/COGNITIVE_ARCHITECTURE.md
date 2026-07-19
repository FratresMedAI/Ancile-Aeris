# ClearSky OS Cognitive Architecture

Adjunct modules for the ClearSky OS ROS 2 workspace. Company context: [fratres-x.com](https://fratres-x.com).

## Overview

ClearSky OS layers perception, fusion, trust, and operator decision support. Cognitive packages extend that core with research adapters — many are roadmap shells until physics models or trained components are wired in.

## Layered architecture

1. **Perception** — visual, thermal, acoustic, RF (and related) adapters feed fusion  
2. **Fusion** — `clearsky_os_fusion` publishes `/fused_tracks`  
3. **Trust** — audit spine + safety gates record and block unsafe paths  
4. **Operator support** — `clearsky_os_operator_copilot` query path  
5. **Coordination** — scout / micro-payload simulation and effector planning (policy-gated)

## Safety foundation

- Hash-chained audit events  
- Safety gate (confidence + human veto + IFF + twin veto)  
- Kinetic / last-resort paths **off by default**  
- No autonomous weapon release pathway  

## Core bringup set

- `clearsky_os_bringup`
- `clearsky_os_darkspace_integration`
- `clearsky_os_fusion`
- `clearsky_os_integration`
- `clearsky_os_interfaces`
- `clearsky_os_operator_copilot`
- `clearsky_os_safety_gate`
- `clearsky_os_sensor_resilience`
- `clearsky_os_sensors`
- `clearsky_os_swarm_intent`
- `clearsky_os_scout_mothership`
- `clearsky_os_effectors`
- `clearsky_os_micro_payloads`

## Roadmap modules

Enable progressively after build, launch, audit, and safety-gate validation:

- Agent orchestration and adversarial defense  
- Cognitive EW and digital twin  
- Causal XAI, verification, and video analytics  
- Federated and continual learning  
- Defensive swarm coordination  
- Zero-knowledge threat sharing  
- Resilient PNT and generative red teaming  
- Neuromorphic and hyperspectral perception stubs  

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the data-flow diagram.
