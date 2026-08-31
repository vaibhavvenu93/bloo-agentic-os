const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

import { useEffect, useMemo, useState } from "react";
import "./App.css";
import AskBloo from "./AskBloo";

const fallbackEvidence = [
  "MERIT is scheduled to launch in-store and online with Sephora Australia and New Zealand on September 30, 2026.",
  "The launch creates a narrow, high-intent window where social attention can convert into attributable customer revenue.",
  "MERIT has strong DTC characteristics and visible social-commerce behavior.",
  "Blueberry can sit between social engagement and purchase intent without requiring MERIT to rebuild its lifecycle stack.",
];

const fallbackResearch = [
  {
    label: "Buyer",
    status: "Blocked",
    detail: "Economic buyer not yet verified.",
  },
  {
    label: "CRM",
    status: "Open",
    detail: "Current lifecycle stack still needs validation.",
  },
  {
    label: "Marketing stack",
    status: "Open",
    detail: "Public evidence is incomplete.",
  },
  {
    label: "Social volume",
    status: "Open",
    detail: "Campaign-level intent volume needs validation.",
  },
];

function titleCase(value = "") {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function App() {
  const [data, setData] = useState(null);
  const [apiState, setApiState] = useState("loading");

  useEffect(() => {
    async function loadBloo() {
      try {
        const response = await fetch(`${API_BASE}/orchestrator`);

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const payload = await response.json();

        setData(payload);
        setApiState("live");
      } catch (error) {
        console.error("BLOO API unavailable:", error);
        setApiState("fallback");
      }
    }

    loadBloo();
  }, []);

  const summary = data?.summary ?? {};
  const commercial = data?.commercial ?? {};
  const scout = commercial?.scout ?? {};
  const researcher = commercial?.researcher ?? {};
  const gate = commercial?.gate ?? {};

  const targets =
    scout?.recommended_targets ??
    scout?.recommendations ??
    [];

  const topTarget = targets[0] ?? {};

  const topCompany =
    topTarget.company ??
    summary.top_account ??
    "MERIT Beauty";

  const opportunityScore =
    topTarget.opportunity_score ??
    topTarget.score ??
    scout?.summary?.highest_score ??
    96;

  const commercialState =
    gate.status ??
    "research_blocked";

  const outboundAllowed =
    gate.outbound_allowed ??
    summary.outbound_allowed ??
    false;

  const blockingCount =
    summary.blocking_research_tasks ??
    gate.blocking_tasks ??
    0;

  const pursuits =
    summary.commercial_pursuits ??
    0;

  const opportunities =
    summary.commercial_opportunities ??
    0;

  const requiresCeo =
    summary.requires_ceo ??
    0;

  const handledWithoutCeo =
    summary.handled_without_ceo ??
    0;

  const operatorActions =
    summary.operator_actions ??
    0;

  const criticReviewed =
    summary.critic_reviewed ??
    0;

  const evidence = useMemo(() => {
    const raw =
      topTarget.evidence ??
      topTarget.verified_signals ??
      [];

    if (!Array.isArray(raw) || raw.length === 0) {
      return fallbackEvidence;
    }

    return raw
      .slice(0, 4)
      .map((item) =>
        typeof item === "string"
          ? item
          : item.statement ??
            item.summary ??
            item.description
      )
      .filter(Boolean);
  }, [topTarget]);

  const researchTasks = useMemo(() => {
    const queue =
      researcher.research_queue ??
      commercial.research_queue ??
      [];

    if (!Array.isArray(queue) || queue.length === 0) {
      return fallbackResearch;
    }

    const companyTasks = queue
      .filter(
        (task) =>
          !task.company ||
          task.company === topCompany
      )
      .slice(0, 4);

    if (companyTasks.length === 0) {
      return fallbackResearch;
    }

    return companyTasks.map((task) => ({
      label: titleCase(
        task.validation_type ??
          task.type ??
          "Research"
      ),
      status:
        task.status === "resolved"
          ? "Resolved"
          : task.blocks_outbound
          ? "Blocked"
          : titleCase(task.status ?? "Open"),
      detail:
        task.question ??
        task.description ??
        "Further validation required.",
    }));
  }, [researcher, commercial, topCompany]);

  return (
    <main className="shell">
      <section className="hero">
        <div className="heroTop">
          <div className="eyebrow">
            BLOO // COMMERCIAL INTELLIGENCE
          </div>

          <div className={`liveBadge ${apiState}`}>
            <span />
            {apiState === "live"
              ? "LIVE AGENT SYSTEM"
              : apiState === "loading"
              ? "CONNECTING"
              : "DEMO FALLBACK"}
          </div>
        </div>

        <div>
          <h1>Nima, I found you a customer.</h1>

          <p className="subhead">
            BLOO found a live commercial window, built the account thesis,
            created the pursuit, and stopped itself before unsafe outbound.
          </p>
        </div>

        <div className="heroMeta">
          <div>
            <span className="metaLabel">Top account</span>
            <strong>{topCompany}</strong>
          </div>

          <div>
            <span className="metaLabel">Opportunity score</span>
            <strong>{opportunityScore} / 100</strong>
          </div>

          <div>
            <span className="metaLabel">Commercial state</span>
            <strong className="blockedText">
              {titleCase(commercialState)}
            </strong>
          </div>
        </div>
      </section>

      <section className="systemStrip">
        <div>
          <span>Opportunities</span>
          <strong>{opportunities}</strong>
        </div>

        <div>
          <span>Pursuits built</span>
          <strong>{pursuits}</strong>
        </div>

        <div>
          <span>Blocking research</span>
          <strong>{blockingCount}</strong>
        </div>

        <div>
          <span>Outbound</span>
          <strong className={outboundAllowed ? "safe" : "danger"}>
            {outboundAllowed ? "Allowed" : "Blocked"}
          </strong>
        </div>
      </section>

      <section className="grid two">
        <article className="panel">
          <span className="sectionIndex">01</span>

          <h2>Why now</h2>

          <p className="lead">
            {topCompany} is entering a launch moment where social conversation,
            purchase intent, creator attention and new retail distribution
            converge.
          </p>

          <div className="signalStack">
            {evidence.map((item, index) => (
              <div className="signal" key={`${item}-${index}`}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <p>{item}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="panel dark">
          <span className="sectionIndex">02</span>

          <h2>The Blueberry wedge</h2>

          <p className="lead">
            Turn launch attention into identifiable customers and attributable
            revenue.
          </p>

          <div className="flow">
            <div>Social engagement</div>
            <span>→</span>
            <div>AI conversation</div>
            <span>→</span>
            <div>Identity capture</div>
            <span>→</span>
            <div>Commerce</div>
          </div>

          <div className="pilot">
            <span className="metaLabel">Pilot hypothesis</span>

            <p>
              Activate high-intent conversations around the launch, capture
              permissioned customer identity, connect it into lifecycle
              systems, and attribute downstream revenue.
            </p>
          </div>
        </article>
      </section>

      <section className="panel researchPanel">
        <div className="sectionHeader">
          <div>
            <span className="sectionIndex">03</span>
            <h2>Research before outbound</h2>
          </div>

          <div className="gateBadge">
            {outboundAllowed
              ? "OUTBOUND CLEARED"
              : "OUTBOUND BLOCKED"}
          </div>
        </div>

        <div className="researchGrid">
          {researchTasks.map((item) => (
            <div className="researchCard" key={item.label}>
              <div className="researchTop">
                <strong>{item.label}</strong>
                <span>{item.status}</span>
              </div>

              <p>{item.detail}</p>
            </div>
          ))}
        </div>

        <div className="safetyCallout">
          <div>
            <span className="metaLabel">Agent decision</span>

            <h3>
              {outboundAllowed
                ? "Research gate cleared."
                : "Do not invent the buyer."}
            </h3>
          </div>

          <p>
            BLOO separates commercial strategy from permission to act.
            Buyer discovery can fail without collapsing the pursuit.
            Unverified contact data never becomes authorized outbound.
          </p>
        </div>
      </section>

      <section className="grid two">
        <article className="panel">
          <span className="sectionIndex">04</span>

          <h2>If {topCompany} says yes tomorrow</h2>

          <div className="timeline">
            <div>
              <span>Day 0–2</span>
              <strong>Deploy</strong>
              <p>
                Connect social surfaces, campaign rules and lifecycle handoff.
              </p>
            </div>

            <div>
              <span>Day 3–10</span>
              <strong>Prove</strong>
              <p>
                Measure conversations, identity capture and attributable
                revenue.
              </p>
            </div>

            <div>
              <span>Day 11–30</span>
              <strong>Expand</strong>
              <p>
                Move from launch activation into always-on lifecycle automation.
              </p>
            </div>
          </div>
        </article>

        <article className="panel">
          <span className="sectionIndex">05</span>

          <h2>Then make it repeatable</h2>

          <div className="loop">
            <span>SELL</span>
            <span>DEPLOY</span>
            <span>PROVE</span>
            <span>EXPAND</span>
            <span>OPERATE</span>
            <span>LEARN</span>
            <span>AUTOMATE</span>
          </div>

          <p className="muted">
            The goal is not another dashboard. It is a company loop where
            opportunities become customers, customers become expansion, and
            repeated work becomes systems.
          </p>
        </article>
      </section>

      <section className="panel ceo">
        <span className="sectionIndex">06</span>

        <div className="ceoGrid">
          <div>
            <div className="eyebrow">CEO ZONE</div>

            <h2>Good morning, Nima.</h2>

            <p className="lead">
              The operating system separates founder judgment from work the
              agents can safely handle on their own.
            </p>

            <div className="agentAudit">
              <span>{operatorActions} operator action</span>
              <span>{criticReviewed} critic review</span>
            </div>
          </div>

          <div className="ceoNumbers">
            <div>
              <strong>{requiresCeo}</strong>
              <span>require you</span>
            </div>

            <div>
              <strong>{handledWithoutCeo}</strong>
              <span>handled without you</span>
            </div>
          </div>
        </div>
      </section>

      <AskBloo />

      <footer>
        <span>BLOO</span>

        <p>
          Give me a company. I’ll help you win it, deploy it, grow it, and build
          the system so we can do it 100 more times.
        </p>
      </footer>
    </main>
  );
}

export default App;
