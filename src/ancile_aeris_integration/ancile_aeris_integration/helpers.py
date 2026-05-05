from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from typing import Any

from std_msgs.msg import String


class AncileAuditBridge:
    """Ancile immutable hash-chain + ROS audit/XAI publishers."""

    def __init__(self, node: Any, component: str) -> None:
        self.node = node
        self.component = component
        self.key = os.getenv("AUDIT_HMAC_KEY", "change-me").encode("utf-8")
        self.last_hash = "GENESIS"
        self.audit_pub = self.node.create_publisher(String, "/audit/events", 20)
        self.xai_pub = self.node.create_publisher(String, "/xai_explanation", 20)

    def _digest(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def emit(self, event_type: str, payload: dict, *, xai_text: str | None = None) -> None:
        now = time.time()
        body = {
            "timestamp": now,
            "component": self.component,
            "event_type": event_type,
            "payload": payload,
            "previous_hash": self.last_hash,
        }
        digest = self._digest(body)
        sig = hmac.new(self.key, digest.encode("utf-8"), hashlib.sha256).hexdigest()
        body["event_hash"] = digest
        body["signature"] = sig
        self.last_hash = digest

        self.audit_pub.publish(String(data=json.dumps(body)))
        xai_payload = {
            "component": self.component,
            "event_type": event_type,
            "summary": xai_text or f"{self.component} produced {event_type}.",
            "trace_hash": digest,
        }
        self.xai_pub.publish(String(data=json.dumps(xai_payload)))
