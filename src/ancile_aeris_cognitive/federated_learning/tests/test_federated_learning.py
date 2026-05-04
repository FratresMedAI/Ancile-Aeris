def build_update_id(model_name: str) -> str:
    return f"{model_name}-12345"


def test_build_update_id() -> None:
    update_id = build_update_id("threat_model_v2")
    assert update_id.startswith("threat_model_v2-")
