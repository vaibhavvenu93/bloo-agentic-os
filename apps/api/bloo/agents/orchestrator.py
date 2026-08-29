from typing import Dict

from apps.api.bloo.agents.critic import CriticAgent
from apps.api.bloo.agents.operator import OperatorAgent
from apps.api.bloo.brain.store import CompanyBrain


class OrchestratorAgent:
    """
    BLOO Orchestrator Agent

    Coordinates specialist agents against the shared Company Brain.
    It decides what to inspect, asks agents for recommendations,
    routes those recommendations through critique, and returns a
    final operating view.
    """

    name = "orchestrator"

    def __init__(self, brain: CompanyBrain):
        self.brain = brain
        self.operator = OperatorAgent(brain)
        self.critic = CriticAgent(brain)

    def run(self) -> Dict:
        """
        Run the first BLOO multi-agent operating workflow.

        Flow:
        Company Brain
            -> Operator
            -> Critic
            -> Final recommendation
        """

        operator_output = self.operator.recommend()

        critic_output = self.critic.review_recommendations(
            operator_output
        )

        approved_actions = critic_output.get(
            "approved_actions",
            []
        )

        challenged_actions = critic_output.get(
            "challenged_actions",
            []
        )

        ceo_items = []

        for review in approved_actions:
            original_action = review.get(
                "original_action",
                {}
            )

            if original_action.get("requires_ceo"):
                ceo_items.append(review)

        team_items = []

        for review in approved_actions:
            original_action = review.get(
                "original_action",
                {}
            )

            if not original_action.get("requires_ceo"):
                team_items.append(review)

        return {
            "agent": self.name,
            "objective": (
                "Coordinate company intelligence into evidence-backed "
                "actions while protecting CEO attention."
            ),
            "workflow": [
                {
                    "step": 1,
                    "agent": "operator",
                    "status": "completed",
                    "output": (
                        "Identified operational actions from "
                        "Company Brain."
                    ),
                },
                {
                    "step": 2,
                    "agent": "critic",
                    "status": "completed",
                    "output": (
                        "Reviewed recommendations against "
                        "available evidence."
                    ),
                },
                {
                    "step": 3,
                    "agent": "orchestrator",
                    "status": "completed",
                    "output": (
                        "Separated approved work, challenged work, "
                        "and CEO attention."
                    ),
                },
            ],
            "brain_state": self.brain.summary(),
            "operator": operator_output,
            "critic": critic_output,
            "final": {
                "approved_team_actions": team_items,
                "ceo_attention": ceo_items,
                "challenged_actions": challenged_actions,
            },
            "summary": {
                "operator_actions": operator_output[
                    "summary"
                ]["total_actions"],
                "critic_reviewed": critic_output[
                    "summary"
                ]["reviewed"],
                "approved": critic_output[
                    "summary"
                ]["approved"],
                "challenged": critic_output[
                    "summary"
                ]["challenged"],
                "requires_ceo": len(ceo_items),
                "handled_without_ceo": len(team_items),
            },
        }
