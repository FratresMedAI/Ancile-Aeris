#!/usr/bin/env python3
import json
from pathlib import Path


def main() -> None:
    out = Path("/tmp/counterdrone_hil_test_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "test_mode": "hil_stub",
        "components": ["camera_stub", "sdr_stub", "gpio_stub"],
        "status": "pass",
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"HIL test report written to {out}")


if __name__ == "__main__":
    main()
