def mismatch_score(visual_tracks: int, rf_hits: int, acoustic_hits: int) -> float:
    total_non_visual = rf_hits + acoustic_hits
    if visual_tracks == 0 and total_non_visual == 0:
        return 0.0
    if visual_tracks == 0:
        return 1.0
    return min(1.0, abs(visual_tracks - total_non_visual) / max(1, visual_tracks + total_non_visual))


def test_high_mismatch_when_visual_missing() -> None:
    assert mismatch_score(0, 2, 1) == 1.0


def test_low_mismatch_when_balanced() -> None:
    assert mismatch_score(3, 2, 1) < 0.2
