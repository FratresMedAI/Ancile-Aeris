# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `main`  | Yes       |
| tagged releases (`v*`) | Best effort |

## Reporting a vulnerability

Do **not** open a public GitHub issue for security-sensitive findings.

Please report vulnerabilities privately via one of:

1. **GitHub Security Advisories** — [Report a vulnerability](https://github.com/Fratres-X-AI/ClearSky-OS/security/advisories/new)
2. **Email** — `security@fratres-x.ai` (subject: `ClearSky OS security`)

Include:

- Affected component / package path
- Steps to reproduce
- Impact assessment (confidentiality, integrity, availability, safety)
- Whether a proof-of-concept is available (do not attach exploit payloads that target production systems)

We aim to acknowledge reports within **5 business days**.

## Scope notes

ClearSky OS is a **simulation-only** defensive C-UAS research stack.

In scope:

- Secrets exposure in the repository or container image
- Unsafe defaults that could mislead operators about authorization state
- Integrity issues in the DARKSPACE / audit trail modeling
- Dependency or container supply-chain issues in supported build paths

Out of scope:

- Requests for real-world weaponization guidance
- Theoretical issues in roadmap stub modules with no executable path
- Findings that require disabling documented safety gates

## Safe harbor

We will not pursue legal action against researchers who:

- Make a good-faith effort to avoid privacy violations and service disruption
- Report promptly and do not exploit findings beyond demonstration
- Do not publicly disclose before we have had a reasonable chance to remediate
