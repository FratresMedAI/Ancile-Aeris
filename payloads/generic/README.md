## Generic Safety, XAI, and Audit Payload

**ClearSky OS — Property of Fratres X AI**

This payload contains shared safety governance, explainability, and immutable auditing components intended for all **counter-UAS and anti-terror defensive** mission profiles.

Mission posture:

- **Primary:** Sovereign-aligned defensive C-UAS operations with causal XAI, DARKSPACE-class audit traces, and strict human-on-the-loop gates (PID ≥ 0.999).
- **Secondary:** Critical infrastructure perimeter monitoring and homeland mass-gathering security patterns with identical safety posture.

Contained node copies:

- `safety_gate_node.py`
- `audit_logger.py`
- `xai_node.py`
- `clearsky_rule_guard.py`

`clearsky_rule_guard.py` is a ClearSky OS stateless safeguard adapter. It adds offline rule-based detection for prompt injection, unsafe tool traces, credential exfiltration patterns, and encoded override attempts.
