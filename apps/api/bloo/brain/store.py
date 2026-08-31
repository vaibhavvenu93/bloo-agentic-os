from typing import Dict, List, Optional

from .models import (
    Account,
    Action,
    Commitment,
    Decision,
    Evidence,
    Goal,
    Insight,
    Mission,
    Outcome,
    Relationship,
)


class CompanyBrain:
    """
    Structured in-memory company graph for BLOO.

    The Company Brain stores verified evidence, accounts, commitments,
    decisions, actions, insights, outcomes and relationships.

    Higher-level agents can query this structured state rather than inventing
    company facts.
    """

    def __init__(self):
        self.evidence: Dict[str, Evidence] = {}
        self.goals: Dict[str, Goal] = {}
        self.missions: Dict[str, Mission] = {}
        self.accounts: Dict[str, Account] = {}
        self.commitments: Dict[str, Commitment] = {}
        self.decisions: Dict[str, Decision] = {}
        self.insights: Dict[str, Insight] = {}
        self.actions: Dict[str, Action] = {}
        self.outcomes: Dict[str, Outcome] = {}
        self.relationships: List[Relationship] = []

    # ------------------------------------------------------------------
    # WRITE OPERATIONS
    # ------------------------------------------------------------------

    def add_evidence(self, item: Evidence) -> Evidence:
        self.evidence[item.id] = item
        return item

    def add_goal(self, item: Goal) -> Goal:
        self.goals[item.id] = item
        return item

    def add_mission(self, item: Mission) -> Mission:
        self.missions[item.id] = item
        return item

    def add_account(self, item: Account) -> Account:
        self.accounts[item.id] = item
        return item

    def add_commitment(self, item: Commitment) -> Commitment:
        self.commitments[item.id] = item
        return item

    def add_decision(self, item: Decision) -> Decision:
        self.decisions[item.id] = item
        return item

    def add_insight(self, item: Insight) -> Insight:
        self.insights[item.id] = item
        return item

    def add_action(self, item: Action) -> Action:
        self.actions[item.id] = item
        return item

    def add_outcome(self, item: Outcome) -> Outcome:
        self.outcomes[item.id] = item
        return item

    def add_relationship(self, item: Relationship) -> Relationship:
        self.relationships.append(item)
        return item

    # ------------------------------------------------------------------
    # READ OPERATIONS
    # ------------------------------------------------------------------

    def get_account(
        self,
        account_id: str,
    ) -> Optional[Account]:
        return self.accounts.get(account_id)

    def open_commitments(self) -> List[Commitment]:
        return [
            item
            for item in self.commitments.values()
            if item.status != "completed"
        ]

    def open_decisions(self) -> List[Decision]:
        return [
            item
            for item in self.decisions.values()
            if item.status == "open"
        ]

    def relationships_for(
        self,
        object_id: str,
    ) -> List[Relationship]:
        return [
            item
            for item in self.relationships
            if (
                item.source_id == object_id
                or item.target_id == object_id
            )
        ]

    # ------------------------------------------------------------------
    # SERIALIZATION HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize(item):
        """
        Serialize Pydantic models while supporting both Pydantic v1 and v2.
        """

        if item is None:
            return None

        if hasattr(item, "model_dump"):
            return item.model_dump()

        if hasattr(item, "dict"):
            return item.dict()

        if isinstance(item, dict):
            return item

        return {
            key: value
            for key, value in vars(item).items()
            if not key.startswith("_")
        }

    def _serialize_collection(self, items) -> List[dict]:
        return [
            self._serialize(item)
            for item in items
        ]

    # ------------------------------------------------------------------
    # COMPANY GRAPH
    # ------------------------------------------------------------------

    def snapshot(self) -> dict:
        """
        Return the complete structured Company Brain.

        This is the deterministic graph state that agents and future
        reasoning layers can consume.
        """

        return {
            "summary": self.summary(),
            "accounts": self._serialize_collection(
                self.accounts.values()
            ),
            "evidence": self._serialize_collection(
                self.evidence.values()
            ),
            "goals": self._serialize_collection(
                self.goals.values()
            ),
            "missions": self._serialize_collection(
                self.missions.values()
            ),
            "commitments": self._serialize_collection(
                self.commitments.values()
            ),
            "decisions": self._serialize_collection(
                self.decisions.values()
            ),
            "insights": self._serialize_collection(
                self.insights.values()
            ),
            "actions": self._serialize_collection(
                self.actions.values()
            ),
            "outcomes": self._serialize_collection(
                self.outcomes.values()
            ),
            "relationships": self._serialize_collection(
                self.relationships
            ),
        }

    def query_context(
        self,
        account_id: Optional[str] = None,
    ) -> dict:
        """
        Build deterministic context for BLOO's reasoning layer.

        No company fact is generated here. This method only exposes
        information already present in the Company Brain.
        """

        account = None
        relationships = []

        if account_id:
            account = self.get_account(account_id)
            relationships = self.relationships_for(account_id)

        return {
            "account": self._serialize(account),
            "open_commitments": self._serialize_collection(
                self.open_commitments()
            ),
            "open_decisions": self._serialize_collection(
                self.open_decisions()
            ),
            "relationships": self._serialize_collection(
                relationships
            ),
            "summary": self.summary(),
        }

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    def summary(self) -> dict:
        return {
            "evidence": len(self.evidence),
            "goals": len(self.goals),
            "missions": len(self.missions),
            "accounts": len(self.accounts),
            "open_commitments": len(
                self.open_commitments()
            ),
            "open_decisions": len(
                self.open_decisions()
            ),
            "insights": len(self.insights),
            "actions": len(self.actions),
            "outcomes": len(self.outcomes),
            "relationships": len(self.relationships),
        }
