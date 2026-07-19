Revised May 8, 2026 – Final LRBAA Submission Version

# Ancile Aeris v2.1 Quad Chart

**Solicitation:** DHS S&T LRBAA **24-01** (**DHS_ST_LRBAA_24-01** · [SAM.gov](https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view)) · **BORAP 04 — Countering UAS · Type II / III**  
**LRBAA Counter-UAS / Anti-Terror Defensive System**  
**Property of Fratres X AI**  
**GitHub:** https://github.com/Fratres-X-AI/Ancile-Aeris  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Quad Chart Layout

Use a four-quadrant PDF layout:

| Topic box | LRBAA 24-01 (Notice DHS_ST_LRBAA_24-01) • BORAP 04 Countering UAS • Type II/III • detect/track/identify/mitigate • urban • mass gatherings • critical infrastructure • borders/perimeters |
|-----------|-------------------------------------------------------------------------------------------------------------|
| Technical Approach *(Q1)* | Innovation *(Q2)* |
| **Team *(Q3)*** | **Impact *(Q4)*** |

| Technical Approach | Innovation |
|---|---|
| ROS 2 stack: fused tracks, PID ≥ 0.999 gates, **2–4 mothership FOB swarm** (`/mesh/fob_status`, `/payload/micro_deployment`), modular micro-payload simulation, DARKSPACE, cognitive EW → **non-kinetic-first** `ancile_aeris_effectors` (optional `kamikaze_ram` kinetic sim **last resort**, off by default). Current **TRL 3–4** sim prototype → **Phase I target TRL 5**. | Layered non-kinetic defeat capability with **advanced layered response modeling** (XAI, monitor-only posture until authorized); **representative synthetic evaluation:** ~94% fused-track correlation and effector-selection confidence greater than **0.88** across **N=500** swarm-style scenarios (**not operational T&E**). |
| **Team** | **Impact** |
| Fratres X AI is **a specialized software-defined defense team with deep ROS 2 and cognitive systems expertise, delivering modular, auditable prototypes for federal acquisition pathways.** Verified GitHub/colcon demos. Optional legacy `baby_interceptor`: **simulation-only, not in default demo.** | BORAP 04 pillars anchored in software; humane oversight; ROS 2 open interfaces and **JIATF-401 Marketplace** transition path; **~18‑month** SDR lab path toward **TRL 6** RF bench integration—not fielded kinetic release. |

## Quadrant 1 - Technical Approach

Ancile Aeris v2.1 shows end-to-end C-UAS *software integration*:

- Detect / track via multi-modal inputs → **`/fused_tracks`**.
- Identify / enrich fused records for operator adjudication workflows.
- Mitigate conceptually via **non-kinetic-first** policy + cognitive chain (simulation stubs only); **`kamikaze_ram`** kinetic sim exists only as explicit-policy last resort.
- **FOB swarm:** **`/mesh/fob_status`**, **`/payload/micro_deployment`** (advisory, simulation).
- Mesh ISR: **`/scout_eyes`**, **`/mesh/mothership_swarm_status`**, heartbeats.
- Audit: **`/audit/events`**, **`/darkspace/status`** (`integrity_ok: true`; `chain_gap_count: 0` verified demo).
- Human-on-the-loop: monitor-only absent authorization.

### TRL / cost snapshot (Phase I sizing)

**Current TRL 3–4** · Target **TRL 5** post–Phase I · **Phase I $250k–$350k** (indicative range) · **18-month** plan toward **TRL 6** SDR lab integration.

**Visual:** `Sensors → Fusion → PID Gate → FOB Swarm / Mesh ISR → Non-Kinetic Effectors → (optional gated kinetic sim) → Cognitive EW → DARKSPACE/XAI`

## Quadrant 2 - Innovation

Layered catalog: **`non-kinetic-first`** in default configuration—`monitor`, `multi_sensor_deception`, `cognitive_jamming`, `gnss_link_spoofing`, `hpm_denial_stub`, `control_link_takeover` (dual-auth); optional **`kamikaze_ram`** kinetic-energy simulation **last resort** when kinetic family is enabled in policy (not default).

Selection path: `agent_orchestrator → digital_twin → cognitive_ew` with published rationale on `/effector/selected_plan` and `/cognitive_ew_commands`. This delivers **layered non-kinetic defeat capability** with measured, auditable operator visibility—**not** autonomous engagement.

**Visual:** effector wheel + DARKSPACE/XAI assurance ring.

## Quadrant 3 - Team

- https://github.com/Fratres-X-AI/Ancile-Aeris  
- `colcon build --symlink-install --packages-up-to ancile_aeris_bringup`  
- `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py`  
- Clean DARKSPACE verification run captured in submission materials.

## Quadrant 4 - Impact

| Area | Value |
|------|--------|
| **BORAP mapping** | Software-first **detect / track / ID / mitigate** across challenging environments. |
| **Non-kinetic** | Primary narrative: HPM *stub*, jamming / spoof / deception *models*, authorized takeover *concept*. |
| **Oversight** | Hash-chained audit + XAI text for analytics / forensics-style review. |
| **Integration** | Open ROS 2 topics; **SDR follow-on**; **JIATF-401** listing vision. |
| **Interoperability** | Lattice-style mesh analog; Fortem DroneHunter wording **reference-only, not integrated**; Leonidas phrasing limited to HPM **stub** only. |

**Verified-demo callouts:** `/darkspace/status` clean • `/effector/selected_plan` + XAI • `/cognitive_ew_commands` • `/mesh/fob_status` + `/payload/micro_deployment` (simulation).

## Alignment (non-endorsement)

Lattice-style mesh ISR analogs, JIATF-401 marketplace packaging, Replicator-fielding idioms, DHS PEO UAS threads—context only under disclaimer.

## Production Notes

- One page, four quadrants balanced; navy / steel accent; QR to GitHub.  

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

**Ancile Aeris v2.1 - Property of Fratres X AI**
