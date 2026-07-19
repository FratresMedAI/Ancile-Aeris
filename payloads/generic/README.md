## Generic safety, XAI, and audit payload

Shared safety governance, explainability, and audit components for ClearSky OS profiles.

Modules:

- `safety_gate_node.py`
- `audit_logger.py`
- `xai_node.py`
- `clearsky_rule_guard.py`

`clearsky_rule_guard.py` is a stateless safeguard adapter for prompt-injection / unsafe-tool pattern scoring on operator text paths.
