import json


def test_visual_payload_shape() -> None:
    payload = {
        "tracks": [{"track_id": "vis-00001", "cls": "drone", "confidence": 0.9}],
        "latency_ms": 20.0,
    }
    serialized = json.dumps(payload)
    parsed = json.loads(serialized)
    assert isinstance(parsed["tracks"], list)
    assert parsed["tracks"][0]["cls"] == "drone"


def test_acoustic_payload_shape() -> None:
    payload = {
        "detections": [{"detection_id": "aud-00001", "confidence": 0.8}],
        "latency_ms": 15.0,
    }
    parsed = json.loads(json.dumps(payload))
    assert "detections" in parsed
    assert parsed["detections"][0]["confidence"] > 0.0


def test_rf_payload_shape() -> None:
    payload = {
        "fingerprints": [{"emitter_id": "rf-00001", "modulation_guess": "ofdm"}],
        "latency_ms": 18.0,
    }
    parsed = json.loads(json.dumps(payload))
    assert parsed["fingerprints"][0]["modulation_guess"] == "ofdm"


def test_lidar_payload_shape() -> None:
    payload = {
        "detections": [{"x": 1.0, "y": 2.0, "z": 0.5, "confidence": 0.7}],
        "source": "lidar_sim",
    }
    parsed = json.loads(json.dumps(payload))
    assert parsed["detections"][0]["z"] == 0.5


def test_sigint_payload_shape() -> None:
    payload = {
        "event_id": "sigint-1",
        "band_hz": [2.4e9, 2.5e9],
        "signal_type": "control_link_candidate",
    }
    parsed = json.loads(json.dumps(payload))
    assert parsed["signal_type"] == "control_link_candidate"
