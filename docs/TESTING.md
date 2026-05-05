# Ancile-Aeris Testing`r`n`r`n**Property of Fratres X AI**

## Build Validation

Run inside Docker container context:

```bash
docker compose -f docker/docker-compose.yml build ancile-aeris
```

## Package Tests

```bash
docker run --rm -v "c:/Users/Besn Daddy/Desktop/Ancile Aeris/Ancile-Aeris:/opt/ancile_aeris_ws" -w /opt/ancile_aeris_ws ancile-aeris bash -lc "rm -rf build install log && source /opt/ros/kilted/setup.bash && colcon build --symlink-install && source install/setup.bash && colcon test && colcon test-result --verbose"
```

## Launch Smoke Test

```bash
docker compose -f docker/docker-compose.yml up ancile-aeris
```

Video-enhanced C-UAS profile:

```bash
ANCILE_PAYLOAD=cuas ANCILE_SIM_MODE=true docker compose -f docker/docker-compose.yml up ancile-aeris
```

Expected indicators:
- selected payload nodes plus shared dashboard and safety paths start
- `/fused_tracks`, `/predicted_trajectories`, `/threats`, `/effector_commands`, `/audit/events`, `/dashboard/state` active
- `/sensor/visual/analytics`, `/swarm/intent_assessment`, `/sensor/resilience_alerts` active

## Soldier-Safety Gate Validation

Run mixed friendly/hostile defensive scenario validation:

```bash
docker run --rm -v "c:/Users/Besn Daddy/Desktop/Ancile Aeris/Ancile-Aeris:/opt/ancile_aeris_ws" -w /opt/ancile_aeris_ws ancile-aeris bash -lc "python3 scripts/soldier_safety_scenario.py"
```

Pass criteria:
- friendly tracks are always forced to `monitor` (`blocked_friendly_iff`)
- any digital twin risk blocks non-monitor actions (`blocked_digital_twin_risk`)
- non-monitor action requires operator authorization
- `zero_fratricide = true`
- `latency_target_met = true` with `<100 ms` decision latency in scenario report

## Performance Baseline Targets

- Detectionâ†’Fusionâ†’C2 pipeline latency: target `<150 ms` (sim baseline)
- Visual pipeline effective throughput (simulated): target `>=30 FPS` on Jetson-class target
- Dashboard update cadence: `>=5 Hz`

## Regression Checklist

- `colcon build --symlink-install` success
- `colcon test` success
- no schema regressions in JSON payload contracts
- ROE safety gates continue to block non-authorized actions in non-sim mode

## Conservation Anti-Poaching Scenario

Run conservation scenario generator:

```bash
python scripts/conservation_anti_poaching_scenario.py
```

Pass criteria:
- detect/track outputs are generated from conservation payload data.
- any non-monitor recommendation remains blocked without operator authorization.
- report is generated at `reports/conservation_anti_poaching_report.json`.

## BORAP 04 Urban Mass-Gathering Demo

```bash
python scripts/demo_borap04_urban_mass_gathering.py
```

Pass criteria:
- report generated at `reports/borap04_urban_mass_gathering_report.json`.
- report includes video analytics, uncertainty-aware fusion, swarm intent, copilot, and sensor resilience flags.

