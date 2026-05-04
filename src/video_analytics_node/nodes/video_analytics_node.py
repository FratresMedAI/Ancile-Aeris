#!/usr/bin/env python3
import json
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def _behavior_from_history(window: deque[dict]) -> str:
    if len(window) < 2:
        return "observe"
    first = window[0]
    last = window[-1]
    dx = float(last.get("x", 0.0)) - float(first.get("x", 0.0))
    dy = float(last.get("y", 0.0)) - float(first.get("y", 0.0))
    distance = (dx * dx + dy * dy) ** 0.5
    if distance < 3.0:
        return "loiter"
    if abs(dx) + abs(dy) > 15.0:
        return "rapid_descent"
    return "approach"


class VideoAnalyticsNode(Node):
    def __init__(self) -> None:
        super().__init__("video_analytics_node")
        self.declare_parameter("visual_tracks_topic", "/sensor/visual/tracks")
        self.declare_parameter("analytics_topic", "/sensor/visual/analytics")
        self.declare_parameter("behavioral_alerts_topic", "/behavioral_alerts")
        self.declare_parameter("min_confidence", 0.55)

        visual_topic = str(self.get_parameter("visual_tracks_topic").value)
        self.analytics_pub = self.create_publisher(
            String, str(self.get_parameter("analytics_topic").value), 20
        )
        self.behavior_pub = self.create_publisher(
            String, str(self.get_parameter("behavioral_alerts_topic").value), 20
        )
        self.create_subscription(String, visual_topic, self._on_visual_tracks, 20)
        self.track_history: dict[str, deque[dict]] = {}
        self.get_logger().info("video_analytics_node initialized")

    def _on_visual_tracks(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid visual tracks payload")
            return

        tracks = payload.get("tracks", [])
        if not tracks:
            return

        min_conf = float(self.get_parameter("min_confidence").value)
        enriched = []
        behavior_alerts = []
        for trk in tracks:
            confidence = float(trk.get("confidence", 0.0))
            if confidence < min_conf:
                continue
            track_id = str(trk.get("track_id", "unknown"))
            hist = self.track_history.setdefault(track_id, deque(maxlen=20))
            hist.append(
                {
                    "x": float(trk.get("x", 0.0)),
                    "y": float(trk.get("y", 0.0)),
                    "confidence": confidence,
                }
            )
            behavior = _behavior_from_history(hist)
            analytics = {
                "track_id": track_id,
                "drone_class": "uas_candidate",
                "visual_confirmation": True,
                "behavior_tag": behavior,
                "reid_id": f"reid-{track_id}",
                "thumbnail_ref": f"/tmp/sim_frames/{track_id}.jpg",
                "bbox": trk.get("bbox", {"x": trk.get("x", 0.0), "y": trk.get("y", 0.0)}),
                "confidence": confidence,
            }
            enriched.append(analytics)
            if behavior in {"approach", "rapid_descent"}:
                behavior_alerts.append(
                    {"track_id": track_id, "behavior_tag": behavior, "confidence": confidence}
                )

        if not enriched:
            return

        analytics_msg = String()
        analytics_msg.data = json.dumps({"video_analytics": enriched})
        self.analytics_pub.publish(analytics_msg)

        behavior_msg = String()
        behavior_msg.data = json.dumps({"alerts": behavior_alerts})
        self.behavior_pub.publish(behavior_msg)


def main() -> None:
    rclpy.init()
    node = VideoAnalyticsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
