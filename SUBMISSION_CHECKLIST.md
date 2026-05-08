# Ancile Aeris LRBAA v2.1 Submission Checklist

**Property of Fratres X AI** · **BORAP 04 — Countering Unmanned Aircraft Systems** (DHS S&T LRBAA **24-01**)

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release.

Master index (paths and Word exports): **[`submission/LRBAA_Submission_Package_v2.1.md`](submission/LRBAA_Submission_Package_v2.1.md)**

## Narrative and quad (upload as required by the notice)

- [ ] **Concept Paper** — [`submission/Ancile_Aeris_Concept_Paper_v2.1.md`](submission/Ancile_Aeris_Concept_Paper_v2.1.md) · [`.docx`](submission/Ancile_Aeris_Concept_Paper_v2.1.docx) — convert to **PDF** in Word if the portal requires PDF.
- [ ] **Quad Chart** (one page, four quadrants — layout in Word from) — [`submission/Ancile_Aeris_Quad_Chart_v2.1.md`](submission/Ancile_Aeris_Quad_Chart_v2.1.md) · [`.docx`](submission/Ancile_Aeris_Quad_Chart_v2.1.docx)

## Video (typical “concept overview” attachment)

- [ ] **Silent 4:00 MP4** (burned-in subtitles) — `artifacts/video_v21/Ancile_Aeris_v2.1_LRBAA_BORAP_04_4min_demo.mp4`
- [ ] **With voiceover** (optional) — `artifacts/video_v21/Ancile_Aeris_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4`
- [ ] **Script / production notes** (reviewer reference) — [`submission/Ancile_Aeris_Video_Script_v2.1.md`](submission/Ancile_Aeris_Video_Script_v2.1.md) · [`.docx`](submission/Ancile_Aeris_Video_Script_v2.1.docx); [`submission/Video_Production_Package_v2.1.md`](submission/Video_Production_Package_v2.1.md) · [`.docx`](submission/Video_Production_Package_v2.1.docx)
- [ ] **Full narration text** — [`submission/Ancile_Aeris_Voiceover_Narration_v2.1.md`](submission/Ancile_Aeris_Voiceover_Narration_v2.1.md) · [`.docx`](submission/Ancile_Aeris_Voiceover_Narration_v2.1.docx)

## Code / reproducibility

- [ ] **Repository URL** — https://github.com/FratresMedAI/Ancile-Aeris  
- [ ] **Docker-only build** documented in [`README.md`](README.md); demo: `ros2 launch ancile_aeris_bringup ancile_aeris_basic_demo.launch.py` (inside container per README).

## Regenerate Office exports from Markdown

```powershell
cd "path\to\Ancile-Aeris"
python tools\export_submission_docx.py
```

Requires **Pandoc** ([install](https://pandoc.org/installing.html); on Windows, `%LocalAppData%\Pandoc\pandoc.exe` after winget install).

## Technical completeness (software)

- [x] Layered non-kinetic effector stack (`ancile_aeris_effectors`) with simulation-safe paths and XAI on `/effector/selected_plan` and `/cognitive_ew_commands`
- [x] FOB swarm + modular micro-payload simulation topics (`/mesh/fob_status`, `/payload/micro_deployment`)
- [x] DARKSPACE audit posture (`/darkspace/status` verified in demo narrative)
- [x] Human-on-the-loop; **kamikaze ram** only as policy-gated last-resort **simulation**
- [x] BORAP pillars mapped in [`docs/LRBAA_BORAP_04_MAPPING.md`](docs/LRBAA_BORAP_04_MAPPING.md)

---

**Ancile Aeris v2.1 — Property of Fratres X AI**
