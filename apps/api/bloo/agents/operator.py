from typing import Dict, List

from apps.api.bloo.brain.store import CompanyBrain


class OperatorAgent:
    """
    BLOO Operator Agent

    Looks across the shared Company Brain and identifies
    operational work that should be closed, escalated, or delegated.
    """

    name = "operator"

    def __init__(self, brain: CompanyBrain):
        self.brain = brain

    def _commitment_actions(self) -> List[Dict]:
        actions = []

        for commitment in self.brain.open_commitments():
            actions.append(
                {
                    "type": "commitment_follow_up",
                    "priority": "high",
                    "object_id": commitment.id,
                    "owner": commitment.owner,
                    "reason": commitment.description,
                    "recommended_action": (
                        f"Close or update commitment owned by "
                        f"{commitment.owner}."
                    ),
                    "requires_ceo": False,
                }
            )

        return actions

    def _decision_actions(self) -> List[Dict]:
        actions = []

        for decision in self.brain.open_decisions():
            actions.append(
                {
                    "type": "decision_required",
                    "priority": "high",
                    "object_id": decision.id,
                    "owner": decision.owner,
                    "reason": decision.question,
                    "recommended_action": (
                        decision.recommendation
                        or "Review evidence and make a decision."
                    ),
                    "requires_ceo": True,
                }
            )

        return actions

    def _insight_actions(self) -> List[Dict]:
        actions = []

        for insight in self.brain.insights.values():
            actions.append(
                {
                    "type": "insight_review",
                    "priority": "medium",
                    "object_id": insight.id,
                    "owner": None,
                    "reason": insight.title,
                    "recommended_action": (
                        "Determine whether this learning should become "
                        "a repeatable playbook, experiment, or workflow."
                    ),
                    "requires_ceo": False,
                }
            )

        return actions

    def recommend(self) -> Dict:
        """
        Produce a structured operating recommendation from the Brain.
        """

        actions = []

        actions.extend(self._commitment_actions())
        actions.extend(self._decision_actions())
        actions.extend(self._insight_actions())

        ceo_items = [
            action
            for action in actions
            if action["requires_ceo"]
        ]

        team_items = [
            action
            for action in actions
            if not action["requires_ceo"]
        ]

        return {
            "agent": self.name,
            "objective": (
                "Close loops, surface blockers, and reduce unnecessary "
                "CEO coordination."
            ),
            "brain_state": self.brain.summary(),
            "recommended_actions": actions,
            "ceo_attention": ceo_items,
            "team_actions": team_items,
            "summary": {
                "total_actions": len(actions),
                "requires_ceo": len(ceo_items),
                "handled_without_ceo": len(team_items),
            },
        }
