"""Tests for clearsky_os_baby_interceptor (imports monolithic node module from source tree)."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_NODE = Path(__file__).resolve().parent.parent / "clearsky_os_baby_interceptor" / "interceptor_node.py"
_spec = spec_from_file_location("clearsky_os_baby_interceptor_node", _NODE)
assert _spec and _spec.loader
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def test_auth_path_requires_double_human_authorization() -> None:
    assert not _mod.auth_path_ok(True, True, False, True, True)
    assert _mod.auth_path_ok(True, True, True, True, True)
