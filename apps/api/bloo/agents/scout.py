from typing import Dict, List

from apps.api.bloo.intelligence.commercial import (
    get_commercial_accounts,
)


class ScoutAgent:
    """
    BLOO Scout Agent

    Reads from the shared Commercial Intelligence layer,
    ranks opportunities, and recommends which accounts
    Blueberry should investigate now.

    Scout does not own account data.
    It interprets the intelligence layer.
    """

    name = "scout"

    def __init__(self):
        self.accounts = get_commercial_accounts()

    def _calculate_readiness(self, account: Dict) -> Dict:
        """
        Respect the readiness assessment produced by the
        Commercial Intelligence layer.

        Scout interprets intelligence.
        It does not independently redefine evidence quality.
        """

        evidence = account.get(
            "evidence_summary",
            {},
        )

        intelligence_readiness = evidence.get(
            "readiness",
            "research_required",
        )

        if intelligence_readiness == "outbound_ready":
            scout_status = "outbound_ready"

        elif (
            intelligence_readiness
            == "commercially_relevant_research"
        ):
            scout_status = "research_before_outbound"

        else:
            scout_status = "validation_required"

        return {
            "status": scout_status,
            "intelligence_readiness": intelligence_readiness,
            "verified_signals": evidence.get(
                "verified",
                0,
            ),
            "signals_requiring_validation": evidence.get(
                "requires_validation",
                0,
            ),
        }

    def _build_recommendation(
        self,
        account: Dict,
    ) -> Dict:

        hypothesis = account.get(
            "commercial_hypothesis",
            {},
        )

        readiness = self._calculate_readiness(
            account
        )

        return {
            "id": account.get("id"),
            "company": account.get("company"),
            "industry": account.get("industry"),
            "opportunity_score": account.get(
                "opportunity_score"
            ),

            "why_this_account": account.get(
                "why_this_account"
            ),

            "why_now": hypothesis.get(
                "why_now"
            ),

            "problem_hypothesis": hypothesis.get(
                "problem"
            ),

            "blueberry_wedge": hypothesis.get(
                "blueberry_wedge"
            ),

            "pilot_hypothesis": hypothesis.get(
                "pilot"
            ),

            "evidence": account.get(
                "verified_signals",
                [],
            ),

            "needs_validation": account.get(
                "needs_validation",
                [],
            ),

            "evidence_summary": account.get(
                "evidence_summary",
                {},
            ),

            "readiness": readiness,

            "recommended_next_step": (
                "Prepare the account for outbound."
                if readiness["status"]
                == "outbound_ready"
                else (
                    "Complete targeted research before outbound."
                    if readiness["status"]
                    == "research_before_outbound"
                    else
                    "Validate core commercial evidence before progressing."
                )
            ),
        }

    def rank_targets(self) -> List[Dict]:
        """
        Return commercial opportunities in ranked order.
        """

        recommendations = [
            self._build_recommendation(account)
            for account in self.accounts
        ]

        return sorted(
            recommendations,
            key=lambda item: item.get(
                "opportunity_score",
                0,
            ),
            reverse=True,
        )

    def recommend(
        self,
        limit: int = 3,
    ) -> Dict:

        ranked = self.rank_targets()

        selected = ranked[:limit]

        outbound_ready = [
            target
            for target in selected
            if target["readiness"]["status"]
            == "outbound_ready"
        ]

        research_required = [
            target
            for target in selected
            if target["readiness"]["status"]
            != "outbound_ready"
        ]

        return {
            "agent": self.name,

            "objective": (
                "Identify the companies Blueberry should spend "
                "commercial attention on while preventing weak "
                "or unverified account theses from reaching outbound."
            ),

            "targets_considered": len(
                ranked
            ),

            "recommended_targets": selected,

            "outbound_ready": outbound_ready,

            "research_required": research_required,

            "summary": {
                "recommended": len(
                    selected
                ),

                "outbound_ready": len(
                    outbound_ready
                ),

                "research_required": len(
                    research_required
                ),

                "highest_score": (
                    selected[0][
                        "opportunity_score"
                    ]
                    if selected
                    else None
                ),

                "top_account": (
                    selected[0][
                        "company"
                    ]
                    if selected
                    else None
                ),

                "top_account_readiness": (
                    selected[0][
                        "readiness"
                    ]["status"]
                    if selected
                    else None
                ),
            },
        }
