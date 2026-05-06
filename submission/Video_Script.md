# Ancile Aeris Four-Minute Demo Script

**Ancile Aeris - Property of Fratres X AI**

## 0:00-0:20 - Title and Mission

**Visual:** Title card: "Ancile Aeris: Cognitive Layered Defensive Shield for Counter-UAS." Background: subdued event security / conservation imagery.

**Narration:** "Ancile Aeris is Fratres X AI's simulation-first defensive shield for counter-UAS operations. It combines sensing, fusion, DARKSPACE audit, safety gates, scout ISR, and an operator copilot under strict human-on-the-loop control."

## 0:20-0:50 - One-Command Launch

**Visual:** Terminal runs `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`. Show nodes initializing.

**Narration:** "The v2.0 basic demo launches with one ROS 2 command. Core packages start together: sensors, fusion, DARKSPACE audit, safety gate, scout mothership, and operator copilot."

## 0:50-1:25 - Fused Tracks

**Visual:** `ros2 topic echo /fused_tracks` showing fused JSON and scout overlay tracks with position, altitude, sensor type, and confidence.

**Narration:** "Sensor stubs feed a fusion node that publishes live tracks. The scout mothership adds high-altitude ISR overlays, including altitude and sensor provenance, while avoiding feedback loops."

## 1:25-1:55 - DARKSPACE Audit

**Visual:** `ros2 topic echo /audit/events` or DARKSPACE log view with fusion, scout handoff, and safety events.

**Narration:** "DARKSPACE records material events for traceability. This creates a defensible record of what the system observed, recommended, blocked, or escalated."

## 1:55-2:25 - Safety Gate Veto

**Visual:** `ros2 topic echo /safety_gate_status`; show the gate blocking action until confidence, IFF, veto, and human controls are satisfied.

**Narration:** "Ancile Aeris is defensive-only. The safety gate blocks high-consequence actions unless evidence and human authorization are present. The architecture is designed to prevent autonomous kill-chain behavior."

## 2:25-2:55 - Copilot Response

**Visual:** `ros2 service list` showing `/ancile_aeris_operator_copilot/query`; optional service call or UI capture of a guarded answer.

**Narration:** "The operator copilot helps summarize system state, explain why a track is blocked or escalated, and keep the human operator in control."

## 2:55-3:30 - Optional Interceptor Simulator

**Visual:** Show `enable_baby_interceptor:=true` as an optional launch argument, then `/interceptor_status` holding pending authorization.

**Narration:** "The baby interceptor path is simulation-only and disabled by default. Even when enabled, it requires safety gate clearance, launch authorization, and terminal authorization before reporting a simulated result."

## 3:30-4:00 - LRBAA Close

**Visual:** Architecture diagram or package list, then closing card.

**Narration:** "Ancile Aeris provides a credible baseline for LRBAA BORAP 04: modular, auditable, explainable, and safe to demonstrate. It is ready for rapid iteration toward field adapters, hardware-in-the-loop testing, and operator workflow validation."

**Ancile Aeris - Property of Fratres X AI**
