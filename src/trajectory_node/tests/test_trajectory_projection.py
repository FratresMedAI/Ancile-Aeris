def project(x: float, y: float, vx: float, vy: float, t: float) -> tuple[float, float]:
    return x + vx * t, y + vy * t


def test_project_forward() -> None:
    px, py = project(0.0, 0.0, 2.0, -1.0, 1.5)
    assert px == 3.0
    assert py == -1.5


def test_project_zero_velocity() -> None:
    px, py = project(10.0, 5.0, 0.0, 0.0, 2.0)
    assert px == 10.0
    assert py == 5.0
