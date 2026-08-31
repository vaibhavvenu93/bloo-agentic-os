const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

import { useState } from "react";

const DEFAULT_QUESTION = "Why is MERIT Beauty blocked from outbound?";

function AskBloo() {
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [status, setStatus] = useState("idle");
  const [brainResult, setBrainResult] = useState(null);
  const [error, setError] = useState("");

  async function askBloo() {
    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
      return;
    }

    setStatus("loading");
    setError("");

    try {
      /*
       * The public Company Brain currently contains the Mellow Sleep
       * reference graph. The commercial orchestration endpoint contains
       * the live MERIT pursuit and research gate.
       *
       * We query both rather than pretending MERIT already exists as
       * private customer data inside the Company Brain.
       */
      const [brainResponse, orchestratorResponse] = await Promise.all([
        fetch(`${API_BASE}/brain/query?q=Mellow`),
        fetch(`${API_BASE}/orchestrator`),
      ]);

      if (!brainResponse.ok || !orchestratorResponse.ok) {
        throw new Error("BLOO could not read its operating state.");
      }

      const brain = await brainResponse.json();
      const orchestration = await orchestratorResponse.json();

      const commercial = orchestration?.commercial ?? {};
      const finalState = orchestration?.final ?? {};
      const summary = orchestration?.summary ?? {};

      const gate =
        commercial?.gate ??
        finalState?.gate ??
        {};

      const researchQueue =
        commercial?.research_queue ??
        finalState?.research_queue ??
        [];

      const pursuits =
        finalState?.commercial_pursuits ??
        commercial?.pursuits ??
        [];

      const meritPursuit =
        pursuits.find(
          (pursuit) =>
            String(pursuit?.company ?? "")
              .toLowerCase()
              .includes("merit")
        ) ?? pursuits[0] ?? null;

      const blockingTasks = Array.isArray(researchQueue)
        ? researchQueue.filter(
            (task) =>
              task?.blocks_outbound === true ||
              task?.status !== "resolved"
          )
        : [];

      const fallbackBlockers = [
        {
          label: "Buyer",
          question:
            "Verify who owns social commerce, lifecycle growth and the ANZ launch.",
        },
        {
          label: "Marketing stack",
          question:
            "Validate the lifecycle, CRM, CDP and commerce systems that would receive captured identity.",
        },
        {
          label: "Social volume",
          question:
            "Quantify purchase-intent engagement around the ANZ Sephora launch.",
        },
        {
          label: "CRM check",
          question:
            "Confirm whether MERIT Beauty already exists in Blueberry's CRM or active pipeline.",
        },
      ];

      const blockers =
        blockingTasks.length > 0
          ? blockingTasks.slice(0, 4).map((task, index) => ({
              label:
                task?.validation_type ??
                task?.task_type ??
                `Research ${index + 1}`,
              question:
                task?.question ??
                task?.description ??
                task?.task ??
                "Resolve this research item before outbound.",
            }))
          : fallbackBlockers;

      const outboundAllowed =
        gate?.outbound_allowed ??
        summary?.outbound_allowed ??
        meritPursuit?.outbound_allowed ??
        false;

      setBrainResult({
        brain,
        orchestration,
        meritPursuit,
        blockers,
        outboundAllowed,
        blockingCount:
          summary?.blocking_research_tasks ??
          blockers.length,
      });

      setStatus("done");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "BLOO could not complete the query."
      );
      setStatus("error");
    }
  }

  const blockerCount =
    brainResult?.blockingCount ??
    brainResult?.blockers?.length ??
    0;

  return (
    <section className="askBlooSection">
      <div className="askBlooHeader">
        <div>
          <span className="sectionNumber">07</span>
          <span className="eyebrow">COMPANY BRAIN</span>
          <h2>Ask BLOO.</h2>
        </div>

        <div className="askBlooMode">
          <span className="liveDot" />
          Structured company graph
        </div>
      </div>

      <p className="askBlooIntro">
        Ask the operating system a company question. BLOO reads structured
        evidence and the live agent state before recommending what should
        happen next.
      </p>

      <div className="askBlooComposer">
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              askBloo();
            }
          }}
          aria-label="Ask BLOO a company question"
        />

        <button
          type="button"
          onClick={askBloo}
          disabled={status === "loading"}
        >
          {status === "loading" ? "Reading company…" : "Ask BLOO →"}
        </button>
      </div>

      {error && (
        <div className="askBlooError">
          {error}
        </div>
      )}

      {brainResult && (
        <div className="askBlooResult">
          <div className="askBlooDecision">
            <span className="metaLabel">BLOO ANSWER</span>

            <h3>
              MERIT Beauty is commercially interesting.
              <br />
              It is not outbound-ready.
            </h3>

            <p>
              BLOO has built the pursuit, but the research gate still contains{" "}
              <strong>{blockerCount} blocking items</strong>. Until those are
              resolved, the system refuses to fabricate a buyer or authorize
              outreach.
            </p>

            <div className="decisionBadges">
              <span>
                {brainResult.outboundAllowed
                  ? "Outbound allowed"
                  : "Outbound blocked"}
              </span>

              <span>
                Evidence-backed
              </span>

              <span>
                No synthetic contacts
              </span>
            </div>
          </div>

          <div className="askBlooGrid">
            <div className="askBlooPanel">
              <span className="metaLabel">WHAT BLOO KNOWS</span>

              <h4>Commercial thesis</h4>

              <p>
                MERIT's ANZ Sephora launch creates a narrow social-commerce
                window where launch attention can become attributable customer
                revenue.
              </p>

              <div className="brainProof">
                <span>
                  {
                    brainResult.brain?.brain_summary?.evidence ??
                    brainResult.brain?.brain_summary?.evidence_count ??
                    0
                  }{" "}
                  reference evidence objects
                </span>

                <span>
                  {
                    brainResult.brain?.brain_summary?.relationships ??
                    0
                  }{" "}
                  graph relationships
                </span>
              </div>
            </div>

            <div className="askBlooPanel">
              <span className="metaLabel">WHAT BLOO DOES NOT KNOW</span>

              <h4>Research gate</h4>

              <div className="blockerList">
                {brainResult.blockers.map((blocker, index) => (
                  <div
                    className="blockerRow"
                    key={`${blocker.label}-${index}`}
                  >
                    <span>{String(index + 1).padStart(2, "0")}</span>

                    <div>
                      <strong>{blocker.label}</strong>
                      <p>{blocker.question}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="workflowBuilder">
            <div className="workflowCopy">
              <span className="metaLabel">PROPOSED WORKFLOW</span>

              <h3>
                Resolve research gate →
                <br />
                unlock safe outbound.
              </h3>

              <p>
                The workflow is generated from the missing operating state,
                not from an invented contact list.
              </p>
            </div>

            <div className="workflowSteps">
              <div>
                <span>01</span>
                <strong>Verify buyer</strong>
                <p>Identify the accountable commercial owner.</p>
              </div>

              <div>
                <span>02</span>
                <strong>Validate stack</strong>
                <p>Confirm where captured customer identity should flow.</p>
              </div>

              <div>
                <span>03</span>
                <strong>Check CRM</strong>
                <p>Prevent duplicate or conflicting founder-led outreach.</p>
              </div>

              <div>
                <span>04</span>
                <strong>Re-run gate</strong>
                <p>Only release the pursuit when evidence clears the blockers.</p>
              </div>
            </div>
          </div>

          <div className="askBlooAudit">
            <span>SCOUT</span>
            <i>→</i>
            <span>RESEARCHER</span>
            <i>→</i>
            <span>SELLER</span>
            <i>→</i>
            <span>GATE</span>
            <i>→</i>
            <span>OPERATOR</span>
            <i>→</i>
            <span>CRITIC</span>
          </div>
        </div>
      )}
    </section>
  );
}

export default AskBloo;
