from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF, Measurement, associate_nearest
from clearsky_os_fusion.learned_fusion import score_measurement, shadow_associate
from clearsky_os_fusion.measurement_adapters import adapt_lidar, adapt_bearing_only


def test_ekf_tracks_moving_target() -> None:
    ekf = ConstantVelocityEKF(dt=0.1, process_var=1.0, measure_var=0.02)
    for i in range(20):
        ekf.predict(0.1)
        ekf.update(0.1 * (i + 1), 0.0)
    state = ekf.state()
    assert state["x"] > 1.0
    assert abs(state["vx"] - 1.0) < 0.5


def test_calibrated_confidence_bounds() -> None:
    ekf = ConstantVelocityEKF(dt=0.05)
    ekf.update(0.0, 0.0)
    conf = ekf.calibrated_confidence(0.8)
    assert 0.0 <= conf <= 1.0


def test_associate_nearest_gates_outlier() -> None:
    ekf = ConstantVelocityEKF(dt=0.05)
    ekf.update(0.0, 0.0)
    ekf.predict(0.05)
    chosen = associate_nearest(
        ekf,
        [
            Measurement(x=0.02, y=0.01, confidence=0.9, track_id="near", modality="visual"),
            Measurement(x=50.0, y=50.0, confidence=0.99, track_id="far", modality="visual"),
        ],
        gate=3.0,
    )
    assert chosen is not None
    assert chosen.track_id == "near"


def test_lidar_adapter() -> None:
    ms = adapt_lidar([{"id": "l1", "range_m": 100.0, "bearing_deg": 0.0, "confidence": 0.7}])
    assert abs(ms[0].x - 100.0) < 1e-6
    assert ms[0].modality == "lidar"


def test_bearing_adapter() -> None:
    ms = adapt_bearing_only(
        [{"detection_id": "a1", "estimated_bearing_deg": 90.0, "confidence": 0.6}],
        range_hint_m=50.0,
        modality="acoustic",
    )
    assert abs(ms[0].y - 50.0) < 1e-6


def test_learned_prefers_near_over_high_conf_far() -> None:
    ekf = ConstantVelocityEKF(dt=0.05)
    ekf.update(0.0, 0.0)
    ekf.predict(0.05)
    near = Measurement(0.05, 0.0, 0.6, "near", "visual")
    far = Measurement(80.0, 80.0, 0.99, "far", "visual")
    # Near should score higher once mahalanobis is considered
    assert score_measurement(near, 0.5) >= score_measurement(far, 20.0)
    chosen = shadow_associate(ekf, [near, far], min_score=0.1)
    assert chosen is not None
    assert chosen.track_id == "near"
