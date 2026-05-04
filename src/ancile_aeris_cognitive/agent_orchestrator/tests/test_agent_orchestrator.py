from dataclasses import dataclass


@dataclass
class AgentScore:
    detection: float
    intent: float
    mitigation: float
    safety: float


def aggregate_agent_score(score: AgentScore) -> float:
    return (score.detection + score.intent + score.mitigation + score.safety) / 4.0


def test_aggregate_agent_score() -> None:
    value = aggregate_agent_score(AgentScore(0.8, 0.7, 0.6, 1.0))
    assert 0.0 <= value <= 1.0
    assert value > 0.75
