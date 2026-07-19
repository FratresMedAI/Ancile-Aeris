#!/usr/bin/env python3
r"""Render an ClearSky OS v2.1 video paced to a recorded voiceover WAV.

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

import render_clearsky_os_v21_video as base


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "video_v21"
KEY_DIR = OUT_DIR / "recorded_voiceover_keyframes"
CONCEPT_DIR = OUT_DIR / "concept_renders"
REPO_VOICEOVER = OUT_DIR / "recorded_voiceover" / "NoteGPT_Speech_1778252509802.wav"
DEFAULT_VOICEOVER = REPO_VOICEOVER if REPO_VOICEOVER.exists() else Path(r"C:\Users\Besn Daddy\Downloads\NoteGPT_Speech_1778252509802.wav")
OUTPUT = OUT_DIR / "ClearSky_OS_v2.1_LRBAA_BORAP_04_recorded_voiceover_demo.mp4"

FPS = 24


def audio_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def concept_bg(image_name: str, title: str, kicker: str = "ClearSky OS v2.1 | LRBAA BORAP 04 | Simulation Only") -> Image.Image:
    """Use cinematic concept art as the base while keeping submission guardrails visible."""
    path = CONCEPT_DIR / image_name
    if not path.is_file():
        return base.bg(title, kicker)

    src = Image.open(path).convert("RGB")
    src_ratio = src.width / src.height
    dst_ratio = base.WIDTH / base.HEIGHT
    if src_ratio > dst_ratio:
        new_h = base.HEIGHT
        new_w = int(new_h * src_ratio)
    else:
        new_w = base.WIDTH
        new_h = int(new_w / src_ratio)
    img = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - base.WIDTH) // 2
    top = (new_h - base.HEIGHT) // 2
    img = img.crop((left, top, left + base.WIDTH, top + base.HEIGHT))

    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, base.WIDTH, 118), fill=(3, 8, 16, 150))
    d.rectangle((0, base.HEIGHT - 190, base.WIDTH, base.HEIGHT), fill=(3, 8, 16, 135))
    d.text((46, 28), kicker, font=base.TINY, fill=(210, 220, 232))
    d.text((46, 56), title, font=base.H2, fill=base.WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
    d.line((46, 118, base.WIDTH - 46, 118), fill=base.GOLD + (190,), width=2)
    d.text((46, base.HEIGHT - 36), "Simulation-only C-UAS defensive demonstration. No autonomous weapon release.", font=base.TINY, fill=base.MUTED)
    return img


def caption(frame: Image.Image, text: str) -> None:
    """Smaller caption bar for recorded narration; visuals should carry the frame."""
    if not text:
        return
    d = ImageDraw.Draw(frame, "RGBA")
    lines = base.wrap(d, text, 1320, base.TINY)
    line_h = 28
    box_h = min(len(lines), 4) * line_h + 34
    y1 = base.HEIGHT - box_h - 54
    x1, x2 = 300, base.WIDTH - 300
    d.rounded_rectangle((x1, y1, x2, y1 + box_h), radius=16, fill=(0, 0, 0, 142), outline=base.GOLD + (130,), width=2)
    y = y1 + 17
    for line in lines[:4]:
        bbox = d.textbbox((0, 0), line, font=base.TINY)
        d.text(((base.WIDTH - (bbox[2] - bbox[0])) // 2, y), line, font=base.TINY, fill=base.WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
        y += line_h


def slide_opening() -> Image.Image:
    img = concept_bg("01_mothership_fob_swarm.png", "ClearSky OS v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((70, 165), "Complete ROS 2 Counter-UAS Software Demonstration", font=base.H1, fill=base.GOLD, stroke_width=2, stroke_fill=(0, 0, 0))
    base.text_box(
        d,
        (70, 300, 820, 570),
        "Submission Context",
        "DHS S&T LRBAA 24-01\nBORAP 04: Countering UAS\nDetect | Track | Identify | Mitigate",
        base.BLUE,
    )
    base.text_box(
        d,
        (1030, 300, 1780, 570),
        "Boundary",
        "Simulation-only demonstration\nHuman-governed\nAuditable ROS 2 topics\nNo autonomous engagement",
        base.GREEN,
    )
    d.text((70, 780), "Property of Fratres X AI | github.com/Fratres-X-AI/ClearSky-OS", font=base.BODY, fill=base.WHITE)
    return img


def slide_mission() -> Image.Image:
    img = concept_bg("03_fusion_darkspace_cop.png", "Detect -> Track -> Identify -> Mitigate")
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
    img = concept_bg("01_mothership_fob_swarm.png", "Mothership Forward Operating Base Swarm")
    d = ImageDraw.Draw(img, "RGBA")
    nodes = [(430, 390, "mhs-001"), (810, 275, "mhs-002"), (1190, 450, "mhs-003"), (1480, 315, "mhs-004")]
    base.text_box(
        d,
        (95, 750, 1810, 910),
        "Operational Model",
        "1-4 scout motherships act as mobile Forward Operating Bases in one operational area with mesh-visible status.",
        base.GOLD,
    )
    return img


def slide_payloads() -> Image.Image:
    img = concept_bg("02_micro_payload_bay.png", "Modular Micro-Drone Payload Bay")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(
        d,
        (95, 745, 1810, 895),
        "Representative Inventory",
        "10-12 hot-swappable slots: sensor pod, acoustic disruptor, kevlar web deployer, cognitive EW pod, and locked kamikaze ram reserve.",
        base.GOLD,
    )
    return img


def slide_docker() -> Image.Image:
    return base.slide_04()


def slide_fused_tracks() -> Image.Image:
    img = concept_bg("03_fusion_darkspace_cop.png", "Simulated Evidence to /fused_tracks")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(
        d,
        (90, 735, 980, 900),
        "/fused_tracks",
        "machine-readable confidence\nmodality coverage\nclear track state information",
        base.GREEN,
    )
    return img


def slide_fob_topics() -> Image.Image:
    img = concept_bg("01_mothership_fob_swarm.png", "FOB Coordination Topics")
    d = ImageDraw.Draw(img, "RGBA")
    base.terminal_box(
        d,
        (70, 675, 905, 915),
        [
            "/mesh/fob_status",
            '  "fleet": ["mhs-001", "mhs-002", "mhs-003"]',
            '  "micro_capacity": 12',
        ],
    )
    base.terminal_box(
        d,
        (1015, 675, 1850, 915),
        [
            "/payload/micro_deployment",
            '  "hot_swap": true',
            '  "effector_alignment": "non_kinetic"',
        ],
    )
    return img


def slide_non_kinetic() -> Image.Image:
    return concept_bg("04_non_kinetic_gates.png", "Non-Kinetic-First Doctrine")


def slide_kamikaze_locked() -> Image.Image:
    img = concept_bg("04_non_kinetic_gates.png", "Kamikaze Ram: Locked Last-Resort Simulation")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(
        d,
        (985, 725, 1810, 905),
        "Gates Required",
        "safety gate approval\npaired human authorization\ndisabled by default",
        base.RED,
    )
    return img


def slide_darkspace() -> Image.Image:
    img = concept_bg("03_fusion_darkspace_cop.png", "DARKSPACE Audit Status")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(
        d,
        (995, 720, 1810, 900),
        "/darkspace/status",
        "integrity_ok: true\nchain_gap_count: 0\naudit events recorded",
        base.GREEN,
    )
    return img


def slide_effector_plan() -> Image.Image:
    img = concept_bg("03_fusion_darkspace_cop.png", "Effector Selected Plan")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(
        d,
        (90, 720, 1025, 900),
        "/effector/selected_plan",
        "chosen mode | rationale | authorization state | monitor-only flag",
        base.GOLD,
    )
    return img


def slide_cognitive_ew() -> Image.Image:
    img = concept_bg("03_fusion_darkspace_cop.png", "Cognitive EW Commands with XAI")
    d = ImageDraw.Draw(img, "RGBA")
    base.terminal_box(
        d,
        (820, 610, 1810, 900),
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
    img = concept_bg("03_fusion_darkspace_cop.png", "Disciplined Transition Path")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(d, (90, 680, 570, 900), "Today", "open ROS 2 interfaces\nsimulation demo\naudit topics", base.GREEN)
    base.text_box(d, (720, 680, 1200, 900), "Later", "SDR laboratory integration\nrepresentative feeds\nbench validation", base.GOLD)
    base.text_box(d, (1340, 680, 1820, 900), "Packaging", "marketplace-style\nmodular government evaluation", base.BLUE)
    return img


def slide_interoperability() -> Image.Image:
    img = concept_bg("01_mothership_fob_swarm.png", "Interoperability Context References")
    d = ImageDraw.Draw(img, "RGBA")
    base.text_box(d, (90, 650, 900, 835), "Context Only", "Anduril Lattice-style overlays\nJIATF-401 Marketplace sourcing idiom\nReplicator 2 velocity doctrine analogue", base.BLUE)
    base.text_box(d, (1020, 650, 1830, 835), "Modeled, Not Hardware", "Leonidas-class HPM wording confined to stub\nFortem DroneHunter naming as optional third-party illustrative geometry", base.GOLD)
    base.text_box(
        d,
        (300, 865, 1620, 985),
        "Non-Endorsement",
        "References are alignment examples only; no integration, endorsement, or fielded hardware claim is made.",
        base.GREEN,
    )
    return img


def slide_close() -> Image.Image:
    img = concept_bg("01_mothership_fob_swarm.png", "ClearSky OS v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((90, 270), "Simulation-honest. Human-governed. Fully auditable.", font=base.H1, fill=base.GOLD, stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((90, 380), "Ready for LRBAA reviewer inspection.", font=base.H2, fill=base.WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((90, 480), "Thank you for your time and service.", font=base.H2, fill=base.BLUE, stroke_width=2, stroke_fill=(0, 0, 0))
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
    "ClearSky OS v2.1 is a complete ROS 2 counter-UAS software demonstration for DHS S&T LRBAA 24-01 and BORAP 04.",
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
    "ClearSky OS v2.1 is simulation honest, human governed, fully auditable, and ready for LRBAA reviewer inspection. Thank you for your time and service.",
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
        caption(img, subtitle)
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
