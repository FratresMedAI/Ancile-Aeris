# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for tagged releases.

## [Unreleased]

### Added

- Root `LICENSE` (Apache-2.0) and `NOTICE`
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- GitHub issue and pull request templates
- Portfolio-oriented README with architecture overview and badges

### Changed

- **Rebranded from Ancile Aeris to ClearSky OS** — ROS packages `ancile_aeris_*` → `clearsky_os_*`, Docker/k8s names, env vars `ANCILE_*` → `CLEARSKY_*`, docs and submission materials
- Canonical repository URL set to `https://github.com/Fratres-X-AI/ClearSky-OS`
- Documentation paths made host-agnostic for Docker workflows

## [2.1.0] - 2026-05

### Added

- v2.1 basic demo: sensors → fusion → DARKSPACE audit → safety gate → mothership FOB swarm → micro-payload simulation → operator copilot → non-kinetic-first effectors
- Recorded voiceover demo media under `artifacts/video_v21/`
- LRBAA / BORAP 04 submission package materials under `submission/`

### Notes

- Simulation-only defensive demonstration; kinetic `kamikaze_ram` remains policy-off by default

## [2.0.0] - 2026-05

### Added

- Tag `v2.0-lrbaa` baseline for DHS S&T LRBAA 24-01 / BORAP 04 filing materials
- Docker-first ROS 2 Kilted workspace and CI build/test workflow

[Unreleased]: https://github.com/Fratres-X-AI/ClearSky-OS/compare/v2.0-lrbaa...HEAD
[2.1.0]: https://github.com/Fratres-X-AI/ClearSky-OS/releases/tag/v2.0-lrbaa
[2.0.0]: https://github.com/Fratres-X-AI/ClearSky-OS/releases/tag/v2.0-lrbaa
