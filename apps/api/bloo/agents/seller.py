from typing import Dict, List, Optional


class SellerAgent:
    """
    BLOO Seller Agent

    Converts a Scout opportunity into a structured enterprise pursuit.

    It does not invent private company information.
    Public evidence, inferred buyer hypotheses, and proposed actions
    remain clearly separated.
    """

    name = "seller"

    def build_pursuit(
        self,
        target: Dict,
    ) -> Dict:

        company = target.get(
            "company",
            "Unknown company",
        )

        opportunity_score = target.get(
            "opportunity_score",
            0,
        )

        confidence = target.get(
            "confidence",
            0.5,
        )

        return {
            "agent": self.name,
            "account": {
                "id": target.get("id"),
                "company": company,
                "industry": target.get("industry"),
                "opportunity_score": opportunity_score,
            },

            # -----------------------------------------
            # WHY THIS ACCOUNT
            # -----------------------------------------

            "why_now": {
                "trigger": target.get("trigger"),
                "reason": target.get("why_now"),
                "evidence_status": target.get(
                    "evidence_status",
                    "hypothesis",
                ),
                "confidence": confidence,
            },

            # -----------------------------------------
            # COMMERCIAL THESIS
            # -----------------------------------------

            "commercial_thesis": (
                f"{company} appears to have a timely opportunity "
                "for Blueberry to convert high-intent social "
                "engagement into personalized conversations, "
                "owned customer data, and attributable revenue."
            ),

            "blueberry_wedge": target.get(
                "blueberry_wedge"
            ),

            # -----------------------------------------
            # BUYING COMMITTEE HYPOTHESIS
            # -----------------------------------------

            "buying_committee": [
                {
                    "role": "CMO / Chief Growth Officer",
                    "type": "economic_buyer",
                    "message": (
                        "Incremental revenue, customer intelligence, "
                        "and measurable commercial impact."
                    ),
                    "status": "hypothesis",
                },
                {
                    "role": "VP Ecommerce / Growth",
                    "type": "commercial_champion",
                    "message": (
                        "Convert social purchase intent into "
                        "measurable commerce."
                    ),
                    "status": "hypothesis",
                },
                {
                    "role": "Head of Social / Community",
                    "type": "operational_champion",
                    "message": (
                        "Personalize high-volume customer "
                        "engagement without losing brand voice."
                    ),
                    "status": "hypothesis",
                },
                {
                    "role": "Lifecycle / CRM Lead",
                    "type": "stakeholder",
                    "message": (
                        "Turn previously anonymous social audiences "
                        "into lifecycle-ready customer profiles."
                    ),
                    "status": "hypothesis",
                },
            ],

            # -----------------------------------------
            # PILOT DESIGN
            # -----------------------------------------

            "pilot": {
                "name": (
                    f"{company} Social-to-Revenue Pilot"
                ),
                "duration_days": 30,
                "scope": (
                    "One campaign, one high-intent social motion, "
                    "and one measurable conversion objective."
                ),
                "hypothesis": (
                    "Blueberry can monetize social interactions "
                    "that currently contain purchase intent but "
                    "do not reliably become known customers."
                ),
                "success_metrics": [
                    "conversation response rate",
                    "email / SMS capture",
                    "conversion rate",
                    "attributed revenue",
                    "time to first attributable sale",
                ],
            },

            # -----------------------------------------
            # SALES MOTION
            # -----------------------------------------

            "discovery_questions": [
                (
                    "What happens today when somebody shows "
                    "purchase intent in a comment or DM?"
                ),
                (
                    "How much of that audience becomes a known "
                    "email or SMS customer?"
                ),
                (
                    "Can downstream revenue be attributed back "
                    "to those conversations?"
                ),
                (
                    "Where does manual community management "
                    "stop scaling?"
                ),
                (
                    "What would make a 30-day pilot "
                    "economically undeniable?"
                ),
            ],

            "outreach": {
                "angle": (
                    "Lead with the current commercial trigger, "
                    "not a generic Blueberry platform pitch."
                ),
                "draft": (
                    f"I noticed the current momentum around "
                    f"{company}. It made me wonder how much "
                    "high-intent social engagement is currently "
                    "turning into identifiable customers and "
                    "attributable revenue. Rather than pitch a "
                    "broad platform, I'd test one campaign where "
                    "Blueberry turns that engagement into "
                    "personalized conversations and measurable "
                    "commerce."
                ),
                "requires_human_approval": True,
            },

            # -----------------------------------------
            # RISK / VALIDATION
            # -----------------------------------------

            "unknowns": [
                "Exact buyer names need enrichment.",
                "Existing CRM ownership must be checked.",
                "Current commerce and lifecycle stack must be verified.",
                "Social-intent volume must be validated.",
                "Economic value of the opportunity must be quantified.",
            ],

            "next_actions": [
                "Check whether the account already exists in CRM.",
                "Enrich the buying committee through Apollo / Clay.",
                "Verify the external trigger and relevant evidence.",
                "Identify one concrete campaign for the pilot.",
                "Create personalized multi-threaded outreach.",
            ],

            "confidence": confidence,
        }

    def build_from_scout(
        self,
        scout_output: Dict,
        limit: Optional[int] = None,
    ) -> Dict:

        targets: List[Dict] = scout_output.get(
            "recommended_targets",
            [],
        )

        if limit is not None:
            targets = targets[:limit]

        pursuits = [
            self.build_pursuit(target)
            for target in targets
        ]

        return {
            "agent": self.name,
            "received_from": "scout",
            "objective": (
                "Turn high-priority account signals into "
                "credible enterprise sales motions."
            ),
            "pursuits": pursuits,
            "summary": {
                "targets_received": len(targets),
                "pursuits_created": len(pursuits),
                "top_account": (
                    pursuits[0]["account"]["company"]
                    if pursuits
                    else None
                ),
            },
        }
