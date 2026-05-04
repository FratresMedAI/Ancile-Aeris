def summarize(tracks: int, threats: int, commands: int, audits: int) -> dict:
    return {
        "tracks": tracks,
        "threats": threats,
        "commands": commands,
        "audits": audits,
    }


def test_summary_shape() -> None:
    s = summarize(2, 1, 1, 5)
    assert s["tracks"] == 2
    assert s["audits"] == 5
