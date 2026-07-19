# ClearSky OS Testing

Host-agnostic build, test, and smoke validation for the Docker-supported workspace.

## Build validation

```bash
docker compose -f docker/docker-compose.yml build clearsky-os
```

## Package tests

```bash
docker run --rm -v "${PWD}:/opt/clearsky_os_ws" -w /opt/clearsky_os_ws clearsky-os bash -lc "rm -rf build install log && source /opt/ros/kilted/setup.bash && colcon build --symlink-install && source install/setup.bash && colcon test && colcon test-result --verbose"
```

## Launch smoke test

```bash
docker compose -f docker/docker-compose.yml up clearsky-os
```

C-UAS payload profile:

```bash
CLEARSKY_PAYLOAD=cuas CLEARSKY_SIM_MODE=true docker compose -f docker/docker-compose.yml up clearsky-os
```

Expected indicators:
- selected payload nodes plus shared dashboard and safety paths start
- `/fused_tracks`, `/audit/events`, `/safety_gate_status` active
- effector / scout topics publish when enabled in `payload_selector.yaml`

## Safety-gate scenario

```bash
docker run --rm -v "${PWD}:/opt/clearsky_os_ws" -w /opt/clearsky_os_ws clearsky-os bash -lc "python3 scripts/soldier_safety_scenario.py"
```

Pass criteria:
- friendly tracks forced to `monitor` (`blocked_friendly_iff`)
- digital twin risk blocks non-monitor actions (`blocked_digital_twin_risk`)
- non-monitor action requires operator authorization
- `zero_fratricide = true`

## Regression checklist

- `colcon build --symlink-install` success
- `colcon test` success
- no schema regressions in JSON payload contracts
- safety gates continue to block non-authorized actions outside sim shortcuts
