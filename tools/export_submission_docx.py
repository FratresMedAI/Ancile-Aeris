#!/usr/bin/env python3
"""Regenerate submission .docx from Markdown via Pandoc (v2.1 LRBAA package).

Requires: Pandoc on PATH, or default install at %LocalAppData%\\Pandoc\\pandoc.exe (Windows).

Usage (from repository root):
  python tools/export_submission_docx.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pandoc() -> str:
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"
    if local.is_file():
        return str(local)
    w = shutil.which("pandoc")
    if w:
        return w
    raise SystemExit(
        "pandoc not found. Install from https://pandoc.org/installing.html "
        "or winget install JohnMacFarlane.Pandoc"
    )


PAIRS: list[tuple[str, str]] = [
    ("submission/Ancile_Aeris_Concept_Paper_v2.1.md", "submission/Ancile_Aeris_Concept_Paper_v2.1.docx"),
    ("submission/Ancile_Aeris_Quad_Chart_v2.1.md", "submission/Ancile_Aeris_Quad_Chart_v2.1.docx"),
    ("submission/Ancile_Aeris_Video_Script_v2.1.md", "submission/Ancile_Aeris_Video_Script_v2.1.docx"),
    ("submission/Video_Production_Package_v2.1.md", "submission/Video_Production_Package_v2.1.docx"),
    ("submission/Ancile_Aeris_Voiceover_Narration_v2.1.md", "submission/Ancile_Aeris_Voiceover_Narration_v2.1.docx"),
    ("submission/LRBAA_Submission_Package_v2.1.md", "submission/LRBAA_Submission_Package_v2.1.docx"),
]


def main() -> None:
    exe = pandoc()
    for src_rel, dst_rel in PAIRS:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.is_file():
            print("skip (missing):", src_rel, file=sys.stderr)
            continue
        subprocess.run(
            [exe, str(src), "-o", str(dst)],
            check=True,
        )
        print("Wrote", dst_rel)


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
