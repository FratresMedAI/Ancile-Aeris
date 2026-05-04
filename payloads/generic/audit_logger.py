from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class AuditEvent:
    timestamp: float
    event_type: str
    payload: Dict[str, Any]
    previous_hash: str
    event_hash: str
    signature: str


class ImmutableAuditLogger:
    def __init__(self, path: str, key: str | None = None) -> None:
        self.path = path
        self.key = (key or os.getenv("AUDIT_HMAC_KEY", "change-me")).encode("utf-8")
        self.last_hash = self._load_last_hash()

    def _load_last_hash(self) -> str:
        if not os.path.exists(self.path):
            return "GENESIS"
        prev = "GENESIS"
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                evt = json.loads(raw)
                prev = evt.get("event_hash", prev)
        return prev

    def _compute_hash(self, ts: float, event_type: str, payload: Dict[str, Any], previous_hash: str) -> str:
        canonical = json.dumps(
            {"timestamp": ts, "event_type": event_type, "payload": payload, "previous_hash": previous_hash},
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _sign(self, digest: str) -> str:
        return hmac.new(self.key, digest.encode("utf-8"), hashlib.sha256).hexdigest()

    def append(self, event_type: str, payload: Dict[str, Any]) -> AuditEvent:
        ts = time.time()
        digest = self._compute_hash(ts, event_type, payload, self.last_hash)
        sig = self._sign(digest)
        event = AuditEvent(ts, event_type, payload, self.last_hash, digest, sig)

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), separators=(",", ":")) + "\n")

        self.last_hash = digest
        return event

    def verify(self) -> bool:
        if not os.path.exists(self.path):
            return True
        prev = "GENESIS"
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                evt = json.loads(raw)
                digest = self._compute_hash(evt["timestamp"], evt["event_type"], evt["payload"], prev)
                sig = self._sign(digest)
                if evt["previous_hash"] != prev or evt["event_hash"] != digest or evt["signature"] != sig:
                    return False
                prev = evt["event_hash"]
        return True
