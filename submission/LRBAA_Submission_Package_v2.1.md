Revised May 8, 2026 — Ancile Aeris **v2.1** (LRBAA **24-01** · BORAP **04**)

# LRBAA submission package index (v2.1)

**Property of Fratres X AI** · https://github.com/Fratres-X-AI/Ancile-Aeris

Use this list when assembling uploads to SAM.gov / reviewer portals. Authoritative solicitation text remains on **SAM.gov** ([Notice DHS_ST_LRBAA_24-01](https://sam.gov/opp/a0969993ee8542988595334947e39a7d/view)).

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Core narrative (BORAP 04)

| Deliverable | Markdown (source of truth) | Word (print / portal upload) |
|-------------|---------------------------|------------------------------|
| Concept Paper | [`Ancile_Aeris_Concept_Paper_v2.1.md`](Ancile_Aeris_Concept_Paper_v2.1.md) | [`Ancile_Aeris_Concept_Paper_v2.1.docx`](Ancile_Aeris_Concept_Paper_v2.1.docx) |
| Quad Chart (layout + copy) | [`Ancile_Aeris_Quad_Chart_v2.1.md`](Ancile_Aeris_Quad_Chart_v2.1.md) | [`Ancile_Aeris_Quad_Chart_v2.1.docx`](Ancile_Aeris_Quad_Chart_v2.1.docx) |

Regenerate Word from Markdown: `python tools/export_submission_docx.py`

**PDF:** Open the `.docx` in Microsoft Word (or equivalent) and use **Save As → PDF** if the portal requires PDF. (Pandoc + PDF engines are optional; DOCX is the checked-in portable export.)

## Video

| Asset | Location |
|-------|----------|
| Production notes & render recipe | [`Video_Production_Package_v2.1.md`](Video_Production_Package_v2.1.md) · [`.docx`](Video_Production_Package_v2.1.docx) |
| On-screen / caption script | [`Ancile_Aeris_Video_Script_v2.1.md`](Ancile_Aeris_Video_Script_v2.1.md) · [`.docx`](Ancile_Aeris_Video_Script_v2.1.docx) |
| Full voiceover narration (timed) | [`Ancile_Aeris_Voiceover_Narration_v2.1.md`](Ancile_Aeris_Voiceover_Narration_v2.1.md) · [`.docx`](Ancile_Aeris_Voiceover_Narration_v2.1.docx) |
| **Primary reviewer video with recorded narration** | `artifacts/video_v21/Ancile_Aeris_v2.1_LRBAA_BORAP_04_recorded_voiceover_demo.mp4` |
| Recorded source WAV used in primary video | `artifacts/video_v21/recorded_voiceover/NoteGPT_Speech_1778252509802.wav` |
| Recorded-voiceover key frames | `artifacts/video_v21/recorded_voiceover_keyframes/*.png` |
| Recorded-voiceover render CLI | `python tools/render_recorded_voiceover_v21_video.py --voiceover artifacts/video_v21/recorded_voiceover/NoteGPT_Speech_1778252509802.wav` |
| Silent render (burned-in subtitles) | Repository: `artifacts/video_v21/Ancile_Aeris_v2.1_LRBAA_BORAP_04_4min_demo.mp4` |
| With AI voiceover (Edge TTS mux) | `artifacts/video_v21/Ancile_Aeris_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4` |
| Key frames (CapCut / editor) | `artifacts/video_v21/keyframes/*.png` |
| Local render CLI | `python tools/render_ancile_aeris_v21_video.py` |
| Voiceover CLI | `python tools/synthesize_voiceover_v21.py` (requires `pip install edge-tts`; network for TTS) |

## Code / verification

| Item | Location |
|------|----------|
| Docker-only supported build | [`README.md`](../README.md), [`docker/`](../docker/) |
| Operator topic / BORAP mapping | [`docs/LRBAA_BORAP_04_MAPPING.md`](../docs/LRBAA_BORAP_04_MAPPING.md) |

## Legacy filenames (`*_v2.0.*`)

Older `*_v2.0.md` / `.pdf` paths are retained for repository history. The **v2.1** BORAP submission should cite the **`*_v2.1.*`** files above.

---

**Ancile Aeris v2.1 — Property of Fratres X AI**
