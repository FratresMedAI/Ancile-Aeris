from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.synthetic_dataset_pipeline import generate_manifest
from scripts.model_export_pipeline import export_plan


def test_generate_manifest(tmp_path: Path) -> None:
    manifest = generate_manifest(tmp_path, 20)
    assert manifest.exists()


def test_export_plan(tmp_path: Path) -> None:
    plan = export_plan("yolo26s", tmp_path)
    assert plan.exists()
