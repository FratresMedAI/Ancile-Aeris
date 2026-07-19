#!/usr/bin/env python3
"""Generate narration audio for ClearSky OS v2.1 submission video.

Uses Edge TTS (free; requires network once per run).
Requires: pip install edge-tts
Requires: FFmpeg on PATH OR imageio-ffmpeg (bundled FFmpeg from render script deps).

Writes:
  artifacts/video_v21/voiceover/narration_v21.wav
  artifacts/video_v21/ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4

Usage:
  python tools/synthesize_voiceover_v21.py
  python tools/synthesize_voiceover_v21.py --voice en-US-GuyNeural --rate -4%
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import subprocess
from pathlib import Path

try:
    import edge_tts
except ImportError as exc:
    raise SystemExit(
        "Missing edge-tts. Install with:\n  python -m pip install edge-tts\n"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "video_v21"
VO_DIR = OUT_DIR / "voiceover"
VIDEO_SILENT = OUT_DIR / "ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo.mp4"
VIDEO_VOICE = OUT_DIR / "ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo_with_voiceover.mp4"
FULL_WAV = VO_DIR / "narration_v21.wav"


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def resolve_ffprobe() -> str | None:
    """imageio_ffmpeg bundles ffmpeg but often omits ffprobe use PATH or dir lookup."""
    fe = Path(ffmpeg_exe()).resolve()
    name = "ffprobe.exe" if fe.suffix.lower() == ".exe" else "ffprobe"
    candidate = fe.with_name(name)
    if candidate.is_file():
        return str(candidate)
    which = shutil.which(name)
    return which


def _duration_from_ffmpeg_stderr(stderr: str) -> float:
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", stderr)
    if not m:
        raise RuntimeError("Could not parse duration from ffmpeg -i output")
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


def ffprobe_duration(path: Path) -> float:
    probe = resolve_ffprobe()
    if probe:
        cmd = [
            probe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ]
        try:
            raw = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
            return float(json.loads(raw)["format"]["duration"])
        except (FileNotFoundError, subprocess.CalledProcessError, KeyError, ValueError):
            pass
    ff = ffmpeg_exe()
    proc = subprocess.run(
        [ff, "-hide_banner", "-nostdin", "-i", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
        check=False,
    )
    return _duration_from_ffmpeg_stderr(proc.stderr or "")


def tts_normalize(text: str) -> str:
    """Speak ROS topics and paths clearly."""
    text = text.replace("/fused_tracks", "fused-tracks topic")
    text = text.replace("/mesh/fob_status", "mesh slash fob status")
    text = text.replace("/payload/micro_deployment", "payload slash micro deployment")
    text = text.replace("/effector/selected_plan", "effector selected plan topic")
    text = text.replace("/cognitive_ew_commands", "cognitive E W commands")
    text = text.replace("clearsky_os_basic_demo.launch.py", "clearsky os basic demo launch file")
    text = text.replace("LRBAA", "Ell Are Bee Ay Ay")
    text = text.replace("BORAP", "Bow Rap")
    text = text.replace("UAS", "U A S")
    text = text.replace("C-UAS", "Counter U A S")
    text = text.replace("ROS", "Ross")
    text = text.replace("DARKSPACE", "Darkspace")
    text = text.replace("/darkspace/status", "darkspace status topic")
    text = text.replace("/audit/events", "audit events topic")
    text = re.sub(r"[/_]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# (start_sec, end_sec, on_screen_subtitle_style, spoken_text)
# spoken_text omitted where same as subtitle after normalize
SEGMENTS: list[tuple[float, float, str, str | None]] = [
    (
        0,
        15,
        "",
        (
            "ClearSky OS version two dot one is Ross Two counter U A S integration software framed for "
            "D H S Science and Technology L R B A A twenty four oh one and topic B O R A P zero four: "
            "Countering Unmanned Aircraft Systems. Everything shown here is demonstrated in simulation only."
        ),
    ),
    (
        15,
        30,
        "",
        (
            "The release configures two to four scout motherships acting as mobile Forward Operating Bases "
            "within one operational area, exchanging mesh style telemetry for reviewer inspection."
        ),
    ),
    (
        30,
        48,
        "",
        (
            "Each mothership exposes a modular micro payload bay modeled at ten to twelve slots. "
            "Representative payloads are a sensor extension pod, an acoustic disruption module, "
            "a kevlar web deployer, a cognitive electronic warfare pod, and one reserved kinetic ram slot, all simulation."
        ),
    ),
    (
        48,
        68,
        "",
        (
            "Reviewers reconstruct the authoritative demo using the Linux container workflow: "
            "clean build dot sh, source the workspace, then launch clearsky os basic demo. No Windows native build is required."
        ),
    ),
    (
        68,
        88,
        "",
        (
            "Simulated modalities produce structured fused tracks with confidence, modality coverage, "
            "and safety metadata so operators can review evidence without claiming field sensor performance."
        ),
    ),
    (
        88,
        108,
        "",
        (
            "Forward operating base coordination publishes on mesh fob status and payload micro deployment, "
            "including advisory effector alignment cues so simulated inventory aligns with layered policy."
        ),
    ),
    (
        108,
        128,
        "",
        (
            "The software assumes non kinetic responses first: monitor posture, deception, cognitive jam concepts, "
            "navigation link spoofing concepts, directed energy stubs, and dual approved takeover pathways before any kinetic story."
        ),
    ),
    (
        128,
        148,
        "",
        (
            "Kamikaze ram appears only as a last resort kinetic energy simulation. Default policy disables it "
            "and mandates paired operator authorization alongside open safety predicates."
        ),
    ),
    (
        148,
        168,
        "",
        (
            "Darkspace summarizes audit continuity across published events: integrity o k and chain gap count metrics "
            "support supervisory review alongside other Ross topics."
        ),
    ),
    (
        168,
        188,
        "",
        (
            "The effector planner publishes the selected plan document with explanatory rationale "
            "and explicit monitor only flags so evaluators see human governed layering at the wire protocol."
        ),
    ),
    (
        188,
        210,
        "",
        (
            "Open Ross interfaces underpin a disciplined transition: representative feeds today, "
            "laboratory S D R bring up, and marketplace style packaging for repeatable government evaluation."
        ),
    ),
    (
        210,
        240,
        "",
        (
            "ClearSky OS version two dot one remains simulation honest, authority preserving, immutable on the audit spine, "
            "and intentionally modest in claims. Licensed Apache two point zero by Fratres X A I."
        ),
    ),
]


async def synth_segment_mp3(text: str, out_mp3: Path, voice: str, rate: str) -> None:
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(out_mp3))


def _atempo_chain(desired_ratio: float) -> str:
    """desired_ratio = input_duration / desired_output_duration (speak faster if > 1)."""
    filt: list[str] = []
    ratio = desired_ratio
    while ratio > 2.0:
        filt.append("atempo=2.0")
        ratio /= 2.0
    while ratio < 0.5:
        filt.append("atempo=0.5")
        ratio /= 0.5
    if abs(ratio - 1.0) > 1e-3:
        r = min(max(ratio, 0.501), 1.999)
        filt.append(f"atempo={r:.6f}")
    return ",".join(filt) if filt else "anull"


def fit_segment_audio(in_mp3: Path, target_sec: float, out_wav: Path) -> None:
    """Stretch or pad narration to exactly target_sec for seamless concat."""
    actual = ffprobe_duration(in_mp3)
    ff = ffmpeg_exe()
    if actual <= 0:
        raise RuntimeError(f"Bad duration for {in_mp3}")
    ratio = actual / target_sec

    tmp = out_wav.with_suffix(".tmp.wav")

    subprocess.run(
        [
            ff,
            "-y",
            "-i",
            str(in_mp3),
            "-af",
            _atempo_chain(ratio),
            "-ar",
            "48000",
            "-ac",
            "2",
            str(tmp),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    stretched = ffprobe_duration(tmp)

    if stretched > target_sec + 0.05:
        subprocess.run(
            [
                ff,
                "-y",
                "-i",
                str(tmp),
                "-t",
                f"{target_sec:.3f}",
                "-ar",
                "48000",
                "-ac",
                "2",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif stretched < target_sec - 0.05:
        pad = target_sec - stretched
        subprocess.run(
            [
                ff,
                "-y",
                "-i",
                str(tmp),
                "-af",
                f"apad=pad_dur={pad:.4f}",
                "-t",
                f"{target_sec:.3f}",
                "-ar",
                "48000",
                "-ac",
                "2",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        shutil.move(str(tmp), str(out_wav))
        return

    if tmp.exists():
        tmp.unlink()


def concat_wavs(paths: list[Path], out_path: Path) -> None:
    ff = ffmpeg_exe()
    concat_file = VO_DIR / "concat_list.txt"
    lines = [f"file '{p.as_posix()}'\n" for p in paths]
    concat_file.write_text("".join(lines), encoding="utf-8")
    subprocess.run(
        [
            ff,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:a",
            "pcm_s24le",
            str(out_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def mux_voiceover(video: Path, wav: Path, out_mp4: Path) -> None:
    ff = ffmpeg_exe()
    subprocess.run(
        [
            ff,
            "-y",
            "-i",
            str(video),
            "-i",
            str(wav),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_mp4),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default="en-US-GuyNeural")
    parser.add_argument("--rate", default="-5%")
    parser.add_argument("--skip-video", action="store_true", help="Only build WAV")
    args = parser.parse_args()

    if not VIDEO_SILENT.exists():
        raise SystemExit(
            f"Missing silent video: {VIDEO_SILENT}\nRun: python tools/render_clearsky_os_v21_video.py first."
        )

    VO_DIR.mkdir(parents=True, exist_ok=True)
    wav_parts: list[Path] = []

    async def build_all() -> None:
        for i, (t0, t1, subtitle, spoken) in enumerate(SEGMENTS):
            target = round(t1 - t0, 3)
            text = spoken.strip() if spoken else tts_normalize(subtitle)
            raw_mp3 = VO_DIR / f"seg_{i:02d}_raw.mp3"
            part_wav = VO_DIR / f"seg_{i:02d}.wav"
            await synth_segment_mp3(text, raw_mp3, args.voice, args.rate)
            fit_segment_audio(raw_mp3, target, part_wav)
            wav_parts.append(part_wav)

    asyncio.run(build_all())

    concat_wavs(wav_parts, FULL_WAV)
    print("Wrote", FULL_WAV)

    if not args.skip_video:
        mux_voiceover(VIDEO_SILENT, FULL_WAV, VIDEO_VOICE)
        print("Wrote", VIDEO_VOICE)


if __name__ == "__main__":
    main()
