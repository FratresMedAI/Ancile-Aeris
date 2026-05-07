# Ancile Aeris — LRBAA BORAP 04 Concept Paper (Pure C-UAS / Anti-Terror)

**Ancile Aeris — Property of Fratres X AI**

## Executive Summary

Ancile Aeris is a simulation-first ROS 2 defensive stack for counter-UAS and anti-terror perimeter security at mass gatherings and critical infrastructure. The platform combines multi-modal sensing stubs, deterministic fusion, DARKSPACE-class audit emission, PID >= 0.999 safety gates, causal explainability, and strict human-on-the-loop decision control.

The architecture includes mesh-capable mothership ISR and optional baby interceptor simulation, where high-consequence actions remain blocked unless human approvals are present.

## Layered Defense and Government Integration Context

Ancile Aeris is positioned as a modular integration layer aligned to the **DHS Program Executive Office for UAS/C-UAS** mission profile. Integration references include:
- **Anduril Lattice** for mesh-enabled situational awareness analogs.
- **JIATF-401 Marketplace** for interoperable acquisition and vendor integration pathways.
- **Fortem DroneHunter F700** class capture concepts for low-collateral interdiction narratives.
- **Epirus Leonidas** style non-kinetic effect narratives under human command authority.
- **Replicator 2** style rapid fielding and iterative deployment posture.

## Technical Differentiators

1. **Mesh Mothership ISR:** coordinated coverage and heartbeat awareness across multiple mothership instances.
2. **Fusion + Safety Gate:** `/fused_tracks` feeds PID-gated decision pathways with auditable context.
3. **DARKSPACE Audit:** immutable `/audit/events` trail for oversight and after-action review.
4. **Human Authorization:** optional interceptor path requires double human authorization when configured.
5. **Layered Non-Kinetic Defeat Stack:** `ancile_aeris_effectors` simulates an escalating, human-gated effector catalog: multi-sensor deception, cognitive jamming, GNSS/link spoofing, HPM-class denial, and authorized cyber takeover of recovered control links. Selection runs through the cognitive layer (`agent_orchestrator` -> `digital_twin` -> `cognitive_ew`), surfaces XAI rationale on `/cognitive_ew_commands`, and remains monitor-only unless the safety gate is open.

## Lethally Effective Layered Defeat (Simulation-Safe)

Ancile Aeris models a *layered defeat* doctrine that prefers non-kinetic, low-collateral options first and only escalates when score and authorization warrant it. Every effector in the catalog publishes an explainable plan (`/effector/selected_plan`) and is forced to monitor-only when the safety gate is closed; takeover-class effects additionally require dual operator authorization. This delivers a credible, lethally effective defeat narrative for mass-gathering and critical-infrastructure C-UAS *without* embedding any unlawful autonomous engagement in the codebase.

## 2026 Security Relevance

Ancile Aeris supports event-security rehearsals for **FIFA 2026** and **America 250** in simulation mode, emphasizing lawful, defensive, and auditable C-UAS operations.

**Ancile Aeris — Property of Fratres X AI**

