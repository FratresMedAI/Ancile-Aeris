def template_answer(query: str, summary: dict, latest: dict) -> str:
    return (
        f"Query: {query}\n"
        f"Current counts - tracks: {summary.get('tracks', 0)}, threats: {summary.get('threats', 0)}, "
        f"commands: {summary.get('commands', 0)}, audits: {summary.get('audits', 0)}.\n"
        f"Latest threat snapshot: {latest.get('threat', {})}"
    )


def test_template_answer_contains_query() -> None:
    text = template_answer("show threats", {"tracks": 2, "threats": 1}, {"threat": {"id": "t1"}})
    assert "show threats" in text
    assert "tracks: 2" in text
    assert "threats: 1" in text
