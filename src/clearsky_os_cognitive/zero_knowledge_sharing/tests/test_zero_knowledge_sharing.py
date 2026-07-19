def build_share_id(partner: str) -> str:
    return f"{partner}-1234"


def test_build_share_id() -> None:
    assert build_share_id("jiatf401").startswith("jiatf401-")
