from typing import Dict

from apps.api.bloo.agents.critic import CriticAgent
from apps.api.bloo.agents.operator import OperatorAgent
from apps.api.bloo.agents.scout import ScoutAgent
from apps.api.bloo.agents.seller import SellerAgent
from apps.api.bloo.brain.store import CompanyBrain


class OrchestratorAgent:
    """
    BLOO Orchestrator Agent

    Coordinates specialist agents around one shared Company Brain.

    Current flow:

    Scout
      -> finds commercial opportunities

    Seller
      -> turns the strongest opportunities into pursuits

    Operator
      -> identifies operational actions

    Critic
      -> challenges recommendations using evidence

    Orchestrator
      -> separates autonomous work from CEO attention
    """

    name = "orchestrator"

    def __init__(self, brain: CompanyBrain):
        self.brain = brain

        self.scout = ScoutAgent()
        self.seller = SellerAgent()
        self.operator = OperatorAgent(brain)
        self.critic = CriticAgent(brain)

    def run(self) -> Dict:

        # -------------------------------------------------
        # STEP 1 — FIND OPPORTUNITIES
        # -------------------------------------------------

        scout_output = self.scout.recommend(limit=3)

        # -------------------------------------------------
        # STEP 2 — BUILD COMMERCIAL PURSUITS
        # -------------------------------------------------

        seller_output = self.seller.build_from_scout(
            scout_output,
            limit=3,
        )

        # -------------------------------------------------
        # STEP 3 — OPERATING INTELLIGENCE
        # -------------------------------------------------

        operator_output = self.operator.recommend()

        # -------------------------------------------------
        # STEP 4 — CRITIC REVIEW
        # -------------------------------------------------

        critic_output = self.critic.review_recommendations(
            operator_output
        )

        approved_actions = critic_output.get(
            "approved_actions",
            [],
        )

        challenged_actions = critic_output.get(
            "challenged_actions",
            [],
        )

        # -------------------------------------------------
        # STEP 5 — CEO ATTENTION FILTER
        # -------------------------------------------------

        ceo_attention = []
        handled_without_ceo = []

        for review in approved_actions:
            original_action = review.get(
                "original_action",
                {},
            )

            if original_action.get("requires_ceo", False):
                ceo_attention.append(review)
            else:
                handled_without_ceo.append(review)

        # -------------------------------------------------
        # FINAL COMPANY VIEW
        # -------------------------------------------------

        return {
            "agent": self.name,
            "objective": (
                "Coordinate commercial and operational intelligence "
                "into evidence-backed actions while protecting CEO attention."
            ),

            "workflow": [
                {
                    "step": 1,
                    "agent": "scout",
                    "status": "completed",
                    "output": (
                        "Identified and ranked commercial opportunities."
                    ),
                },
                {
                    "step": 2,
                    "agent": "seller",
                    "status": "completed",
                    "output": (
                        "Converted top opportunities into enterprise pursuits."
                    ),
                },
                {
                    "step": 3,
                    "agent": "operator",
                    "status": "completed",
                    "output": (
                        "Identified operational actions from Company Brain."
                    ),
                },
                {
                    "step": 4,
                    "agent": "critic",
                    "status": "completed",
                    "output": (
                        "Reviewed proposed actions against evidence."
                    ),
                },
                {
                    "step": 5,
                    "agent": "orchestrator",
                    "status": "completed",
                    "output": (
                        "Separated company work from CEO-attention items."
                    ),
                },
            ],

            "brain_state": self.brain.summary(),

            "commercial": {
                "scout": scout_output,
                "seller": seller_output,
            },

            "operations": {
                "operator": operator_output,
                "critic": critic_output,
            },

            "final": {
                "commercial_opportunities": scout_output.get(
                    "recommended_targets",
                    [],
                ),
                "commercial_pursuits": seller_output.get(
                    "pursuits",
                    [],
                ),
                "approved_team_actions": handled_without_ceo,
                "ceo_attention": ceo_attention,
                "challenged_actions": challenged_actions,
            },

            "summary": {
                "commercial_opportunities": len(
                    scout_output.get(
                        "recommended_targets",
                        [],
                    )
                ),
                "commercial_pursuits": len(
                    seller_output.get(
                        "pursuits",
                        [],
                    )
                ),
                "operator_actions": operator_output.get(
                    "summary",
                    {},
                ).get(
                    "total_actions",
                    0,
                ),
                "critic_reviewed": critic_output.get(
                    "summary",
                    {},
                ).get(
                    "reviewed",
                    0,
                ),
                "approved": critic_output.get(
                    "summary",
                    {},
                ).get(
                    "approved",
                    0,
                ),
                "challenged": critic_output.get(
                    "summary",
                    {},
                ).get(
                    "challenged",
                    0,
                ),
                "requires_ceo": len(
                    ceo_attention
                ),
                "handled_without_ceo": len(
                    handled_without_ceo
                ),
            },
        }
