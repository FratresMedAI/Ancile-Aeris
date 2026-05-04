#!/usr/bin/env python3
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class Threat:
    track_id: str
    score: float
    classification: str
    recommended_effector: str


@dataclass
class EffectorCommand:
    command_id: str
    track_id: str
    action: str
    authorized: bool
    reason: str


class C2DecisionNode(Node):
    def __init__(self) -> None:
        super().__init__("c2_decision_node")

        self.declare_parameter("fused_tracks_topic", "/fused_tracks")
        self.declare_parameter("predicted_topic", "/predicted_trajectories")
        self.declare_parameter("threats_topic", "/threats")
        self.declare_parameter("effector_cmd_topic", "/effector_commands")
        self.declare_parameter("audit_topic", "/audit/events")
        self.declare_parameter("xai_topic", "/xai_explanation")
        self.declare_parameter("operator_auth_topic", "/operator/authorizations")
        self.declare_parameter("rl_recommendation_topic", "/sim/rl_recommendations")
        self.declare_parameter("cyber_topic", "/cyber/identity_assessments")
        self.declare_parameter("digital_twin_topic", "/digital_twin_state")
        self.declare_parameter("swarm_intent_topic", "/swarm/intent_assessment")
        self.declare_parameter("score_threshold", 0.65)
        self.declare_parameter("pid_gate", 0.999)
        self.declare_parameter("hostile_identity_confidence", 0.7)
        self.declare_parameter("allow_jamming", True)
        self.declare_parameter("allow_spoofing", True)
        self.declare_parameter("allow_kinetic", False)
        self.declare_parameter("sim_mode", True)
        self.declare_parameter("use_rl_policy", True)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(String, self.get_parameter("fused_tracks_topic").value, self._on_fused_tracks, qos)
        self.create_subscription(String, self.get_parameter("predicted_topic").value, self._on_predicted, qos)
        self.create_subscription(String, self.get_parameter("rl_recommendation_topic").value, self._on_rl_recommendations, qos)
        self.create_subscription(String, self.get_parameter("cyber_topic").value, self._on_cyber, qos)
        self.create_subscription(String, self.get_parameter("digital_twin_topic").value, self._on_digital_twin, qos)
        self.create_subscription(String, self.get_parameter("swarm_intent_topic").value, self._on_swarm_intent, qos)
        self.create_subscription(String, self.get_parameter("operator_auth_topic").value, self._on_operator_auth, qos)

        self.threat_pub = self.create_publisher(String, self.get_parameter("threats_topic").value, qos)
        self.cmd_pub = self.create_publisher(String, self.get_parameter("effector_cmd_topic").value, qos)
        self.audit_pub = self.create_publisher(String, self.get_parameter("audit_topic").value, qos)
        self.xai_pub = self.create_publisher(String, self.get_parameter("xai_topic").value, qos)

        self.latest_predicted = None
        self.latest_rl: dict[str, dict] = {}
        self.latest_cyber: dict[str, dict] = {}
        self.latest_operator_auth: dict[str, dict] = {}
        self.latest_digital_twin: dict = {}
        self.latest_swarm_intent: dict = {}
        self.command_seq = 0
        self.get_logger().info("c2_decision_node initialized")

    def _on_predicted(self, msg: String) -> None:
        try:
            self.latest_predicted = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid predicted trajectory payload")

    def _threat_score(self, track: dict) -> float:
        confidence = float(track.get("confidence", 0.0))
        speed = abs(float(track.get("vx", 0.0))) + abs(float(track.get("vy", 0.0)))
        speed_norm = min(1.0, speed / 20.0)

        predicted_risk = 0.4
        if self.latest_predicted and self.latest_predicted.get("predictions"):
            predicted_risk = 0.6

        return 0.6 * confidence + 0.25 * speed_norm + 0.15 * predicted_risk

    def _on_rl_recommendations(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rl recommendation payload")
            return
        self.latest_rl = {r.get("track_id", ""): r for r in payload.get("recommendations", [])}

    def _on_cyber(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid cyber payload")
            return
        self.latest_cyber = {a.get("emitter_id", ""): a for a in payload.get("assessments", [])}

    def _on_operator_auth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid operator authorization payload")
            return

        auths = payload.get("authorizations", [])
        self.latest_operator_auth = {str(a.get("track_id", "")): a for a in auths}

    def _on_digital_twin(self, msg: String) -> None:
        try:
            self.latest_digital_twin = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid digital twin payload")

    def _on_swarm_intent(self, msg: String) -> None:
        try:
            self.latest_swarm_intent = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid swarm intent payload")

    def _select_effector(self, score: float) -> str:
        allow_jam = bool(self.get_parameter("allow_jamming").value)
        allow_spoof = bool(self.get_parameter("allow_spoofing").value)
        allow_kin = bool(self.get_parameter("allow_kinetic").value)

        if score > 0.85 and allow_spoof:
            return "spoof"
        if score > 0.70 and allow_jam:
            return "jam"
        if score > 0.90 and allow_kin:
            return "kinetic_stub"
        return "monitor"

    def _select_effector_with_policy(self, track_id: str, score: float) -> str:
        base = self._select_effector(score)
        if not bool(self.get_parameter("use_rl_policy").value):
            return base

        rec = self.latest_rl.get(track_id)
        if rec is None:
            return base

        if float(rec.get("confidence", 0.0)) < 0.65:
            return base

        action = str(rec.get("preferred_action", base))
        allowed = {"monitor", "jam", "spoof", "kinetic_stub"}
        return action if action in allowed else base

    def _authorize(self, action: str) -> tuple[bool, str]:
        sim_mode = bool(self.get_parameter("sim_mode").value)
        if action in {"jam", "spoof", "kinetic_stub"} and not sim_mode:
            return False, "blocked_in_live_mode_without_human_approval"
        if action == "kinetic_stub" and not bool(self.get_parameter("allow_kinetic").value):
            return False, "kinetic_disabled_by_roe"
        return True, "authorized"

    def _publish_audit(self, track_id: str, score: float, action: str, authorized: bool, reason: str) -> None:
        audit_msg = String()
        audit_msg.data = json.dumps({
            "event": "c2_decision",
            "track_id": track_id,
            "score": score,
            "action": action,
            "authorized": authorized,
            "reason": reason,
        })
        self.audit_pub.publish(audit_msg)

    def _publish_xai(self, track_id: str, score: float, action: str, uncertainty: dict | None = None) -> None:
        twin = self.latest_digital_twin.get("digital_twin_state", {}) if self.latest_digital_twin else {}
        uncertainty = uncertainty or {}
        uncertainty_total = float(uncertainty.get("total", 1.0))
        certainty = max(0.0, 1.0 - uncertainty_total)
        nl_summary = (
            f"Threat score {score:.2f} for {track_id}. Recommended action: {action}. "
            f"Estimated certainty {certainty:.2f} from multimodal agreement and trajectory context."
        )
        rationale = {
            "track_id": track_id,
            "score": score,
            "action": action,
            "top_features": ["confidence", "speed", "predicted_risk", "twin_collision_risk"],
            "digital_twin_context": twin,
            "swarm_intent": self.latest_swarm_intent,
            "uncertainty": uncertainty,
            "nl_summary": nl_summary,
            "explanation": "Action selected by ROE-constrained score with policy assist and twin context.",
        }
        msg = String()
        msg.data = json.dumps(rationale)
        self.xai_pub.publish(msg)

    def _extract_twin_risk(self) -> float:
        if not self.latest_digital_twin:
            return 1.0

        state = self.latest_digital_twin.get("digital_twin_state", {})
        if not isinstance(state, dict):
            return 1.0

        risk = state.get("soldier_risk", None)
        if risk is not None:
            try:
                return max(0.0, float(risk))
            except (TypeError, ValueError):
                return 1.0

        collisions = int(state.get("predicted_collisions", 0))
        return 0.0 if collisions <= 0 else 1.0

    def _is_friendly(self, track_id: str) -> bool:
        assessment = self.latest_cyber.get(track_id)
        if not assessment:
            return False
        return str(assessment.get("disposition", "")) == "friendly"

    def _is_hostile_confirmed(self, track_id: str) -> bool:
        assessment = self.latest_cyber.get(track_id)
        if not assessment:
            return False
        disposition = str(assessment.get("disposition", ""))
        conf = float(assessment.get("confidence", 0.0))
        min_conf = float(self.get_parameter("hostile_identity_confidence").value)
        return disposition == "unknown_or_hostile" and conf >= min_conf

    def _operator_acknowledged(self, track_id: str, action: str) -> bool:
        if action == "monitor":
            return True

        auth = self.latest_operator_auth.get(track_id)
        if not auth:
            return False
        return bool(auth.get("authorized", False)) and str(auth.get("action", "")) == action

    def _on_fused_tracks(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid fused track payload")
            return

        tracks = payload.get("tracks", [])
        if not tracks:
            return

        track = tracks[0]
        track_id = str(track.get("track_id", "unknown"))
        score = self._threat_score(track)
        threshold = float(self.get_parameter("score_threshold").value)

        if score < threshold:
            return

        action = self._select_effector_with_policy(track_id, score)

        pid = payload.get("pid", {})
        pid_passed = bool(pid.get("passed", False))
        pid_conf = float(pid.get("confidence", 0.0))
        pid_gate = float(self.get_parameter("pid_gate").value)

        uncertainty = payload.get("uncertainty", {})

        # BORAP 04 safety posture across dense urban, mass gatherings,
        # critical infrastructure, mobile platforms, and remote terrain:
        # if any gate fails, commands are forced to monitor-only.
        if not pid_passed or pid_conf < pid_gate:
            action = "monitor"
            authorized = False
            reason = "blocked_pid_gate"
        elif self._is_friendly(track_id):
            action = "monitor"
            authorized = False
            reason = "blocked_friendly_iff"
        elif not self._is_hostile_confirmed(track_id):
            action = "monitor"
            authorized = False
            reason = "blocked_unconfirmed_hostile_identity"
        elif action != "monitor" and self._extract_twin_risk() > 0.0:
            action = "monitor"
            authorized = False
            reason = "blocked_digital_twin_risk"
        elif not self._operator_acknowledged(track_id, action):
            authorized = False
            reason = "blocked_no_operator_authorization"
        else:
            authorized, reason = self._authorize(action)

        threat = Threat(
            track_id=track_id,
            score=score,
            classification="hostile_suspect",
            recommended_effector=action,
        )

        threat_msg = String()
        threat_msg.data = json.dumps({"threats": [asdict(threat)]})
        self.threat_pub.publish(threat_msg)

        self.command_seq += 1
        cmd = EffectorCommand(
            command_id=f"cmd-{self.command_seq:05d}",
            track_id=track_id,
            action=action,
            authorized=authorized,
            reason=reason,
        )
        cmd_msg = String()
        cmd_msg.data = json.dumps({"commands": [asdict(cmd)]})
        self.cmd_pub.publish(cmd_msg)
        self._publish_audit(track_id, score, action, authorized, reason)
        self._publish_xai(track_id, score, action, uncertainty=uncertainty)


def main() -> None:
    rclpy.init()
    node = C2DecisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
