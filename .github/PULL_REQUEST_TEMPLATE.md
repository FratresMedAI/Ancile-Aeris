## Summary

<!-- 1–3 bullets: why this change exists -->

## Type of change

- [ ] Bug fix
- [ ] Feature / capability
- [ ] Documentation
- [ ] Tests / CI
- [ ] Refactor (no behavior change)

## Test plan

- [ ] `colcon build` succeeds in ROS 2 Kilted (Docker / CI)
- [ ] Relevant `colcon test` targets pass
- [ ] Manual smoke (if applicable): `ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py`

## Safety / policy impact

- [ ] No change to autonomous release semantics
- [ ] Kinetic / last-resort paths remain policy-off by default (or documented exception)
- [ ] Audit / DARKSPACE behavior unchanged or documented

## Checklist

- [ ] Docs updated for new topics, params, or launch flags
- [ ] No secrets or machine-specific paths committed
