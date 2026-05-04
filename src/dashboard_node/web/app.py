#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st


def _load_guard():
    root = Path(__file__).resolve().parents[4]
    guard_path = root / "payloads" / "generic"
    if str(guard_path) not in sys.path:
        sys.path.insert(0, str(guard_path))
    try:
        from darkspace_rule_guard import classify_text  # type: ignore
        return classify_text
    except Exception:
        return None


def _is_authenticated() -> bool:
    expected = os.getenv("COUNTERDRONE_DASH_TOKEN", "changeme")
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False

    if st.session_state.auth_ok:
        return True

    st.sidebar.subheader("Dashboard Auth")
    token = st.sidebar.text_input("Token", type="password")
    if st.sidebar.button("Login"):
        st.session_state.auth_ok = token == expected
    return st.session_state.auth_ok


def _read_state_file(path: str) -> dict:
    if not os.path.exists(path):
        return {"summary": {}, "latest": {}}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"summary": {}, "latest": {}}


def main() -> None:
    st.set_page_config(page_title="Ancile-Aeris Dashboard", layout="wide")
    st.title("Ancile-Aeris Control Dashboard")
    st.caption("BORAP 04 aligned simulation-safe monitoring and C2 oversight")

    if not _is_authenticated():
        st.warning("Authentication required")
        return

    state_path = os.getenv("COUNTERDRONE_DASH_STATE", "/tmp/counterdrone_dashboard_state.json")
    state = _read_state_file(state_path)

    payload_options = {
        "cuas": "BORAP04 Dense Urban",
        "conservation": "BORAP04 Mass Gathering",
        "generic": "BORAP04 Critical Infrastructure",
    }
    selected_payload = st.sidebar.selectbox("Payload", list(payload_options.keys()), index=0)
    st.sidebar.caption(f"Scenario label: {payload_options[selected_payload]}")

    c1, c2, c3, c4 = st.columns(4)
    summary = state.get("summary", {})
    c1.metric("Tracks", summary.get("tracks", 0))
    c2.metric("Threats", summary.get("threats", 0))
    c3.metric("Commands", summary.get("commands", 0))
    c4.metric("Audit Events", summary.get("audits", 0))

    st.subheader("Latest State")
    st.write({
        "active_payload": selected_payload,
        "scenario_label": payload_options[selected_payload],
    })
    st.json(state.get("latest", {}))
    st.caption(f"Last refresh: {datetime.utcnow().isoformat()}Z")

    st.subheader("Operator Copilot")
    backend = os.getenv("ANCILE_COPILOT_BACKEND", "template")
    query = st.text_input("Ask copilot", "Summarize threats in the last interval")
    if st.button("Run copilot query"):
        guard = _load_guard()
        if guard is not None:
            verdict = guard(query)
            if verdict.label == "block":
                st.error("Query blocked by DARKSPACE rule guard.")
                return
        summary = state.get("summary", {})
        latest = state.get("latest", {})
        answer = (
            f"[{backend}] tracks={summary.get('tracks', 0)}, threats={summary.get('threats', 0)}, "
            f"commands={summary.get('commands', 0)}, audits={summary.get('audits', 0)}. "
            f"Latest threat={json.dumps(latest.get('threat', {}))}"
        )
        st.success(answer)


if __name__ == "__main__":
    main()
