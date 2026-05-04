#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def generate_manifest(output_dir: Path, sample_count: int) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "synthetic_manifest.json"
    entries = []
    for i in range(sample_count):
        entries.append(
            {
                "id": f"syn-{i:06d}",
                "image": f"images/syn_{i:06d}.png",
                "label": f"labels/syn_{i:06d}.txt",
                "weather": ["clear", "rain", "fog", "dust"][i % 4],
                "swarm_size": 1 + (i % 8),
            }
        )

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"samples": entries}, f)

    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="/tmp/counterdrone_synth")
    parser.add_argument("--sample-count", type=int, default=10000)
    args = parser.parse_args()

    manifest_path = generate_manifest(Path(args.output_dir), args.sample_count)
    print(f"Generated synthetic manifest: {manifest_path}")


if __name__ == "__main__":
    main()
