Revised May 8, 2026 – Final LRBAA Submission Version

# ClearSky OS v2.1 Video Production Package

**Solicitation line:** DHS S&T LRBAA 24-01 (**DHS_ST_LRBAA_24-01**) · BORAP 04 Countering Unmanned Aircraft Systems  
**Runtime:** 4:00 for the local silent / Edge-TTS render; **3:38.98** for the primary reviewer video built around the recorded WAV.  
**Audience:** DHS LRBAA reviewers; C-UAS acquisition stakeholders; lab integrators  
**Tone:** restrained, credible, technically precise. No hype, no combat-trailer language.  
**Property of Fratres X AI • GitHub:** https://github.com/Fratres-X-AI/ClearSky-OS

**Disclaimer:** Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.

## Creative Direction

The finished piece should read like a disciplined defense-technology software walkthrough: dark technical UI, clean line art, restrained map overlays, terminal proof, and conservative narration. The FOB swarm and micro-drone payloads are shown as **simulation inventory and coordination logic**, not field hardware. The **kamikaze ram** appears only as a locked, policy-gated last-resort simulation path.

Anchor message:

```text
BORAP-04-responsive ROS 2 C-UAS software prototype:
Mothership FOB Swarm + modular micro-payload simulation,
non-kinetic-first response doctrine,
DARKSPACE auditability,
human authority preserved.
```

## Exact Timed Shot List

| Time | Shot | Visual | Narration Gist |
|---|---|---|---|
| 0:00-0:15 | Opening slate | ClearSky OS v2.1 title, LRBAA BORAP 04, simulation-only badge | Solicitation responsiveness and simulation boundary. |
| 0:15-0:30 | FOB mesh | 2-4 mothership FOBs connected over a single operational area | Mobile FOB swarm coordination. |
| 0:30-0:48 | Payload catalog | Five micro-payload cards: Sensor Pod, Acoustic Disruptor, Kevlar Web, Cognitive EW, Kamikaze Ram | 10-12 modular micro-drone slots per mothership. |
| 0:48-1:08 | Launch proof | Terminal-style demo launch | Docker-only clean build and basic demo launch. |
| 1:08-1:28 | Fusion pipeline | Sensors feed `/fused_tracks` | Detect/track/identify path. |
| 1:28-1:48 | FOB topics | `/mesh/fob_status`, `/payload/micro_deployment` JSON panels | Fleet status and simulated payload deployment view. |
| 1:48-2:08 | Non-kinetic-first doctrine | Layered response hierarchy | Monitor, deception, EW, spoofing, HPM stub, takeover concept. |
| 2:08-2:28 | Gated kinetic | Locked kamikaze ram panel with two human-authorization locks | Kinetic ram only as last-resort simulation. |
| 2:28-2:48 | DARKSPACE | Clean `/darkspace/status` JSON | Audit integrity and chain continuity. |
| 2:48-3:08 | Effector plan | `/effector/selected_plan` excerpt | Rationale, authorization, monitor-only state. |
| 3:08-3:28 | Cognitive EW | `/cognitive_ew_commands` and XAI fields | Operator-reviewable cognitive path. |
| 3:28-3:45 | Transition roadmap | ROS 2 interfaces, SDR lab path, TRL-6 bench | Acquisition and lab integration realism. |
| 3:45-4:00 | Closing slate | GitHub URL, property line, disclaimer | Calm close for evaluator review. |

## Local Free Render Path

The lowest-manual-effort free path is the included local renderer:

```powershell
cd "C:\Users\Besn Daddy\Desktop\ClearSky OS\ClearSky-OS"
python tools\render_clearsky_os_v21_video.py
```

Outputs:

- Key frames: `artifacts/video_v21/keyframes/*.png`
- MP4: `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo.mp4`

The renderer uses only Python, Pillow, NumPy, and `imageio-ffmpeg` (which downloads/uses a free ffmpeg binary via Python package). If dependencies are missing:

```powershell
python -m pip install pillow numpy imageio-ffmpeg
```

## Free AI voiceover (recommended)

Use **Microsoft Edge TTS** via the free Python package `edge-tts` (requires internet while generating audio). The script times each segment to the 4 minute grid, then muxes AAC audio into a new MP4:

```powershell
cd "C:\Users\Besn Daddy\Desktop\ClearSky OS\ClearSky-OS"
python -m pip install edge-tts
python tools\synthesize_voiceover_v21.py
```

Outputs:

- Per-segment temp audio: `artifacts/video_v21/voiceover/`
- Combined narration WAV: `artifacts/video_v21/voiceover/narration_v21.wav`
- **Final video with narration:** `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4`

Spoken transcript (manual recording option): [`submission/ClearSky_OS_Voiceover_Narration_v2.1.md`](ClearSky_OS_Voiceover_Narration_v2.1.md)

Optional voice tweaks:

```powershell
python tools\synthesize_voiceover_v21.py --voice en-US-JennyNeural --rate -6%
python tools\synthesize_voiceover_v21.py --voice en-US-EricNeural --rate -3%
python tools\synthesize_voiceover_v21.py --skip-video
```

(`--skip-video` only writes the WAV.)

## Primary recorded-voiceover render

For the submission video built around the recorded narration, use the checked-in WAV as the timing source. The render script measures the WAV duration, creates recorded-voiceover keyframes with burned-in captions, and muxes the exact recorded audio into the MP4:

```powershell
cd "C:\Users\Besn Daddy\Desktop\ClearSky OS\ClearSky-OS"
python tools\render_recorded_voiceover_v21_video.py --voiceover artifacts\video_v21\recorded_voiceover\NoteGPT_Speech_1778252509802.wav
```

Outputs:

- Source WAV: `artifacts/video_v21/recorded_voiceover/NoteGPT_Speech_1778252509802.wav`
- Key frames: `artifacts/video_v21/recorded_voiceover_keyframes/*.png`
- **Primary recorded-voiceover MP4:** `artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_recorded_voiceover_demo.mp4`

## Optional One-Click Free AI Polish

If the user wants a more animated version with the least manual effort, use **CapCut Free**:

1. Open CapCut Desktop or Web.
2. Create a 16:9 project.
3. Import every PNG from `artifacts/video_v21/keyframes/`.
4. Set each key frame to match the time blocks above, total 4:00.
5. Add Auto Captions or text overlays from `ClearSky_OS_Video_Script_v2.1.md`.
6. Export 1080p MP4.

Paste this prompt into CapCut AI / script-to-video if available:

```text
Create a 4-minute professional DHS LRBAA submission demo video for ClearSky OS v2.1. Use a calm defense-technology style: dark navy interface, gold accents, clean technical diagrams, no explosions, no hype. Show a ROS 2 counter-UAS software prototype with a Mothership FOB Swarm: 2-4 mobile forward operating bases in one operational area, each carrying 10-12 modular micro-drones. Payload variants: Sensor Pod, Acoustic Disruptor, Kevlar Web Deployer, Cognitive EW Pod, and Kamikaze Ram. Emphasize non-kinetic-first doctrine. Show Kamikaze Ram only as simulation-only, last-resort, policy-off by default, requiring double human authorization. Include DARKSPACE audit status, /mesh/fob_status, /payload/micro_deployment, /effector/selected_plan, and /cognitive_ew_commands. Tone: measured, credible, DHS reviewer-ready. Persistent disclaimer: Simulation-only C-UAS defensive demonstration. No autonomous weapon release.
```

## Production Guardrails

- Do not show explosions, combat impact shots, gore, or triumphal kinetic framing.
- Treat all payloads as simulation inventory and software coordination.
- Keep kamikaze ram visually locked/gated and secondary.
- Use the disclaimer at opening and closing.

**ClearSky OS v2.1 - Property of Fratres X AI**
