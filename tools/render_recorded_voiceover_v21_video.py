#!/usr/bin/env python3
r"""Render an Ancile Aeris v2.1 video paced to a recorded voiceover WAV.

Default voiceover:
  C:\Users\Besn Daddy\Downloads\NoteGPT_Speech_1778252509802.wav

The older renderer uses a fixed 4:00 grid. This renderer uses the WAV duration
as the source of truth and distributes shot/subtitle windows over that runtime.
"""

from __future__ import annotations

import argparse
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

import render_ancile_aeris_v21_video as base


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "video_v21"
KEY_DIR = OUT_DIR / "recorded_voiceover_keyframes"
REPO_VOICEOVER = OUT_DIR / "recorded_voiceover" / "NoteGPT_Speech_1778252509802.wav"
DEFAULT_VOICEOVER = REPO_VOICEOVER if REPO_VOICEOVER.exists() else Path(r"C:\Users\Besn Daddy\Downloads\NoteGPT_Speech_1778252509802.wav")
OUTPUT = OUT_DIR / "Ancile_Aeris_v2.1_LRBAA_BORAP_04_recorded_voiceover_demo.mp4"

FPS = 24


def audio_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def slide_opening() -> Image.Image:
    img = base.bg("Ancile Aeris v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((68, 235), "Complete ROS 2 Counter-UAS Software Demonstration", font=base.H1, fill=base.GOLD)
    base.text_box(
        d,
        (70, 360, 900, 690),
        "Submission Context",
        "DHS S&T LRBAA 24-01\nBORAP 04: Countering UAS\nDetect | Track | Identify | Mitigate",
        base.BLUE,
    )
    base.text_box(
        d,
        (980, 360, 1780, 690),
        "Boundary",
        "Simulation-only demonstration\nHuman-governed\nAuditable ROS 2 topics\nNo autonomous engagement",
        base.GREEN,
    )
    d.text((70, 780), "Property of Fratres X AI | github.com/FratresMedAI/Ancile-Aeris", font=base.BODY, fill=base.WHITE)
    return img


def slide_mission() -> Image.Image:
    img = base.bg("Mission Workflow")
    d = ImageDraw.Draw(img, "RGBA")
    items = [
        ("Detect", "simulated visual\nthermal | RF | acoustic", base.GREEN),
        ("Track", "fused state\nconfidence scoring", base.BLUE),
        ("Identify", "operator-reviewable\nclassification context", base.GOLD),
        ("Mitigate", "non-kinetic first\nhuman authorization", base.GREEN),
    ]
    x = 100
    for title, body, accent in items:
        base.text_box(d, (x, 350, x + 390, 675), title, body, accent)
        x += 430
    d.text(
        (115, 760),
        "Dense urban venues | mass gatherings | critical infrastructure | border-adjacent security contexts",
        font=base.H2,
        fill=base.WHITE,
    )
    return img


def slide_fob_swarm() -> Image.Image:
    img = base.bg("Mothership Forward Operating Base Swarm")
    d = ImageDraw.Draw(img, "RGBA")
    nodes = [(430, 390, "mhs-001"), (810, 275, "mhs-002"), (1190, 450, "mhs-003"), (1480, 315, "mhs-004")]
    base.draw_network(d, nodes)
    base.text_box(
        d,
        (95, 735, 1810, 910),
        "Operational Model",
        "1-4 scout motherships act as mobile Forward Operating Bases in one operational area with mesh-visible status.",
        base.GOLD,
    )
    return img


def slide_payloads() -> Image.Image:
    return base.slide_03()


def slide_docker() -> Image.Image:
    return base.slide_04()


def slide_fused_tracks() -> Image.Image:
    img = base.bg("Simulated Evidence to /fused_tracks")
    d = ImageDraw.Draw(img, "RGBA")
    labels = ["visual", "thermal", "acoustic", "RF", "lidar"]
    for i, label in enumerate(labels):
        x = 120 + i * 315
        base.text_box(d, (x, 285, x + 260, 460), label.upper(), "sim feed", base.BLUE)
        d.line((x + 130, 475, 960, 650), fill=base.GOLD + (190,), width=4)
    base.text_box(
        d,
        (545, 635, 1375, 855),
        "/fused_tracks",
        "machine-readable confidence\nmodality coverage\nclear track state information",
        base.GREEN,
    )
    return img


def slide_fob_topics() -> Image.Image:
    return base.slide_06()


def slide_non_kinetic() -> Image.Image:
    return base.slide_07()


def slide_kamikaze_locked() -> Image.Image:
    return base.slide_08()


def slide_darkspace() -> Image.Image:
    return base.slide_09()


def slide_effector_plan() -> Image.Image:
    return base.slide_10()


def slide_cognitive_ew() -> Image.Image:
    img = base.bg("Cognitive EW Commands with XAI")
    d = ImageDraw.Draw(img, "RGBA")
    base.terminal_box(
        d,
        (130, 260, 1790, 860),
        [
            "/cognitive_ew_commands",
            "{",
            '  "selected_effector_mode": "cognitive_jamming",',
            '  "effector_plan_id": "plan-042",',
            '  "xai_rationale": "operator-reviewable modeled response",',
            '  "audit_visible": true',
            "}",
        ],
    )
    return img


def slide_transition() -> Image.Image:
    return base.slide_11()


def slide_interoperability() -> Image.Image:
    img = base.bg("Interoperability Context References")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(d, (90, 290, 900, 510), "Context Only", "Anduril Lattice-style overlays\nJIATF-401 Marketplace sourcing idiom\nReplicator 2 velocity doctrine analogue", base.BLUE)
    base.text_box(d, (1020, 290, 1830, 510), "Modeled, Not Hardware", "Leonidas-class HPM wording confined to stub\nFortem DroneHunter naming as optional third-party illustrative geometry", base.GOLD)
    base.text_box(
        d,
        (170, 660, 1750, 850),
        "Non-Endorsement",
        "References are alignment examples only; no integration, endorsement, or fielded hardware claim is made.",
        base.GREEN,
    )
    return img


def slide_close() -> Image.Image:
    img = base.bg("Ancile Aeris v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((90, 280), "Simulation-honest. Human-governed. Fully auditable.", font=base.H1, fill=base.GOLD)
    d.text((90, 390), "Ready for LRBAA reviewer inspection.", font=base.H2, fill=base.WHITE)
    d.text((90, 490), "Thank you for your time and service.", font=base.H2, fill=base.BLUE)
    base.text_box(
        d,
        (90, 650, 1830, 835),
        "Disclaimer",
        "Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.",
        base.GOLD,
    )
    return img


SLIDES = [
    ("01_opening.png", slide_opening),
    ("02_mission_workflow.png", slide_mission),
    ("03_fob_swarm_1_to_4.png", slide_fob_swarm),
    ("04_micro_payload_catalog.png", slide_payloads),
    ("05_docker_launch.png", slide_docker),
    ("06_fused_tracks.png", slide_fused_tracks),
    ("07_fob_topics.png", slide_fob_topics),
    ("08_non_kinetic_first.png", slide_non_kinetic),
    ("09_kamikaze_locked.png", slide_kamikaze_locked),
    ("10_darkspace_status.png", slide_darkspace),
    ("11_effector_selected_plan.png", slide_effector_plan),
    ("12_cognitive_ew_commands.png", slide_cognitive_ew),
    ("13_transition_path.png", slide_transition),
    ("14_interoperability_context.png", slide_interoperability),
    ("15_closing.png", slide_close),
]


SEGMENT_TEXT = [
    "Ancile Aeris v2.1 is a complete ROS 2 counter-UAS software demonstration for DHS S&T LRBAA 24-01 and BORAP 04.",
    "Detect, track, identify, and mitigate workflows are shown for urban venues, mass gatherings, critical infrastructure, and border-adjacent contexts. Simulation only.",
    "The current build introduces a mothership Forward Operating Base swarm: 1 to 4 scout motherships inside one operational area.",
    "Each mothership carries a representative 10-to-12-slot modular micro-drone bay: sensor, acoustic, kevlar web, cognitive EW, and reserved kamikaze ram.",
    "The standard launch remains the Docker-only ROS 2 demo.",
    "Simulated multi-modal evidence fuses into /fused_tracks with confidence scores, modality coverage, and track state.",
    "FOB coordination is visible on /mesh/fob_status and /payload/micro_deployment.",
    "Non-kinetic-first doctrine prioritizes monitor mode, deception, cognitive jamming, GNSS or link spoofing, HPM modeling, and authorized takeover concepts.",
    "Kamikaze ram is last-resort kinetic-energy simulation, disabled by default, with safety gate approval and paired human authorization.",
    "DARKSPACE records audit events and publishes /darkspace/status with integrity_ok true and chain_gap_count zero.",
    "/effector/selected_plan publishes chosen mode, rationale, authorization state, and monitor-only flag: advanced layered response modeling, not autonomous engagement.",
    "/cognitive_ew_commands carries comparable XAI fields to keep operator review and auditability visible.",
    "The transition path starts with open ROS 2 interfaces, moves toward SDR lab integration, and supports marketplace-style modular packaging.",
    "Interoperability references are context only: Lattice-style overlays, JIATF-401 Marketplace, Replicator 2, Leonidas-class HPM wording as stub, and optional DroneHunter naming.",
    "Ancile Aeris v2.1 is simulation honest, human governed, fully auditable, and ready for LRBAA reviewer inspection. Thank you for your time and service.",
]


def segment_windows(total_seconds: float) -> list[tuple[float, float, str]]:
    weights = [max(6, len(text.split())) for text in SEGMENT_TEXT]
    total_weight = sum(weights)
    starts: list[float] = [0.0]
    acc = 0.0
    for weight in weights[:-1]:
        acc += total_seconds * (weight / total_weight)
        starts.append(acc)
    ends = starts[1:] + [total_seconds]
    return [(s, e, text) for s, e, text in zip(starts, ends, SEGMENT_TEXT)]


def make_keyframes(windows: list[tuple[float, float, str]]) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for (name, func), (_, _, subtitle) in zip(SLIDES, windows):
        img = func()
        base.draw_subtitle(img, subtitle)
        path = KEY_DIR / name
        img.save(path)
        paths.append(path)
    return paths


def _concat_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "'\\''")


def render_video(image_paths: list[Path], voiceover: Path, output: Path, total_seconds: float) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    windows = segment_windows(total_seconds)
    concat_path = OUT_DIR / "recorded_voiceover_concat.txt"
    lines: list[str] = []
    for path, (start, end, _) in zip(image_paths, windows):
        lines.append(f"file '{_concat_path(path)}'\n")
        lines.append(f"duration {max(end - start, 0.1):.3f}\n")
    # The concat demuxer needs the last image repeated to honor its duration.
    lines.append(f"file '{_concat_path(image_paths[-1])}'\n")
    concat_path.write_text("".join(lines), encoding="utf-8")
    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-i",
        str(voiceover),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-vf",
        f"fps={FPS},format=yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output),
    ]
    print(f"Rendering {output} ({total_seconds:.3f}s, {FPS} fps)...")
    subprocess.run(cmd, check=True)
    print("Done:", output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voiceover", type=Path, default=DEFAULT_VOICEOVER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    if not args.voiceover.is_file():
        raise SystemExit(f"Missing voiceover WAV: {args.voiceover}")

    total_seconds = audio_duration(args.voiceover)
    windows = segment_windows(total_seconds)
    image_paths = make_keyframes(windows)
    render_video(image_paths, args.voiceover, args.output, total_seconds)


if __name__ == "__main__":
    main()
