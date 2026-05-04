def build_event(sensor_id: str, counter: int) -> dict:
    return {
        "event_id": f"{sensor_id}-{counter}",
        "sensor_id": sensor_id,
        "pixel_x": counter % 128,
        "pixel_y": (counter * 3) % 128,
        "polarity": 1.0 if counter % 2 else -1.0,
        "confidence": 0.6,
    }


def test_build_event_bounds() -> None:
    event = build_event("stub", 4)
    assert event["pixel_x"] < 128
    assert event["pixel_y"] < 128
