## Generic Safety, XAI, and Audit Payload

This payload contains shared safety governance, explainability, and immutable auditing components intended for all mission profiles.

Dual-use mapping:
- Primary: trustworthy, operator-governed defensive C-UAS operations.
- Secondary: transparent AI governance for public-safety and conservation deployments.

Contained node copies:
- `safety_gate_node.py`
- `audit_logger.py`
- `xai_node.py`
- `darkspace_rule_guard.py`

`darkspace_rule_guard.py` is an Ancile stateless safeguard adapter. It adds offline rule-based detection for prompt injection, unsafe tool traces, credential exfiltration patterns, and encoded override attempts.
