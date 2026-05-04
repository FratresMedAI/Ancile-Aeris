#!/usr/bin/env python3
import json

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from std_msgs.msg import String

from blacksky_digital_twin.msg import DigitalTwinSimulation
from blacksky_digital_twin.srv import SimulateAction


def evaluate_action(action_type: str, target_id: str, friendly_x_positions: list[float]) -> tuple[bool, str, float]:
    if action_type == "shoot":
        if target_id in {str(x) for x in friendly_x_positions}:
            return False, "Friendly unit in danger", 1.0
        return True, "No friendly unit in danger", 0.0
    return True, "Action not simulated", 0.0


class DigitalTwinNode(Node):
    def __init__(self) -> None:
        super().__init__("digital_twin_node")

        self.simulation_result_publisher = self.create_publisher(DigitalTwinSimulation, "simulation_result", 10)
        self.service = self.create_service(SimulateAction, "simulate_action", self.simulate_action_callback)

        self.intended_action_subscriber = self.create_subscription(
            String,
            "intended_action",
            self.intended_action_callback,
            10,
        )
        self.friendly_units_subscriber = self.create_subscription(
            PoseStamped,
            "friendly_units",
            self.friendly_units_callback,
            10,
        )

        self.twin_state_pub = self.create_publisher(String, "/digital_twin_state", 10)
        self.friendly_units: list[PoseStamped] = []
        self.intended_action: dict | None = None

    def intended_action_callback(self, msg: String) -> None:
        parts = msg.data.split(" ")
        if len(parts) < 2:
            self.get_logger().error("Invalid intended action format")
            return
        self.intended_action = {
            "action_type": parts[0],
            "target_id": parts[-1],
        }
        self.get_logger().info(f"Received intended action: {self.intended_action}")

    def friendly_units_callback(self, msg: PoseStamped) -> None:
        self.friendly_units.append(msg)

    def simulate_action_callback(self, request: SimulateAction.Request, response: SimulateAction.Response) -> SimulateAction.Response:
        if not self.intended_action:
            response.success = False
            response.reason = "No intended action received"
            response.impact_score = 1.0
            return response

        if not self.friendly_units:
            response.success = False
            response.reason = "No friendly units available"
            response.impact_score = 1.0
            return response

        friendly_x_positions = [unit.pose.position.x for unit in self.friendly_units]
        success, reason, impact = evaluate_action(request.action_type, request.target_id, friendly_x_positions)

        response.success = success
        response.reason = reason
        response.impact_score = impact

        sim_msg = DigitalTwinSimulation()
        sim_msg.success = success
        sim_msg.reason = reason
        sim_msg.impact_score = impact
        self.simulation_result_publisher.publish(sim_msg)

        twin_state = {
            "digital_twin_state": {
                "scenario_id": "service-sim",
                "mirrored_tracks": len(self.friendly_units),
                "predicted_collisions": 1 if impact > 0.0 else 0,
                "soldier_risk": impact,
                "confidence": 0.9,
                "request": {
                    "action_type": request.action_type,
                    "target_id": request.target_id,
                },
            }
        }
        state_msg = String()
        state_msg.data = json.dumps(twin_state)
        self.twin_state_pub.publish(state_msg)

        return response


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = DigitalTwinNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
