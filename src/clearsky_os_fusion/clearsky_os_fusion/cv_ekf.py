"""Constant-velocity Kalman filter with nearest-neighbor association."""

from __future__ import annotations

import math
from dataclasses import dataclass


def _mat_mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            aik = a[i][k]
            for j in range(cols):
                out[i][j] += aik * b[k][j]
    return out


def _mat_vec(a: list[list[float]], v: list[float]) -> list[float]:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def _mat_add(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _mat_sub(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _mat_T(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def _mat2_inv(m: list[list[float]]) -> list[list[float]]:
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if abs(det) < 1e-12:
        det = 1e-12
    return [[m[1][1] / det, -m[0][1] / det], [-m[1][0] / det, m[0][0] / det]]


def _eye(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


@dataclass
class Measurement:
    x: float
    y: float
    confidence: float = 1.0
    track_id: str = ""


class ConstantVelocityEKF:
    """2D constant-velocity Kalman filter (linear CV model)."""

    def __init__(
        self,
        dt: float = 0.05,
        process_var: float = 2.0,
        measure_var: float = 0.05,
    ) -> None:
        self.dt = max(1e-3, float(dt))
        self.process_var = float(process_var)
        self.measure_var = float(measure_var)
        self.x = [0.0, 0.0, 0.0, 0.0]  # x, y, vx, vy
        self.P = [[10.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        self.initialized = False
        self.last_nis = 0.0

    def _F(self, dt: float) -> list[list[float]]:
        return [
            [1.0, 0.0, dt, 0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

    def _Q(self, dt: float) -> list[list[float]]:
        q = self.process_var
        dt2 = dt * dt
        dt3 = dt2 * dt
        dt4 = dt2 * dt2
        # Continuous white-noise accel model, block diagonal for x/y
        qx = [
            [dt4 / 4.0 * q, 0.0, dt3 / 2.0 * q, 0.0],
            [0.0, dt4 / 4.0 * q, 0.0, dt3 / 2.0 * q],
            [dt3 / 2.0 * q, 0.0, dt2 * q, 0.0],
            [0.0, dt3 / 2.0 * q, 0.0, dt2 * q],
        ]
        return qx

    def predict(self, dt: float | None = None) -> None:
        step = self.dt if dt is None else max(1e-3, float(dt))
        F = self._F(step)
        Q = self._Q(step)
        self.x = _mat_vec(F, self.x)
        self.P = _mat_add(_mat_mul(_mat_mul(F, self.P), _mat_T(F)), Q)

    def update(self, mx: float, my: float) -> float:
        """Update with position measurement. Returns NIS."""
        if not self.initialized:
            self.x = [float(mx), float(my), 0.0, 0.0]
            self.P = [[self.measure_var if i == j else 0.0 for j in range(4)] for i in range(4)]
            self.P[2][2] = 5.0
            self.P[3][3] = 5.0
            self.initialized = True
            self.last_nis = 0.0
            return 0.0

        H = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
        R = [[self.measure_var, 0.0], [0.0, self.measure_var]]
        z = [float(mx), float(my)]
        z_pred = _mat_vec(H, self.x)
        y = [z[0] - z_pred[0], z[1] - z_pred[1]]

        S = _mat_add(_mat_mul(_mat_mul(H, self.P), _mat_T(H)), R)
        S_inv = _mat2_inv(S)
        # K = P H^T S^-1  (4x2)
        PHt = _mat_mul(self.P, _mat_T(H))
        K = _mat_mul(PHt, S_inv)

        self.x = [
            self.x[0] + K[0][0] * y[0] + K[0][1] * y[1],
            self.x[1] + K[1][0] * y[0] + K[1][1] * y[1],
            self.x[2] + K[2][0] * y[0] + K[2][1] * y[1],
            self.x[3] + K[3][0] * y[0] + K[3][1] * y[1],
        ]
        I = _eye(4)
        KH = _mat_mul(K, H)
        self.P = _mat_mul(_mat_sub(I, KH), self.P)

        nis = y[0] * (S_inv[0][0] * y[0] + S_inv[0][1] * y[1]) + y[1] * (
            S_inv[1][0] * y[0] + S_inv[1][1] * y[1]
        )
        self.last_nis = nis
        return nis

    def mahalanobis(self, mx: float, my: float) -> float:
        if not self.initialized:
            return 0.0
        H = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
        R = [[self.measure_var, 0.0], [0.0, self.measure_var]]
        z_pred = _mat_vec(H, self.x)
        y = [float(mx) - z_pred[0], float(my) - z_pred[1]]
        S = _mat_add(_mat_mul(_mat_mul(H, self.P), _mat_T(H)), R)
        S_inv = _mat2_inv(S)
        nis = y[0] * (S_inv[0][0] * y[0] + S_inv[0][1] * y[1]) + y[1] * (
            S_inv[1][0] * y[0] + S_inv[1][1] * y[1]
        )
        return math.sqrt(max(0.0, nis))

    def state(self) -> dict[str, float]:
        return {
            "x": self.x[0],
            "y": self.x[1],
            "vx": self.x[2],
            "vy": self.x[3],
            "p_x": self.P[0][0],
            "p_y": self.P[1][1],
            "nis": self.last_nis,
        }

    def calibrated_confidence(self, measurement_confidence: float) -> float:
        nis_term = max(0.0, 1.0 - self.last_nis / 6.0)
        meas = max(0.0, min(1.0, float(measurement_confidence)))
        if not self.initialized:
            return 0.0
        return max(0.0, min(1.0, 0.55 * meas + 0.45 * nis_term))


def associate_nearest(
    ekf: ConstantVelocityEKF,
    measurements: list[Measurement],
    gate: float = 3.0,
) -> Measurement | None:
    """Pick nearest measurement inside Mahalanobis gate."""
    if not measurements:
        return None
    if not ekf.initialized:
        return max(measurements, key=lambda m: m.confidence)

    best: Measurement | None = None
    best_d = float("inf")
    for m in measurements:
        d = ekf.mahalanobis(m.x, m.y)
        if d <= gate and d < best_d:
            best = m
            best_d = d
    return best
