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
        Determine whether an opportunity is ready for outbound
        or still requires evidence validation.
        """

        evidence = account.get(
            "evidence_summary",
            {},
        )

        verified = evidence.get(
            "verified",
            0,
        )

        requires_validation = evidence.get(
            "requires_validation",
            0,
        )

        if requires_validation == 0 and verified > 0:
            status = "outbound_ready"
        elif verified > 0:
            status = "research_before_outbound"
        else:
            status = "validation_required"

        return {
            "status": status,
            "verified_signals": verified,
            "signals_requiring_validation": requires_validation,
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
            "website": account.get("website"),
            "opportunity_score": account.get(
                "opportunity_score"
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

            "evidence": account.get(
                "verified_signals",
                [],
            ),

            "evidence_summary": account.get(
                "evidence_summary",
                {},
            ),

            "readiness": readiness,

            "recommended_next_step": (
                "Validate outstanding public signals before outbound."
                if readiness["status"] == "validation_required"
                else "Prepare the account for commercial outreach."
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
                "commercial attention on, while preventing weak "
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
            },
        }
