from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF, Measurement, associate_nearest


def test_ekf_tracks_moving_target() -> None:
    ekf = ConstantVelocityEKF(dt=0.1, process_var=1.0, measure_var=0.02)
    # Move along x
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
            Measurement(x=0.02, y=0.01, confidence=0.9, track_id="near"),
            Measurement(x=50.0, y=50.0, confidence=0.99, track_id="far"),
        ],
        gate=3.0,
    )
    assert chosen is not None
    assert chosen.track_id == "near"
