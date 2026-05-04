import hashlib
import json


def classify_oui(oui: str, friendly_ouis: set[str]) -> str:
    return "friendly" if oui.upper() in friendly_ouis else "unknown_or_hostile"


def ledger_hash(prev_hash: str, emitter_id: str, disposition: str, confidence: float) -> str:
    entry = {
        "event": "identity_assessment",
        "emitter_id": emitter_id,
        "disposition": disposition,
        "confidence": confidence,
        "prev_hash": prev_hash,
    }
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode("utf-8")).hexdigest()


def test_friendly_oui() -> None:
    assert classify_oui("D8:3A:DD", {"D8:3A:DD"}) == "friendly"


def test_unknown_oui() -> None:
    assert classify_oui("AA:BB:CC", {"D8:3A:DD"}) == "unknown_or_hostile"


def test_ledger_hash_chain_changes_per_event() -> None:
    h1 = ledger_hash("genesis", "em1", "friendly", 0.9)
    h2 = ledger_hash(h1, "em2", "unknown_or_hostile", 0.8)
    assert h1 != h2


def test_ledger_hash_deterministic_for_same_input() -> None:
    h1 = ledger_hash("genesis", "em1", "friendly", 0.9)
    h2 = ledger_hash("genesis", "em1", "friendly", 0.9)
    assert h1 == h2
