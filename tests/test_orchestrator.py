from apps.api.bloo.agents.orchestrator import OrchestratorAgent
from apps.api.bloo.brain.store import CompanyBrain


def run_orchestrator():
    return OrchestratorAgent(CompanyBrain()).run()


def test_orchestrator_returns_core_sections():
    result = run_orchestrator()

    assert "commercial" in result
    assert "operations" in result
    assert "final" in result
    assert "summary" in result
    assert "workflow" in result


def test_commercial_opportunities_become_pursuits():
    result = run_orchestrator()
    summary = result["summary"]

    assert summary["commercial_opportunities"] == 3
    assert summary["commercial_pursuits"] == 3


def test_unresolved_research_blocks_outbound():
    result = run_orchestrator()

    summary = result["summary"]
    gate = result["commercial"]["gate"]

    assert summary["blocking_research_tasks"] > 0
    assert summary["outbound_allowed"] is False

    assert gate["status"] == "research_blocked"
    assert gate["outbound_allowed"] is False
    assert gate["blocking_tasks"] > 0


def test_workflow_contains_agent_execution():
    result = run_orchestrator()

    workflow = result["workflow"]

    assert isinstance(workflow, list)
    assert len(workflow) > 0

    agents = {
        step.get("agent")
        for step in workflow
    }

    assert "scout" in agents
    assert "researcher" in agents
    assert "seller" in agents
    assert "operator" in agents
    assert "critic" in agents
    assert "orchestrator" in agents


def test_no_fake_outbound_when_research_is_unresolved():
    result = run_orchestrator()

    gate = result["commercial"]["gate"]

    assert gate["outbound_allowed"] is False

    pursuits = result["final"].get(
        "commercial_pursuits",
        [],
    )

    for pursuit in pursuits:
        assert pursuit.get("outbound_allowed") is not True
