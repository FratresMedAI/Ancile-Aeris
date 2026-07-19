# clearsky_os_effectors

Simulation-safe non-kinetic effector catalog and selection policy for the
ClearSky OS counter-UAS stack. This package models a layered defeat
posture in software only; it never drives real RF, directed-energy, or
cyber hardware.

## Effector catalog (simulation stubs)

| Mode                     | Family              | Min score | Notes                                                                  |
| ------------------------ | ------------------- | --------: | ---------------------------------------------------------------------- |
| `monitor`                | passive             |      0.00 | Default; passive ISR overlay only.                                     |
| `multi_sensor_deception` | deception           |      0.55 | Cross-sensor decoy injection to degrade adversary targeting.           |
| `cognitive_jamming`      | rf_denial           |      0.65 | Adaptive narrowband jamming on observed control link.                  |
| `gnss_link_spoofing`     | nav_denial          |      0.72 | Localized GNSS / link spoof to redirect to a safe geofence.            |
| `hpm_denial_stub`        | directed_energy_sim |      0.80 | High-power microwave denial pulse simulation.                          |
| `control_link_takeover`  | cyber_takeover      |      0.88 | Authorized cyber takeover; requires dual operator authorization.       |

All entries are non-kinetic. The catalog enforces `kinetic == False` for
every mode; this is asserted in `tests/test_effector_policy.py`.

## Topics

| Direction | Topic                              | Purpose                                                            |
| --------- | ---------------------------------- | ------------------------------------------------------------------ |
| sub       | `/fused_tracks`                    | Fused track stream (highest-confidence track per tick).            |
| sub       | `/safety_gate_status`              | Master safety gate (`allow: true/false`).                          |
| sub       | `/operator/launch_authorizations`  | Dual-authorization stream for takeover-class effectors.            |
| pub       | `/effector/selected_plan`          | Selected effector intent + XAI rationale (monitor-only by default).|
| pub       | `/effector/status`                 | Per-mode readiness telemetry (sim).                                |
| pub       | `/audit/events`                    | Audit emissions for plan publications.                             |

## Selection invariants

- Safety gate closed → `monitor_only: true`, regardless of score.
- `control_link_takeover` requires both safety gate open and dual auth.
- Disabled families in `enabled_families` are excluded from selection.
- Output always includes XAI rationale and the score threshold that fired.

## Launch

```bash
ros2 launch clearsky_os_effectors clearsky_os_effectors.launch.py
```

This is included automatically by
`clearsky_os_basic_demo.launch.py` when
`features.effectors.enabled: true` in `payload_selector.yaml`.
