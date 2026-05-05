#!/usr/bin/env python3
import json
import time
from pathlib import Path


def decide(track: dict, cyber: dict, pid: dict, twin_risk: float, operator_auth: dict) -> dict:
    action = "jam" if float(track.get("score", 0.0)) >= 0.7 else "monitor"

    if not bool(pid.get("passed", False)) or float(pid.get("confidence", 0.0)) < 0.999:
        return {"action": "monitor", "authorized": False, "reason": "blocked_pid_gate"}
    if cyber.get("disposition") == "friendly":
        return {"action": "monitor", "authorized": False, "reason": "blocked_friendly_iff"}
    if cyber.get("disposition") != "unknown_or_hostile" or float(cyber.get("confidence", 0.0)) < 0.7:
        return {"action": "monitor", "authorized": False, "reason": "blocked_unconfirmed_hostile_identity"}
    if action != "monitor" and twin_risk > 0.0:
        return {"action": "monitor", "authorized": False, "reason": "blocked_digital_twin_risk"}
    if action != "monitor":
        auth = operator_auth.get(track.get("track_id"), {})
        if not auth.get("authorized", False) or auth.get("action") != action:
            return {"action": action, "authorized": False, "reason": "blocked_no_operator_authorization"}
    return {"action": action, "authorized": True, "reason": "authorized"}


def main() -> None:
    start = time.perf_counter()

    tracks = [
        {
            "track": {"track_id": "friendly-001", "score": 0.95},
            "cyber": {"disposition": "friendly", "confidence": 0.99},
            "pid": {"passed": True, "confidence": 0.999},
            "twin_risk": 0.0,
        },
        {
            "track": {"track_id": "hostile-001", "score": 0.93},
            "cyber": {"disposition": "unknown_or_hostile", "confidence": 0.92},
            "pid": {"passed": True, "confidence": 0.999},
            "twin_risk": 0.0,
        },
        {
            "track": {"track_id": "hostile-risky", "score": 0.91},
            "cyber": {"disposition": "unknown_or_hostile", "confidence": 0.95},
            "pid": {"passed": True, "confidence": 0.999},
            "twin_risk": 0.4,
        },
    ]

    operator_auth = {
        "hostile-001": {"authorized": True, "action": "jam"},
        "hostile-risky": {"authorized": True, "action": "jam"},
    }

    decisions = []
    for sample in tracks:
        result = decide(sample["track"], sample["cyber"], sample["pid"], sample["twin_risk"], operator_auth)
        decisions.append({"track_id": sample["track"]["track_id"], **result})

    friendly_actions = [d for d in decisions if d["track_id"].startswith("friendly") and d["action"] != "monitor"]
    fratricide_blocked = len(friendly_actions) == 0

    latency_ms = (time.perf_counter() - start) * 1000.0
    report = {
        "scenario": "mixed_friendly_hostile_defensive",
        "decisions": decisions,
        "zero_fratricide": fratricide_blocked,
        "latency_ms": round(latency_ms, 3),
        "latency_target_ms": 100.0,
        "latency_target_met": latency_ms < 100.0,
    }

    out = Path("/tmp/ancile_aeris_soldier_safety_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()

