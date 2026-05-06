from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class DashboardBridge:
    def __init__(self, out_path: str) -> None:
        self.out_path = Path(out_path)

    def publish(self, payload: Dict[str, Any]) -> None:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        with self.out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
