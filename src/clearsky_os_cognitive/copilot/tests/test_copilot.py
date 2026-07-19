def build_summary(query: str) -> str:
    return f"Stub copilot summary: {query[:120]}"


def test_build_summary_prefix() -> None:
    summary = build_summary("status of monitored tracks")
    assert summary.startswith("Stub copilot summary:")
