from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class EvidenceStatus(str, Enum):
    VERIFIED = "verified"
    LIVE = "live"
    HYPOTHESIS = "hypothesis"


class Evidence(BaseModel):
    id: str
    statement: str
    source: str
    status: EvidenceStatus
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Relationship(BaseModel):
    source_id: str
    relationship: str
    target_id: str


class Goal(BaseModel):
    id: str
    name: str
    description: str
    owner: Optional[str] = None
    status: str = "active"


class Mission(BaseModel):
    id: str
    goal_id: Optional[str] = None
    name: str
    objective: str
    success_condition: str
    status: str = "planned"
    owner: Optional[str] = None


class Account(BaseModel):
    id: str
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    stage: str = "prospect"
    evidence_ids: List[str] = []


class Customer(BaseModel):
    id: str
    account_id: str
    objective: str
    activation_status: str = "not_started"
    expansion_status: str = "unknown"


class Commitment(BaseModel):
    id: str
    description: str
    owner: str
    recipient: Optional[str] = None
    due_at: Optional[datetime] = None
    status: str = "open"
    source_evidence_id: Optional[str] = None


class Decision(BaseModel):
    id: str
    question: str
    owner: Optional[str] = None
    recommendation: Optional[str] = None
    status: str = "open"
    evidence_ids: List[str] = []


class Insight(BaseModel):
    id: str
    title: str
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_ids: List[str] = []


class Action(BaseModel):
    id: str
    action_type: str
    description: str
    owner: Optional[str] = None
    requires_approval: bool = True
    status: str = "proposed"


class Outcome(BaseModel):
    id: str
    action_id: str
    result: str
    success: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)
