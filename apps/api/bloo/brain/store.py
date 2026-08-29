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

    def account(self, account_id: str) -> Optional[Account]:
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

    def relationships_for(self, object_id: str) -> List[Relationship]:
        return [
            item
            for item in self.relationships
            if item.source_id == object_id or item.target_id == object_id
        ]

    def summary(self) -> dict:
        return {
            "evidence": len(self.evidence),
            "goals": len(self.goals),
            "missions": len(self.missions),
            "accounts": len(self.accounts),
            "open_commitments": len(self.open_commitments()),
            "open_decisions": len(self.open_decisions()),
            "insights": len(self.insights),
            "actions": len(self.actions),
            "outcomes": len(self.outcomes),
            "relationships": len(self.relationships),
        }
