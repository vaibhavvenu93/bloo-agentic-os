from typing import Dict, List

from apps.api.bloo.brain.store import CompanyBrain


class CriticAgent:
    """
    BLOO Critic Agent

    Reviews recommendations against available evidence and confidence.
    Its job is to challenge weak reasoning before actions are surfaced
    to humans or other agents.
    """

    name = "critic"

    def __init__(self, brain: CompanyBrain):
        self.brain = brain

    def _evidence_for(self, evidence_ids: List[str]) -> List[Dict]:
        evidence = []

        for evidence_id in evidence_ids:
            item = self.brain.evidence.get(evidence_id)

            if item:
                evidence.append(item.model_dump())

        return evidence

    def review_action(self, action: Dict) -> Dict:
        object_id = action.get("object_id")

        supporting_evidence = []
        confidence_scores = []

        insight = self.brain.insights.get(object_id)

        if insight:
            supporting_evidence = self._evidence_for(
                insight.evidence_ids
            )
            confidence_scores.append(insight.confidence)

        if supporting_evidence:
            confidence_scores.extend(
                item["confidence"]
                for item in supporting_evidence
            )

        if confidence_scores:
            confidence = sum(confidence_scores) / len(confidence_scores)
        else:
            confidence = 0.5

        if confidence >= 0.85:
            verdict = "approved"
            risk = "low"
        elif confidence >= 0.65:
            verdict = "review"
            risk = "medium"
        else:
            verdict = "challenge"
            risk = "high"

        return {
            "agent": self.name,
            "object_id": object_id,
            "original_action": action,
            "verdict": verdict,
            "risk": risk,
            "confidence": round(confidence, 2),
            "supporting_evidence": supporting_evidence,
            "questions": self._challenge_questions(
                action=action,
                evidence=supporting_evidence,
            ),
        }

    def _challenge_questions(
        self,
        action: Dict,
        evidence: List[Dict],
    ) -> List[str]:
        questions = []

        if not evidence:
            questions.append(
                "What evidence directly supports this recommendation?"
            )

        if action.get("requires_ceo"):
            questions.append(
                "Does this genuinely require CEO judgment, or can it be delegated?"
            )

        if action.get("priority") == "high":
            questions.append(
                "What is the measurable cost of not acting now?"
            )

        if not questions:
            questions.append(
                "Is this action materially better than doing nothing?"
            )

        return questions

    def review_recommendations(
        self,
        operator_output: Dict,
    ) -> Dict:
        reviews = [
            self.review_action(action)
            for action in operator_output.get(
                "recommended_actions",
                []
            )
        ]

        approved = [
            review
            for review in reviews
            if review["verdict"] == "approved"
        ]

        challenged = [
            review
            for review in reviews
            if review["verdict"] in {"review", "challenge"}
        ]

        return {
            "agent": self.name,
            "reviewed_agent": operator_output.get("agent"),
            "reviews": reviews,
            "summary": {
                "reviewed": len(reviews),
                "approved": len(approved),
                "challenged": len(challenged),
            },
            "approved_actions": approved,
            "challenged_actions": challenged,
        }
