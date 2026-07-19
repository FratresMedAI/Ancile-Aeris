def classify_material(signature_energy: float) -> str:
    if signature_energy > 0.8:
        return "metallic_body"
    if signature_energy > 0.45:
        return "composite_material"
    return "unknown"


def test_classify_material() -> None:
    assert classify_material(0.9) == "metallic_body"
    assert classify_material(0.5) == "composite_material"
