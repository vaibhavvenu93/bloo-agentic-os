from typing import Dict

from apps.api.bloo.agents.critic import CriticAgent
from apps.api.bloo.agents.operator import OperatorAgent
from apps.api.bloo.agents.researcher import ResearchAgent
from apps.api.bloo.agents.scout import ScoutAgent
from apps.api.bloo.agents.seller import SellerAgent
from apps.api.bloo.brain.store import CompanyBrain


class OrchestratorAgent:
    """
    BLOO Orchestrator Agent

    Coordinates specialist agents around one shared operating view.

    Current flow:

    Commercial Intelligence
        -> Scout
        -> Researcher
        -> Seller
        -> Operator
        -> Critic
        -> Orchestrator
        -> CEO only when necessary

    The Orchestrator also enforces commercial gates.
    Seller may prepare a pursuit while outbound remains blocked.
    """

    name = "orchestrator"

    def __init__(self, brain: CompanyBrain):
        self.brain = brain

        self.scout = ScoutAgent()
        self.researcher = ResearchAgent()
        self.seller = SellerAgent()

        self.operator = OperatorAgent(brain)
        self.critic = CriticAgent(brain)

    def run(self) -> Dict:
        """
        Execute the BLOO commercial + operating loop.
        """

        # -------------------------------------------------
        # STEP 1 — FIND COMMERCIAL OPPORTUNITIES
        # -------------------------------------------------

        scout_output = self.scout.recommend(
            limit=3
        )

        # -------------------------------------------------
        # STEP 2 — IDENTIFY RESEARCH GAPS
        # -------------------------------------------------

        research_output = self.researcher.build_from_scout(
            scout_output,
        )

        # -------------------------------------------------
        # STEP 3 — PREPARE SALES PURSUITS
        # -------------------------------------------------

        seller_output = self.seller.build_from_scout(
            scout_output,
            limit=3,
        )

        # -------------------------------------------------
        # STEP 4 — ENFORCE OUTBOUND GATE
        # -------------------------------------------------

        blocking_tasks = research_output.get(
            "blocking_tasks",
            [],
        )

        outbound_allowed = bool(
            research_output.get(
                "outbound_safe",
                False,
            )
        )

        commercial_status = (
            "outbound_ready"
            if outbound_allowed
            else "research_blocked"
        )

        # Attach gate status to each prepared pursuit.
        gated_pursuits = []

        for pursuit in seller_output.get(
            "pursuits",
            [],
        ):
            gated_pursuit = {
                **pursuit,

                "commercial_gate": {
                    "status": commercial_status,

                    "outbound_allowed": (
                        outbound_allowed
                    ),

                    "blocking_research_tasks": len(
                        blocking_tasks
                    ),

                    "rule": (
                        "Outbound requires buyer and CRM "
                        "validation to be resolved."
                    ),
                },
            }

            gated_pursuits.append(
                gated_pursuit
            )

        seller_output[
            "pursuits"
        ] = gated_pursuits

        seller_output[
            "outbound_allowed"
        ] = outbound_allowed

        # -------------------------------------------------
        # STEP 5 — OPERATING INTELLIGENCE
        # -------------------------------------------------

        operator_output = self.operator.recommend()

        # -------------------------------------------------
        # STEP 6 — CRITIC REVIEW
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
        # STEP 7 — CEO ATTENTION FILTER
        # -------------------------------------------------

        ceo_attention = []
        handled_without_ceo = []

        for review in approved_actions:

            original_action = review.get(
                "original_action",
                {},
            )

            if original_action.get(
                "requires_ceo",
                False,
            ):
                ceo_attention.append(
                    review
                )

            else:
                handled_without_ceo.append(
                    review
                )

        # -------------------------------------------------
        # FINAL OPERATING VIEW
        # -------------------------------------------------

        return {
            "agent": self.name,

            "objective": (
                "Coordinate commercial and operating intelligence "
                "into evidence-backed execution while preventing "
                "premature outbound and protecting CEO attention."
            ),

            "workflow": [
                {
                    "step": 1,
                    "agent": "scout",
                    "status": "completed",
                    "output": (
                        "Ranked commercial opportunities."
                    ),
                },

                {
                    "step": 2,
                    "agent": "researcher",
                    "status": "completed",
                    "output": (
                        "Converted unresolved account questions "
                        "into structured research tasks."
                    ),
                },

                {
                    "step": 3,
                    "agent": "seller",
                    "status": "completed",
                    "output": (
                        "Prepared enterprise pursuits for "
                        "high-priority accounts."
                    ),
                },

                {
                    "step": 4,
                    "agent": "commercial_gate",
                    "status": commercial_status,
                    "output": (
                        "Outbound blocked until required research "
                        "is resolved."
                        if not outbound_allowed
                        else
                        "Evidence requirements satisfied. "
                        "Outbound permitted."
                    ),
                },

                {
                    "step": 5,
                    "agent": "operator",
                    "status": "completed",
                    "output": (
                        "Identified operating actions from "
                        "Company Brain."
                    ),
                },

                {
                    "step": 6,
                    "agent": "critic",
                    "status": "completed",
                    "output": (
                        "Reviewed operating recommendations "
                        "against available evidence."
                    ),
                },

                {
                    "step": 7,
                    "agent": "orchestrator",
                    "status": "completed",
                    "output": (
                        "Separated autonomous work from "
                        "CEO-attention items."
                    ),
                },
            ],

            "brain_state": self.brain.summary(),

            "commercial": {
                "scout": scout_output,
                "researcher": research_output,
                "seller": seller_output,

                "gate": {
                    "status": commercial_status,
                    "outbound_allowed": outbound_allowed,
                    "blocking_tasks": len(
                        blocking_tasks
                    ),
                },
            },

            "operations": {
                "operator": operator_output,
                "critic": critic_output,
            },

            "final": {
                "commercial_opportunities": (
                    scout_output.get(
                        "recommended_targets",
                        [],
                    )
                ),

                "commercial_pursuits": (
                    gated_pursuits
                ),

                "research_queue": (
                    research_output.get(
                        "research_queue",
                        [],
                    )
                ),

                "approved_team_actions": (
                    handled_without_ceo
                ),

                "ceo_attention": (
                    ceo_attention
                ),

                "challenged_actions": (
                    challenged_actions
                ),
            },

            "summary": {
                "commercial_opportunities": len(
                    scout_output.get(
                        "recommended_targets",
                        [],
                    )
                ),

                "commercial_pursuits": len(
                    gated_pursuits
                ),

                "research_tasks": research_output.get(
                    "summary",
                    {},
                ).get(
                    "tasks",
                    0,
                ),

                "blocking_research_tasks": len(
                    blocking_tasks
                ),

                "outbound_allowed": (
                    outbound_allowed
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

                "requires_ceo": len(
                    ceo_attention
                ),

                "handled_without_ceo": len(
                    handled_without_ceo
                ),
            },
        }
