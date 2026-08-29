from fastapi import FastAPI

from apps.api.bloo.agents.critic import CriticAgent
from apps.api.bloo.agents.operator import OperatorAgent
from apps.api.bloo.agents.orchestrator import OrchestratorAgent
from apps.api.bloo.brain.store import CompanyBrain
from examples.blueberry.mellow_sleep import load_mellow_sleep


app = FastAPI(
    title="BLOO",
    description="Agentic operating layer for company intelligence and execution.",
    version="0.4.0",
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
    return brain.accounts


@app.get("/brain/insights")
def insights():
    return brain.insights


@app.get("/brain/commitments")
def commitments():
    return brain.open_commitments()


@app.get("/brain/decisions")
def decisions():
    return brain.open_decisions()


@app.get("/brain/actions")
def actions():
    return brain.actions


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
