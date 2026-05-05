#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import sqlite3
from datetime import datetime, timezone

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


def make_hmac(secret: bytes, payload: str) -> str:
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()


class AncileBridgeAdapterNode(Node):
    def __init__(self) -> None:
        super().__init__("ancile_bridge_adapter_node")

        self.declare_parameter("audit_topic", "/audit/events")
        self.declare_parameter("threat_topic", "/threats")
        self.declare_parameter("command_topic", "/effector_commands")
        self.declare_parameter("health_topic", "/ancile_guard/health")
        self.declare_parameter("db_path", "/tmp/ancile_bridge_adapter.db")
        self.declare_parameter("hmac_secret_env", "ANCILE_HMAC_SECRET")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)

        self.create_subscription(String, self.get_parameter("audit_topic").value, self._on_audit, qos)
        self.create_subscription(String, self.get_parameter("threat_topic").value, self._on_threat, qos)
        self.create_subscription(String, self.get_parameter("command_topic").value, self._on_command, qos)
        self.health_pub = self.create_publisher(String, self.get_parameter("health_topic").value, qos)

        env_key = str(self.get_parameter("hmac_secret_env").value)
        secret = os.environ.get(env_key, "change_me_in_production")
        self.secret = secret.encode("utf-8")

        self.db_path = str(self.get_parameter("db_path").value)
        self._init_db()
        self.timer = self.create_timer(2.0, self._publish_health)

    def _conn(self) -> sqlite3.Connection:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        conn = self._conn()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ancile_bridge_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                source_topic TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                payload_hash TEXT NOT NULL,
                hmac_sig TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def _store(self, topic: str, payload: str) -> None:
        payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        signature = make_hmac(self.secret, payload)
        ts = datetime.now(timezone.utc).isoformat()

        conn = self._conn()
        conn.execute(
            "INSERT INTO ancile_bridge_log (ts, source_topic, payload_json, payload_hash, hmac_sig) VALUES (?, ?, ?, ?, ?)",
            (ts, topic, payload, payload_hash, signature),
        )
        conn.commit()
        conn.close()

    def _on_audit(self, msg: String) -> None:
        self._store(str(self.get_parameter("audit_topic").value), msg.data)

    def _on_threat(self, msg: String) -> None:
        self._store(str(self.get_parameter("threat_topic").value), msg.data)

    def _on_command(self, msg: String) -> None:
        self._store(str(self.get_parameter("command_topic").value), msg.data)

    def _publish_health(self) -> None:
        conn = self._conn()
        row = conn.execute("SELECT COUNT(*) FROM ancile_bridge_log").fetchone()
        conn.close()
        count = int(row[0]) if row else 0

        msg = String()
        msg.data = json.dumps({
            "status": "ok",
            "records": count,
            "db_path": self.db_path,
        })
        self.health_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = AncileBridgeAdapterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
