#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from typing import Callable, Optional

import rclpy
from rclpy.node import Node

from ancile_aeris_operator_copilot.srv import QueryCopilot


def _load_guard() -> Optional[Callable]:
    repo_root = Path(__file__).resolve().parents[3]
    guard_path = repo_root / "payloads" / "generic"
    if str(guard_path) not in sys.path:
        sys.path.insert(0, str(guard_path))
    try:
        from ancile_rule_guard import classify_text  # type: ignore
        return classify_text
    except Exception:
        return None


def _template_answer(query: str, dashboard_state: dict) -> str:
    summary = dashboard_state.get("summary", {})
    latest = dashboard_state.get("latest", {})
    return (
        f"Query: {query}\n"
        f"Current counts - tracks: {summary.get('tracks', 0)}, threats: {summary.get('threats', 0)}, "
        f"commands: {summary.get('commands', 0)}, audits: {summary.get('audits', 0)}.\n"
        f"Latest threat snapshot: {json.dumps(latest.get('threat', {}))}"
    )


class OperatorCopilotNode(Node):
    def __init__(self) -> None:
        super().__init__("ancile_aeris_operator_copilot_node")
        self.declare_parameter("backend", "template")
        self.declare_parameter("dashboard_state_file", "/tmp/ancile_aeris_dashboard_state.json")
        self.guard = _load_guard()
        self.service = self.create_service(QueryCopilot, "ancile_aeris_operator_copilot/query", self._on_query)
        self.get_logger().info("ancile_aeris_operator_copilot_node initialized")

    def _on_query(self, request: QueryCopilot.Request, response: QueryCopilot.Response) -> QueryCopilot.Response:
        backend = str(os.getenv("ANCILE_COPILOT_BACKEND", self.get_parameter("backend").value))
        query = request.query.strip()
        if self.guard is not None:
            verdict = self.guard(query)
            if verdict.label == "block":
                response.blocked = True
                response.backend = backend
                response.reason = "ancile_rule_guard_block"
                response.answer = "Query blocked by Ancile safety rule guard."
                return response

        state_file = str(self.get_parameter("dashboard_state_file").value)
        state = {"summary": {}, "latest": {}}
        if os.path.exists(state_file):
            try:
                with open(state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
            except json.JSONDecodeError:
                pass

        response.blocked = False
        response.backend = backend
        response.reason = "ok"
        if backend == "ollama":
            response.answer = (
                "Ollama backend placeholder: falling back to template summary. "
                + _template_answer(query, state)
            )
        else:
            response.answer = _template_answer(query, state)
        return response


def main() -> None:
    rclpy.init()
    node = OperatorCopilotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
