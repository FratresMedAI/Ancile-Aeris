from __future__ import annotations

import math
import subprocess
from pathlib import Path

try:
    import imageio_ffmpeg
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    print("Missing dependency:", exc)
    print("Install with: python -m pip install pillow numpy imageio-ffmpeg")
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "video_v21"
KEY_DIR = OUT_DIR / "keyframes"
OUTPUT = OUT_DIR / "ClearSky_OS_v2.1_LRBAA_BORAP_04_4min_demo.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 24
TOTAL_SECONDS = 240
CROSSFADE_SECONDS = 1.0

NAVY = (8, 18, 34)
NAVY2 = (13, 32, 58)
GOLD = (220, 176, 77)
BLUE = (72, 151, 220)
GREEN = (87, 190, 135)
RED = (202, 87, 86)
WHITE = (235, 242, 250)
MUTED = (155, 170, 188)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


TITLE = font(72, True)
H1 = font(54, True)
H2 = font(40, True)
BODY = font(32)
SMALL = font(24)
TINY = font(20)
MONO = font(28)


def bg(title: str, kicker: str = "ClearSky OS v2.1 | LRBAA BORAP 04 | Simulation Only") -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(0, WIDTH, 96):
        d.line((i, 0, i - 420, HEIGHT), fill=(255, 255, 255, 9), width=1)
    d.rectangle((0, 0, WIDTH, 100), fill=(5, 13, 25, 220))
    d.text((60, 28), kicker, font=SMALL, fill=(220, 226, 235))
    d.line((60, 104, WIDTH - 60, 104), fill=GOLD + (210,), width=3)
    d.text((60, 132), title, font=TITLE, fill=WHITE)
    d.text((60, HEIGHT - 58), "Simulation-only C-UAS defensive demonstration. No autonomous weapon release.", font=SMALL, fill=MUTED)
    return img


def text_box(d: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, body: str, accent=BLUE) -> None:
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=22, fill=(14, 33, 58, 230), outline=accent + (230,), width=3)
    d.text((x1 + 28, y1 + 22), title, font=H2, fill=accent)
    y = y1 + 82
    for line in body.split("\n"):
        d.text((x1 + 28, y), line, font=BODY, fill=WHITE)
        y += 42


def terminal_box(d: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], lines: list[str]) -> None:
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=20, fill=(3, 8, 14, 245), outline=(80, 95, 120, 230), width=2)
    d.ellipse((x1 + 22, y1 + 20, x1 + 38, y1 + 36), fill=(255, 95, 86))
    d.ellipse((x1 + 48, y1 + 20, x1 + 64, y1 + 36), fill=(255, 189, 46))
    d.ellipse((x1 + 74, y1 + 20, x1 + 90, y1 + 36), fill=(39, 201, 63))
    y = y1 + 64
    for line in lines:
        d.text((x1 + 28, y), line, font=MONO, fill=(200, 235, 210) if line.startswith("$") else (210, 220, 235))
        y += 38


def draw_network(d: ImageDraw.ImageDraw, nodes: list[tuple[int, int, str]], color=BLUE) -> None:
    for i, (x, y, _) in enumerate(nodes):
        for x2, y2, _ in nodes[i + 1 :]:
            d.line((x, y, x2, y2), fill=color + (110,), width=3)
    for x, y, label in nodes:
        d.ellipse((x - 42, y - 42, x + 42, y + 42), fill=(18, 48, 78), outline=GOLD, width=4)
        d.text((x - 34, y - 14), "FOB", font=SMALL, fill=WHITE)
        d.text((x - 56, y + 54), label, font=SMALL, fill=WHITE)


def slide_01() -> Image.Image:
    img = bg("ClearSky OS v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((68, 235), "Mothership FOB Swarm + Modular Micro-Payload Simulation", font=H1, fill=GOLD)
    text_box(d, (70, 360, 900, 680), "Submission Context", "DHS S&T LRBAA 24-01\nBORAP 04: Countering UAS\nDetect -> Track -> Identify -> Mitigate", BLUE)
    text_box(d, (980, 360, 1780, 680), "Safety Posture", "Non-kinetic first\nDARKSPACE audited\nHuman authority preserved\nSimulation only", GREEN)
    d.text((70, 760), "Property of Fratres X AI | github.com/Fratres-X-AI/ClearSky-OS", font=BODY, fill=WHITE)
    return img


def slide_02() -> Image.Image:
    img = bg("Mothership FOB Swarm")
    d = ImageDraw.Draw(img, "RGBA")
    nodes = [(520, 440, "mhs-001"), (970, 300, "mhs-002"), (1320, 560, "mhs-003")]
    draw_network(d, nodes)
    text_box(d, (90, 740, 1810, 900), "Operational Model", "2-4 scout motherships act as mobile Forward Operating Bases in one operational area; each maintains mesh visibility and simulated payload inventory.", GOLD)
    return img


def slide_03() -> Image.Image:
    img = bg("Micro-Drone Payload Catalog")
    d = ImageDraw.Draw(img, "RGBA")
    cards = [
        ("Sensor Pod", "Multi-modal ISR\nextension", GREEN),
        ("Acoustic\nDisruptor", "Directional sound\nsimulation", BLUE),
        ("Kevlar Web", "Net entanglement\nrotor-stop model", GOLD),
        ("Cognitive EW", "SDR jamming /\nspoofing / takeover", BLUE),
        ("Kamikaze Ram", "Last resort kinetic\nsimulation only", RED),
    ]
    x = 90
    for title, body, accent in cards:
        text_box(d, (x, 330, x + 330, 710), title, body + "\n\nSIMULATION", accent)
        x += 355
    d.text((110, 795), "Representative bay: 10-12 modular, hot-swappable micro-drone slots per mothership.", font=H2, fill=WHITE)
    return img


def slide_04() -> Image.Image:
    img = bg("Docker-Only Clean Demo Launch")
    d = ImageDraw.Draw(img, "RGBA")
    terminal_box(
        d,
        (110, 310, 1810, 760),
        [
            "$ cd /opt/clearsky_os_ws",
            "$ ./clean-build.sh",
            "Summary: 17 packages finished",
            "$ source install/setup.bash",
            "$ ros2 launch clearsky_os_bringup clearsky_os_basic_demo.launch.py",
        ],
    )
    return img


def slide_05() -> Image.Image:
    img = bg("Detect -> Track -> Identify")
    d = ImageDraw.Draw(img, "RGBA")
    labels = ["Visual", "Thermal", "Acoustic", "RF", "Lidar"]
    for i, label in enumerate(labels):
        x = 130 + i * 310
        text_box(d, (x, 300, x + 250, 470), label, "sim feed", BLUE)
        d.line((x + 125, 480, 960, 650), fill=GOLD + (190,), width=4)
    text_box(d, (650, 650, 1270, 830), "/fused_tracks", "confidence | modalities | PID metadata | operator context", GREEN)
    return img


def slide_06() -> Image.Image:
    img = bg("FOB Status and Micro Deployment Topics")
    d = ImageDraw.Draw(img, "RGBA")
    terminal_box(
        d,
        (90, 270, 910, 850),
        [
            "/mesh/fob_status",
            "{",
            '  "profile": "mothership_fob_standard",',
            '  "fleet": ["mhs-001", "mhs-002", "mhs-003"],',
            '  "micro_capacity": 12',
            "}",
        ],
    )
    terminal_box(
        d,
        (1010, 270, 1830, 850),
        [
            "/payload/micro_deployment",
            "{",
            '  "hot_swap": true,',
            '  "effector_alignment": "non_kinetic_micro_emphasis",',
            '  "ready_sim": true',
            "}",
        ],
    )
    return img


def slide_07() -> Image.Image:
    img = bg("Non-Kinetic-First Doctrine")
    d = ImageDraw.Draw(img, "RGBA")
    steps = [
        ("1", "Monitor", GREEN),
        ("2", "Deception", GREEN),
        ("3", "Cognitive EW", GREEN),
        ("4", "GNSS / Link\nSpoofing", BLUE),
        ("5", "HPM Stub", BLUE),
        ("6", "Takeover\nConcept", GOLD),
        ("7", "Kamikaze Ram\nLast Resort", RED),
    ]
    x = 70
    for num, label, accent in steps:
        d.rounded_rectangle((x, 410, x + 230, 620), radius=20, fill=(15, 37, 65, 235), outline=accent, width=3)
        d.text((x + 28, 430), num, font=H1, fill=accent)
        d.text((x + 28, 520), label, font=SMALL, fill=WHITE)
        if x < 1530:
            d.line((x + 238, 515, x + 278, 515), fill=MUTED + (180,), width=4)
        x += 260
    d.text((92, 720), "Default policy excludes kinetic_ram; recommendations remain monitor-only absent safety and authorization predicates.", font=BODY, fill=WHITE)
    return img


def slide_08() -> Image.Image:
    img = bg("Kamikaze Ram: Locked Last-Resort Simulation")
    d = ImageDraw.Draw(img, "RGBA")
    text_box(d, (100, 310, 850, 760), "Gates Required", "1. Safety gate open\n2. Operator launch approval\n3. Terminal authorization\n4. Kinetic family enabled\n5. Simulation-only deploy command", RED)
    text_box(d, (970, 310, 1810, 760), "Default State", "kamikaze_ram.enabled: false\nallow_kinetic_ram_in_effector_policy: false\n/effector/kamikaze_authorized: false", GOLD)
    for x in [1240, 1400, 1560]:
        d.rounded_rectangle((x, 820, x + 90, 900), radius=12, outline=RED, width=4)
        d.arc((x + 20, 780, x + 70, 850), 180, 360, fill=RED, width=5)
    return img


def slide_09() -> Image.Image:
    img = bg("DARKSPACE Audit Status")
    d = ImageDraw.Draw(img, "RGBA")
    terminal_box(
        d,
        (180, 285, 1740, 820),
        [
            "/darkspace/status",
            "{",
            '  "integrity_ok": true,',
            '  "events_seen": 1463,',
            '  "chain_gap_count": 0,',
            '  "recent_components": ["fusion", "safety_gate", "fob_coordinator"]',
            "}",
        ],
    )
    return img


def slide_10() -> Image.Image:
    img = bg("Effector Plan with XAI")
    d = ImageDraw.Draw(img, "RGBA")
    terminal_box(
        d,
        (130, 260, 1790, 860),
        [
            "/effector/selected_plan",
            "{",
            '  "doctrine": "layered_non_kinetic_first",',
            '  "selected": {"mode": "cognitive_jamming", "monitor_only": true},',
            '  "xai": {"rationale": "adaptive RF denial recommendation"},',
            '  "policy": {"human_authorization_required": true}',
            "}",
        ],
    )
    return img


def slide_11() -> Image.Image:
    img = bg("Transition Roadmap")
    d = ImageDraw.Draw(img, "RGBA")
    text_box(d, (100, 330, 580, 720), "Today", "ROS 2 simulation\nDocker clean build\nAudited topics", GREEN)
    text_box(d, (720, 330, 1200, 720), "Phase I", "Representative feeds\nSDR lab bring-up\nTRL 5 target", GOLD)
    text_box(d, (1340, 330, 1820, 720), "Roadmap", "Closed-loop RF bench\nMarketplace packaging\nTRL 6 path", BLUE)
    d.line((590, 525, 710, 525), fill=MUTED + (180,), width=5)
    d.line((1210, 525, 1330, 525), fill=MUTED + (180,), width=5)
    return img


def slide_12() -> Image.Image:
    img = bg("ClearSky OS v2.1")
    d = ImageDraw.Draw(img, "RGBA")
    d.text((90, 280), "Simulation-honest. Human-governed. Auditable.", font=H1, fill=GOLD)
    d.text((90, 390), "Mothership FOB Swarm | Modular Micro-Payloads | Non-Kinetic First", font=H2, fill=WHITE)
    d.text((90, 485), "github.com/Fratres-X-AI/ClearSky-OS", font=H2, fill=BLUE)
    text_box(d, (90, 650, 1830, 835), "Disclaimer", "Simulation-only C-UAS defensive demonstration. No autonomous weapon release. Government and industry references are alignment examples only and do not imply endorsement.", GOLD)
    return img


SLIDES = [
    ("01_title_slate.png", slide_01),
    ("02_fob_mesh_swarm.png", slide_02),
    ("03_micro_payload_catalog.png", slide_03),
    ("04_docker_launch.png", slide_04),
    ("05_fusion_pipeline.png", slide_05),
    ("06_fob_topics.png", slide_06),
    ("07_non_kinetic_first.png", slide_07),
    ("08_kamikaze_gated.png", slide_08),
    ("09_darkspace_status.png", slide_09),
    ("10_effector_plan.png", slide_10),
    ("11_transition_roadmap.png", slide_11),
    ("12_closing_slate.png", slide_12),
]

SUBTITLES = [
    (0, 15, "ClearSky OS v2.1: ROS 2 counter-UAS software for LRBAA 24-01 and BORAP 04, demonstrated in simulation only."),
    (15, 30, "Two to four scout motherships operate as mobile Forward Operating Bases in a single operational area."),
    (30, 48, "Each mothership carries a 10-to-12-slot modular micro-drone bay: sensor, acoustic, web, cognitive EW, and gated kamikaze ram."),
    (48, 68, "The authoritative demo remains Docker-only: clean build, source the workspace, and launch clearsky_os_basic_demo."),
    (68, 88, "Simulated modality evidence fuses into /fused_tracks for operator situational awareness and review."),
    (88, 108, "/mesh/fob_status and /payload/micro_deployment expose the FOB fleet and simulated micro-payload inventory."),
    (108, 128, "Doctrine is non-kinetic first: monitor, deception, cognitive EW, spoofing concepts, HPM stub, and takeover concept."),
    (128, 148, "Kamikaze ram is last-resort kinetic-energy simulation only, disabled by default, and requires double human authorization."),
    (148, 168, "DARKSPACE records audit continuity and publishes integrity status for reviewer inspection."),
    (168, 188, "/effector/selected_plan carries selected mode, rationale, authorization state, and monitor-only posture."),
    (188, 210, "Open ROS 2 interfaces support SDR laboratory integration and marketplace-style modular transition."),
    (210, 240, "ClearSky OS v2.1 remains simulation-honest, human-governed, auditable, and ready for LRBAA reviewer inspection."),
]


def wrap(draw: ImageDraw.ImageDraw, text: str, max_width: int, face: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=face)[2] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def subtitle_at(t: float) -> str:
    for start, end, text in SUBTITLES:
        if start <= t < end:
            return text
    return ""


def draw_subtitle(frame: Image.Image, text: str) -> None:
    if not text:
        return
    d = ImageDraw.Draw(frame, "RGBA")
    lines = wrap(d, text, 1500, H2)
    line_h = 52
    box_h = len(lines) * line_h + 50
    y1 = HEIGHT - box_h - 58
    d.rounded_rectangle((160, y1, WIDTH - 160, y1 + box_h), radius=22, fill=(0, 0, 0, 188), outline=GOLD + (220,), width=3)
    y = y1 + 24
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=H2)
        d.text(((WIDTH - (bbox[2] - bbox[0])) // 2, y), line, font=H2, fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))
        y += line_h


def make_keyframes() -> list[Image.Image]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    for name, func in SLIDES:
        img = func()
        img.save(KEY_DIR / name)
        frames.append(img)
    return frames


def frame_at(t: float, images: list[Image.Image]) -> Image.Image:
    shot_seconds = TOTAL_SECONDS / len(images)
    idx = min(int(t // shot_seconds), len(images) - 1)
    local = t - idx * shot_seconds
    base = images[idx]
    if idx > 0 and local < CROSSFADE_SECONDS:
        alpha = local / CROSSFADE_SECONDS
        frame = Image.blend(images[idx - 1], base, alpha)
    else:
        frame = base.copy()
    progress = min(max(local / shot_seconds, 0), 1)
    zoom = 1.0 + 0.018 * progress
    zw, zh = int(WIDTH / zoom), int(HEIGHT / zoom)
    left, top = (WIDTH - zw) // 2, (HEIGHT - zh) // 2
    frame = frame.crop((left, top, left + zw, top + zh)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    draw_subtitle(frame, subtitle_at(t))
    return frame


def render_video(images: list[Image.Image]) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(OUTPUT),
    ]
    print(f"Rendering {OUTPUT} ({TOTAL_SECONDS}s, {FPS} fps)...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    total_frames = TOTAL_SECONDS * FPS
    try:
        for frame_idx in range(total_frames):
            t = frame_idx / FPS
            proc.stdin.write(np.asarray(frame_at(t, images), dtype=np.uint8).tobytes())
            if frame_idx % (FPS * 15) == 0:
                print(f"  {int(t):03d}s / {TOTAL_SECONDS}s")
    finally:
        proc.stdin.close()
    code = proc.wait()
    if code != 0:
        raise SystemExit(code)
    print("Done:", OUTPUT)


def main() -> None:
    images = make_keyframes()
    render_video(images)


if __name__ == "__main__":
    main()
