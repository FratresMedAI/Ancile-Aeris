def auth_path_ok(safety_open: bool, launch: bool, terminal: bool, release_authorized: bool) -> bool:
    return safety_open and launch and terminal and release_authorized


def test_auth_path_requires_double_human_authorization() -> None:
    assert not auth_path_ok(True, True, False, True)
    assert auth_path_ok(True, True, True, True)
