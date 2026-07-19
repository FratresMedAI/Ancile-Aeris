# ClearSky OS LRBAA v2.1 Submission Checklist

**Property of Fratres X AI** · **BORAP 04 — Countering Unmanned Aircraft Systems** (DHS S&T LRBAA **24-01**)

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release.

Master index (paths and Word exports): **[`submission/LRBAA_Submission_Package_v2.1.md`](submission/LRBAA_Submission_Package_v2.1.md)**

## Narrative and quad (upload as required by the notice)

- [ ] **Concept Paper** — [`submission/ClearSky_OS_Concept_Paper_v2.1.md`](submission/ClearSky_OS_Concept_Paper_v2.1.md) · [`.docx`](submission/ClearSky_OS_Concept_Paper_v2.1.docx) — convert to **PDF** in Word if the portal requires PDF.
- [ ] **Quad Chart** (one page, four quadrants — layout in Word from) — [`submission/ClearSky_OS_Quad_Chart_v2.1.md`](submission/ClearSky_OS_Quad_Chart_v2.1.md) · [`.docx`](submission/ClearSky_OS_Quad_Chart_v2.1.docx)

## Video (typical “concept overview” attachment)

- [ ] **Primary recorded-voiceover MP4** — `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_recorded_voiceover_demo.mp4` (built around the checked-in source WAV below).
- [ ] **Recorded source WAV** — `artifacts/video_v21/recorded_voiceover/NoteGPT_Speech_1778252509802.wav`
- [ ] **Silent 4:00 MP4** (backup, burned-in subtitles) — `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo.mp4`
- [ ] **Edge-TTS voiceover MP4** (backup) — `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4`
- [ ] **Script / production notes** (reviewer reference) — [`submission/ClearSky_OS_Video_Script_v2.1.md`](submission/ClearSky_OS_Video_Script_v2.1.md) · [`.docx`](submission/ClearSky_OS_Video_Script_v2.1.docx); [`submission/Video_Production_Package_v2.1.md`](submission/Video_Production_Package_v2.1.md) · [`.docx`](submission/Video_Production_Package_v2.1.docx)
- [ ] **Full narration text** — [`submission/ClearSky_OS_Voiceover_Narration_v2.1.md`](submission/ClearSky_OS_Voiceover_Narration_v2.1.md) · [`.docx`](submission/ClearSky_OS_Voiceover_Narration_v2.1.docx)

## Code / reproducibility

- [ ] **Repository URL** — https://github.com/Fratres-X-AI/ClearSky-OS  
- [ ] **Docker-only build** documented in [`README.md`](README.md); demo: `ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py` (inside container per README).

## Regenerate Office exports from Markdown

```powershell
cd "path\to\ClearSky-OS"
python tools\export_submission_docx.py
```

Requires **Pandoc** ([install](https://pandoc.org/installing.html); on Windows, `%LocalAppData%\Pandoc\pandoc.exe` after winget install).

## Technical completeness (software)

- [x] Layered non-kinetic effector stack (`clearsky_os_effectors`) with simulation-safe paths and XAI on `/effector/selected_plan` and `/cognitive_ew_commands`
- [x] FOB swarm + modular micro-payload simulation topics (`/mesh/fob_status`, `/payload/micro_deployment`)
- [x] DARKSPACE audit posture (`/darkspace/status` verified in demo narrative)
- [x] Human-on-the-loop; **kamikaze ram** only as policy-gated last-resort **simulation**
- [x] BORAP pillars mapped in [`docs/LRBAA_BORAP_04_MAPPING.md`](docs/LRBAA_BORAP_04_MAPPING.md)

---

**ClearSky OS v2.1 — Property of Fratres X AI**
