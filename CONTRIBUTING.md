# Contributing to Ancile Aeris

Thanks for your interest in improving Ancile Aeris. This repository is a **simulation-first** ROS 2 Counter-UAS research prototype. Contributions that strengthen safety, auditability, test coverage, and documentation are especially welcome.

## Before you start

1. Read the [Code of Conduct](CODE_OF_CONDUCT.md).
2. Skim [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and the root [README](README.md).
3. Open an issue describing the change if it is more than a small fix.

## Development environment

**Supported path:** Docker only (see [`docker/`](docker/)).

```bash
# From repository root
ANCILE_LAUNCH_FILE=ancile_aeris_basic_demo.launch.py \
  docker compose -f docker/docker-compose.yml up --build
```

Clean rebuild inside the container:

```bash
./clean-build.sh
# or
source /opt/ros/kilted/setup.bash
rm -rf build/ install/ log/
colcon build --symlink-install --packages-up-to ancile_aeris_bringup
```

Native Windows `colcon build` is **not** supported.

## Contribution guidelines

### Do

- Keep changes focused and reviewable
- Prefer importing production modules in tests over re-implementing scoring logic
- Preserve human-on-the-loop and safety-gate semantics
- Document new ROS topics, parameters, and launch flags
- Match existing package layout (`src/<package>/`)

### Do not

- Introduce autonomous weapon-release pathways
- Enable kinetic modes by default
- Commit secrets, credentials, or large unrelated binaries
- Rewrite submission narrative docs unless the change is factual (URLs, versions)

## Pull request checklist

- [ ] Description explains **why**, not only what
- [ ] Builds in the Docker / CI ROS Kilted environment
- [ ] Relevant `colcon test` targets pass
- [ ] Docs updated when behavior or public topics change
- [ ] No hard-coded machine-specific paths

## Commit style

Prefer concise, imperative subjects:

```text
Add safety-gate regression for dual-authorized veto
Fix Docker CRLF handling for launch entrypoints
Docs: clarify FOB swarm default profile
```

## Security

Report vulnerabilities privately per [SECURITY.md](SECURITY.md). Do not open public issues for exploitable findings.

## License

By contributing, you agree that your contributions are licensed under the [Apache License 2.0](LICENSE).
