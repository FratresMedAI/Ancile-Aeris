"""Tests for scout_mothership (imports monolithic node module from source tree)."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_NODE = Path(__file__).resolve().parent.parent / "scout_mothership" / "scout_node.py"
_spec = spec_from_file_location("scout_node", _NODE)
assert _spec and _spec.loader
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def test_loiter_profile() -> None:
    profile = _mod.loiter_profile()
    assert profile["altitude_m"] > 1000.0
    assert "eo_ir" in profile["sensors"]


def test_arson_signal_shape() -> None:
    sig = _mod._arson_carrier_counterterror_signal(0)
    assert "arson_carrier_precursor_sim" in sig
