from typing import Dict, List


class ScoutAgent:
    """
    BLOO Scout Agent

    Identifies companies worth pursuing based on commercial
    triggers, fit, urgency, and similarity to known successful
    customer patterns.
    """

    name = "scout"

    def __init__(self):
        self.targets = self._seed_targets()

    def _seed_targets(self) -> List[Dict]:
        """
        Initial target set.

        These are structured as public-signal targets.
        We will replace/expand these with live research,
        Apollo, Clay, CRM checks, and current external signals.
        """

        return [
            {
                "id": "target_merit_beauty",
                "company": "MERIT Beauty",
                "industry": "Beauty / DTC",
                "trigger": (
                    "International retail expansion creates a "
                    "time-sensitive customer acquisition moment."
                ),
                "why_now": (
                    "Expansion increases social conversation, product "
                    "discovery, and purchase-intent opportunities."
                ),
                "blueberry_wedge": (
                    "Turn launch-driven social engagement into "
                    "personalized conversations, owned customer data, "
                    "and attributable commerce."
                ),
                "fit_score": 94,
                "urgency_score": 95,
                "confidence": 0.86,
                "evidence_status": "public_signal",
            },
            {
                "id": "target_social_beauty_01",
                "company": "Emerging Beauty Brand",
                "industry": "Beauty / Social Commerce",
                "trigger": (
                    "Rapid social-commerce growth and creator-led "
                    "distribution."
                ),
                "why_now": (
                    "High growth can create large volumes of unmanaged "
                    "purchase-intent conversations."
                ),
                "blueberry_wedge": (
                    "Convert creator and social engagement into "
                    "identifiable, attributable customers."
                ),
                "fit_score": 88,
                "urgency_score": 84,
                "confidence": 0.62,
                "evidence_status": "hypothesis",
            },
            {
                "id": "target_sports_01",
                "company": "Growth Sports Franchise",
                "industry": "Sports / Entertainment",
                "trigger": (
                    "Large fan engagement with limited direct "
                    "one-to-one commercial interaction."
                ),
                "why_now": (
                    "Fan communities increasingly expect direct, "
                    "personalized digital engagement."
                ),
                "blueberry_wedge": (
                    "Turn fan social engagement into personalized "
                    "conversations, known audiences, and commerce."
                ),
                "fit_score": 86,
                "urgency_score": 79,
                "confidence": 0.58,
                "evidence_status": "hypothesis",
            },
        ]

    def rank_targets(self) -> List[Dict]:
        ranked = []

        for target in self.targets:
            score = round(
                (
                    target["fit_score"] * 0.55
                    + target["urgency_score"] * 0.45
                ),
                1,
            )

            ranked.append(
                {
                    **target,
                    "opportunity_score": score,
                }
            )

        return sorted(
            ranked,
            key=lambda item: item["opportunity_score"],
            reverse=True,
        )

    def recommend(self, limit: int = 3) -> Dict:
        ranked = self.rank_targets()
        selected = ranked[:limit]

        return {
            "agent": self.name,
            "objective": (
                "Find companies where Blueberry has a credible "
                "reason to start a commercial conversation now."
            ),
            "targets_considered": len(ranked),
            "recommended_targets": selected,
            "summary": {
                "recommended": len(selected),
                "highest_score": (
                    selected[0]["opportunity_score"]
                    if selected
                    else None
                ),
            },
        }
