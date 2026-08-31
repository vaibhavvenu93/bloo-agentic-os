from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from apps.api.bloo.agents.critic import CriticAgent
from apps.api.bloo.agents.operator import OperatorAgent
from apps.api.bloo.agents.orchestrator import OrchestratorAgent
from apps.api.bloo.brain.store import CompanyBrain
from examples.blueberry.mellow_sleep import load_mellow_sleep


app = FastAPI(
    title="BLOO",
    description="Agentic operating layer for company intelligence and execution.",
    version="0.5.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)



# ---------------------------------------------------------
# COMPANY BRAIN
# ---------------------------------------------------------

brain = CompanyBrain()
load_mellow_sleep(brain)


# ---------------------------------------------------------
# AGENTS
# ---------------------------------------------------------

operator_agent = OperatorAgent(brain)
critic_agent = CriticAgent(brain)
orchestrator_agent = OrchestratorAgent(brain)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def serialize_collection(collection) -> list:
    """
    Convert a CompanyBrain dictionary/list into JSON-safe objects.
    """
    if isinstance(collection, dict):
        values = list(collection.values())
    else:
        values = list(collection)

    result = []

    for item in values:
        if hasattr(item, "model_dump"):
            result.append(item.model_dump())
        elif hasattr(item, "dict"):
            result.append(item.dict())
        else:
            result.append(item)

    return result


def matches_text(item: dict, query: str) -> bool:
    """
    Lightweight structured search across Company Brain objects.

    This deliberately searches structured company objects rather than
    pretending an LLM/RAG layer exists where one does not.
    """
    needle = query.lower().strip()

    if not needle:
        return True

    searchable = " ".join(
        str(value)
        for value in item.values()
        if value is not None
    ).lower()

    return needle in searchable


def filter_by_account(items: list, account_id: Optional[str]) -> list:
    """
    Filter objects to a specific account when the object carries
    account_id directly.

    Objects without an account_id are left available because they may
    be connected through relationships instead.
    """
    if not account_id:
        return items

    filtered = []

    for item in items:
        item_account_id = item.get("account_id")

        if item_account_id == account_id:
            filtered.append(item)

    return filtered


# ---------------------------------------------------------
# CORE
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "product": "BLOO",
        "status": "online",
        "mission": (
            "Help small teams operate with more intelligence, "
            "leverage, and fewer dropped loops."
        ),
        "brain": brain.summary(),
        "agents": {
            "operator": "active",
            "critic": "active",
            "orchestrator": "active",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "product": "BLOO",
        "version": "0.5.0",
    }


# ---------------------------------------------------------
# COMPANY BRAIN API
# ---------------------------------------------------------

@app.get("/brain")
def brain_summary():
    return {
        "company": "Blueberry",
        "reference_customer": "Mellow Sleep",
        "mode": "public-reference-demo",
        "summary": brain.summary(),
    }


@app.get("/brain/accounts")
def accounts():
    return serialize_collection(brain.accounts)


@app.get("/brain/insights")
def insights():
    return serialize_collection(brain.insights)


@app.get("/brain/commitments")
def commitments():
    return serialize_collection(brain.open_commitments())


@app.get("/brain/decisions")
def decisions():
    return serialize_collection(brain.open_decisions())


@app.get("/brain/actions")
def actions():
    return serialize_collection(brain.actions)


@app.get("/brain/evidence")
def evidence():
    return serialize_collection(brain.evidence)


@app.get("/brain/goals")
def goals():
    return serialize_collection(brain.goals)


@app.get("/brain/missions")
def missions():
    return serialize_collection(brain.missions)


@app.get("/brain/outcomes")
def outcomes():
    return serialize_collection(brain.outcomes)


@app.get("/brain/relationships")
def relationships():
    return serialize_collection(brain.relationships)


@app.get("/brain/query")
def query_brain(
    q: str = Query(
        default="",
        description="Text to search across structured Company Brain objects.",
    ),
    object_type: Optional[str] = Query(
        default=None,
        description=(
            "Optional object type: accounts, evidence, goals, missions, "
            "commitments, decisions, insights, actions, outcomes, relationships."
        ),
    ),
    account_id: Optional[str] = Query(
        default=None,
        description="Optional account ID filter.",
    ),
):
    """
    Query BLOO's structured Company Brain.

    This is intentionally not generic vector search.

    The endpoint searches explicit company objects and returns the
    underlying records so an operator or agent can reason from
    inspectable evidence.
    """

    collections = {
        "accounts": serialize_collection(brain.accounts),
        "evidence": serialize_collection(brain.evidence),
        "goals": serialize_collection(brain.goals),
        "missions": serialize_collection(brain.missions),
        "commitments": serialize_collection(brain.commitments),
        "decisions": serialize_collection(brain.decisions),
        "insights": serialize_collection(brain.insights),
        "actions": serialize_collection(brain.actions),
        "outcomes": serialize_collection(brain.outcomes),
        "relationships": serialize_collection(brain.relationships),
    }

    if object_type:
        normalized_type = object_type.lower().strip()

        if normalized_type not in collections:
            return {
                "status": "invalid_object_type",
                "query": q,
                "object_type": object_type,
                "allowed_types": list(collections.keys()),
                "results": [],
                "count": 0,
            }

        collections = {
            normalized_type: collections[normalized_type]
        }

    results = []

    for collection_name, items in collections.items():
        account_filtered_items = filter_by_account(
            items,
            account_id,
        )

        for item in account_filtered_items:
            if matches_text(item, q):
                results.append(
                    {
                        "object_type": collection_name,
                        "object": item,
                    }
                )

    return {
        "status": "ok",
        "query": q,
        "object_type": object_type,
        "account_id": account_id,
        "count": len(results),
        "results": results,
        "brain_summary": brain.summary(),
        "source_mode": "structured-company-graph",
    }


# ---------------------------------------------------------
# AGENT API
# ---------------------------------------------------------

@app.get("/operator")
def operator():
    return operator_agent.recommend()


@app.get("/critic")
def critic():
    operator_output = operator_agent.recommend()
    return critic_agent.review_recommendations(operator_output)


@app.get("/orchestrator")
def orchestrator():
    return orchestrator_agent.run()
