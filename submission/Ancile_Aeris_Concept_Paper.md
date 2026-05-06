# Ancile Aeris: Cognitive Layered Defensive Shield for Counter-UAS

**Ancile Aeris - Property of Fratres X AI**

## Executive Summary

Ancile Aeris is a simulation-first ROS 2 defensive shield for counter-unmanned aircraft systems (C-UAS), built to help operators detect, understand, audit, and safely respond to drone activity around dense public events, critical infrastructure, and conservation terrain. The current v2.0 basic demo launches a working baseline stack: multi-modal sensing, fused tracks, DARKSPACE audit, a safety gate, a high-altitude scout mothership simulator, and an operator copilot.

The system is designed around a 21-capability architecture, but it does not depend on all capabilities being active at once. Its core value is the disciplined integration model: every capability is modular, every recommendation is explainable, every event is auditable, and any simulated action path remains blocked behind human-on-the-loop controls.

## Technical Approach

Ancile Aeris uses ROS 2 Kilted packages to create a layered defensive pipeline. Sensor simulation nodes publish visual, thermal, RF, acoustic, LiDAR, and SIGINT observations. The fusion node produces `/fused_tracks` with confidence, class labels, and PID-gate metadata. DARKSPACE audit records material events through `/audit/events` and HMAC-style audit hooks. The safety gate publishes `/safety_gate_status`, enforcing human veto, IFF, and risk controls before downstream action nodes can progress.

The high-altitude scout mothership adds a persistent ISR layer. It publishes simulation-safe ISR overlays to `/fused_tracks` and `/scout_eyes`, including position, altitude, sensor type, and confidence. Optional baby interceptor simulation consumes `/interceptor_handoff` and publishes `/interceptor_status`; it never claims autonomous deployment and remains blocked unless the safety gate, launch authorization, and terminal authorization are all true.

## Operational Impact

The platform targets the operational gap between raw drone sensing and accountable human decision-making. Event security teams need a way to distinguish ambiguous commercial drone activity from coordinated threats, preserve audit trails, and explain why a response was recommended or blocked. Ancile Aeris provides that operational layer.

Near-term mission examples include 2026 event security support for FIFA-related venues, America250 gatherings, stadium perimeters, utility corridors, and emergency response sites. The same architecture supports conservation and wildlife protection missions: scout ISR can identify poaching patterns, fused sensing can monitor protected corridors, and the copilot can support ranger decision-making without changing the safety model.

## Trust & Safety Architecture

Ancile Aeris is defensive-only and human-on-the-loop by design. It does not implement autonomous kill-chain behavior. The safety gate is the system boundary for high-consequence recommendations, and DARKSPACE audit records both positive and negative decisions.

Trust features include:

- DARKSPACE immutable audit events for fusion updates, scout handoffs, copilot responses, and interceptor simulation results.
- Explainable AI text on material recommendations and blocked paths.
- Explicit human veto, launch authorization, and terminal authorization state.
- Payload selector controls that allow capabilities to be disabled for safe demonstrations.
- Simulation-only interceptor status, with zero collateral-risk claims unless authorization gates are satisfied.

## Path to Deployment

The v2.0 demo is ready for LRBAA BORAP 04 review as a credible technical baseline. The next deployment milestones are sensor adapters, formal message definitions for selected JSON topics, hardware-in-the-loop testing, audit database hardening, and operator UI workflows. The roadmap keeps the 21-capability vision intact while allowing disciplined increments: validate the baseline, add cognitive EW and digital twin stubs, expand XAI, then integrate selected field sensors under the same safety and audit model.

Ancile Aeris is positioned as a serious defensive systems foundation: modular, auditable, explainable, and safe to demonstrate.

**Ancile Aeris - Property of Fratres X AI**
