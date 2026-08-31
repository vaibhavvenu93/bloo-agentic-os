cat > README.md <<'EOF'
# BLOO

### An agentic commercial operating system built as an outside-in exploration for Blueberry.

> Give me a company. I'll help you win it, deploy it, grow it, and build the system so we can do it 100 more times.

---

## Why I built this

I was exploring Blueberry's Chief of Staff role and kept coming back to one question:

**What would it actually look like to multiply the founder rather than simply help the founder?**

So instead of writing another application, I built a working hypothesis.

BLOO starts with a commercial opportunity, builds an evidence-backed pursuit, identifies what it still does not know, refuses unsafe action, and turns repeated work into operating workflows.

The loop is:

**SELL → DEPLOY → PROVE → EXPAND → OPERATE → LEARN → AUTOMATE**

This is not intended to prescribe how Blueberry should operate internally.

It is an outside-in prototype showing how I think about revenue, customers, systems, AI agents, execution, and founder leverage.

---

## The opening experiment

The prototype begins with a simple claim:

> **Nima, I found you a customer.**

BLOO identifies **MERIT Beauty** as a high-potential commercial opportunity based on publicly available signals around its Australia and New Zealand expansion.

It then builds:

- a "why now" account thesis
- a Blueberry-specific commercial wedge
- a pilot hypothesis
- a deployment path
- a proof phase
- an expansion path
- a research gate before outbound

But there is an important constraint.

BLOO does **not** pretend that public research gives it everything required to sell safely.

If the buyer, stack, CRM state, or other required evidence is unknown, the system blocks outbound.

---

## The agent system

BLOO uses specialist agents rather than one unconstrained assistant.

### Scout

Finds commercially interesting accounts and ranks opportunities.

### Researcher

Determines what is known, what is inferred, and what still needs verification.

### Seller

Builds the commercial pursuit and messaging strategy from available evidence.

It cannot authorize outbound when research requirements remain unresolved.

### Gate

Separates a good commercial hypothesis from permission to act.

Missing evidence remains visible instead of being silently invented.

### Operator

Turns known company state into executable actions.

### Critic

Reviews recommendations before they become operating decisions.

Together:

**Scout → Researcher → Seller → Gate → Operator → Critic**

---

## Ask BLOO

The prototype includes an interactive Company Brain.

Instead of treating company memory as a pile of documents, BLOO models information as a structured company graph.

Objects can represent:

- accounts
- evidence
- commitments
- decisions
- goals
- missions
- actions
- outcomes
- relationships

Ask BLOO queries this operating state alongside the live commercial orchestration state.

For example:

> **Why is MERIT Beauty blocked from outbound?**

BLOO separates:

### What it knows

The public commercial evidence supporting the account thesis.

### What it does not know

The unresolved research required before action.

It then proposes the next operating workflow from those missing states.

---

## Example: MERIT Beauty

The current prototype uses publicly available information indicating a time-bound commercial window around MERIT Beauty's Australia and New Zealand expansion.

The thesis:

Social attention, creator activity, customer intent and new retail distribution are converging around the launch.

The proposed Blueberry wedge:

**Social engagement → AI conversation → identity capture → commerce**

The pilot hypothesis is to convert high-intent launch conversations into permissioned customer identity and attributable downstream revenue.

This is a commercial hypothesis — not a claim that MERIT Beauty is currently a Blueberry prospect or customer.

---

## Research before outbound

A commercially attractive account is not automatically an outbound-ready account.

BLOO maintains a research gate around questions such as:

- Who actually owns the relevant commercial outcome?
- What lifecycle and CRM stack is in place?
- What systems should captured customer identity flow into?
- Is the company already present in Blueberry's CRM or active pipeline?
- Is there enough evidence to justify the proposed outreach?

If those requirements remain unresolved:

**OUTBOUND BLOCKED**

The system does not manufacture a buyer name, fake an email address, or silently convert an assumption into a fact.

This is deliberate.

---

## From opportunity to operating system

Finding an account is useful.

Winning and expanding accounts repeatedly requires infrastructure.

If the account converted, BLOO models the next operating loop.

### Deploy

Connect the relevant surfaces, campaign rules and lifecycle handoff.

### Prove

Measure conversations, identity capture and attributable revenue.

### Expand

Move from launch activation into broader lifecycle automation.

### Operate

Track commitments, actions, decisions and unresolved loops.

### Learn

Store outcomes and evidence back into company memory.

### Automate

Turn repeated operating patterns into reusable workflows.

The goal is not another dashboard.

The goal is a company loop where:

**opportunities become customers → customers become expansion → repeated work becomes systems**

---

## Company Brain

BLOO maintains structured company memory rather than relying only on conversational context.

The current graph supports objects including:

```text
Account
Evidence
Goal
Mission
Commitment
Decision
Insight
Action
Outcome
Relationship
```

The API exposes structured views such as:

```text
/brain
/brain/accounts
/brain/evidence
/brain/commitments
/brain/decisions
/brain/insights
/brain/actions
/brain/relationships
/brain/query
```

`/brain/query` searches explicit company objects and returns inspectable records.

The point is simple:

**agents should reason from company state, not invent company state.**

---

## Founder leverage

The CEO should not become the routing layer for the company.

BLOO therefore separates work the system can safely handle from decisions requiring founder judgment.

The prototype includes a CEO Zone:

> **Good morning, Nima.**

It surfaces what genuinely requires CEO attention and what the operating system handled without escalation.

The broader question behind the prototype is:

**How much organizational throughput can an eight-person company create without proportionally increasing coordination overhead?**

---

## Architecture

```text
             PUBLIC / AUTHORIZED SIGNALS
                        │
                        ▼
                      SCOUT
                        │
                        ▼
                   RESEARCHER
                        │
                        ▼
                     SELLER
                        │
                        ▼
                 RESEARCH GATE
                    ╱       ╲
                   ╱         ╲
              BLOCKED        READY
                               │
                               ▼
                           OPERATOR
                               │
                               ▼
                            CRITIC
                               │
                               ▼
                       COMPANY BRAIN
                               │
                               ▼
                    WORKFLOW GENERATION
```

The commercial operating loop:

```text
SELL
  ↓
DEPLOY
  ↓
PROVE
  ↓
EXPAND
  ↓
OPERATE
  ↓
LEARN
  ↓
AUTOMATE
  └──────────────→ back into SELL
```

---

## Agent orchestration

The backend orchestrator runs the specialist agents as a coordinated system.

Conceptually:

```text
Scout
  │
  ├── finds opportunities
  ▼
Researcher
  │
  ├── identifies missing evidence
  ▼
Seller
  │
  ├── creates pursuits
  ▼
Gate
  │
  ├── authorizes or blocks outbound
  ▼
Operator
  │
  ├── recommends execution
  ▼
Critic
  │
  └── reviews recommendations
```

The frontend consumes this live orchestration state rather than displaying invented operating metrics.

---

## Safety and evidence

This prototype intentionally distinguishes between three kinds of information:

### 1. Verified public information

Publicly observable commercial signals used to build account hypotheses.

### 2. Derived commercial hypotheses

Reasoned conclusions such as why an account may be attractive or what a pilot could look like.

### 3. Private company/customer state

Information BLOO does not possess unless an authorized integration provides it.

The system does not fabricate:

- private CRM state
- customer data
- buyer identity
- verified email addresses
- internal Blueberry decisions
- authorized outreach status

Where evidence is missing, BLOO creates or preserves a research requirement.

---

## Public reference data

The Company Brain currently includes a public-reference fixture based on Blueberry's published Mellow Sleep case study.

This fixture exists to demonstrate how customer evidence, accounts and relationships can be represented in the graph.

It is **not** a live connection to Mellow Sleep or Blueberry.

No private customer information is used.

---

## Apollo integration boundary

BLOO includes an enrichment connector contract and an Apollo implementation for buyer discovery.

The connector is designed to preserve a strict distinction between:

```text
discovered person
verified buyer
enriched contact
outbound-safe contact
```

If enrichment cannot verify the required state, the research gate remains unresolved.

The prototype does not depend on Apollo being available in order to preserve the pursuit itself.

---

## Future authorized connectors

The architecture is designed so public/demo boundaries can later be replaced by authorized integrations.

Examples include:

```text
CRM
Shopify
Klaviyo
Slack
Linear
Apollo
customer data platforms
analytics systems
internal operating databases
```

Live integrations should use:

- explicit authorization
- scoped permissions
- auditable actions
- human confirmation where appropriate
- clear separation between read and write capabilities

---

## Technology

### Backend

- Python
- FastAPI
- Pydantic models
- specialist agent orchestration
- structured Company Brain
- deterministic research gates
- connector abstraction

### Frontend

- React
- Vite
- live FastAPI integration
- interactive Company Brain experience

### Testing

The repository includes automated tests around the orchestration and research-gate behavior.

---

## Repository structure

```text
bloo-agentic-os/
│
├── apps/
│   ├── api/
│   │   └── bloo/
│   │       ├── agents/
│   │       │   ├── scout.py
│   │       │   ├── researcher.py
│   │       │   ├── seller.py
│   │       │   ├── operator.py
│   │       │   ├── critic.py
│   │       │   └── orchestrator.py
│   │       │
│   │       ├── brain/
│   │       │   ├── models.py
│   │       │   └── store.py
│   │       │
│   │       ├── connectors/
│   │       │   ├── enrichment.py
│   │       │   └── apollo.py
│   │       │
│   │       ├── intelligence/
│   │       │   └── commercial.py
│   │       │
│   │       └── main.py
│   │
│   └── web/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── AskBloo.jsx
│       │   ├── App.css
│       │   └── index.css
│       └── package.json
│
├── examples/
│   └── blueberry/
│       └── mellow_sleep.py
│
├── tests/
│
└── README.md
```

---

## Run locally

### 1. Start the API

From the repository root:

```bash
cd bloo-agentic-os
source .venv/bin/activate
uvicorn apps.api.bloo.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Useful endpoints:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/orchestrator
http://127.0.0.1:8000/brain
http://127.0.0.1:8000/brain/query?q=Mellow
```

### 2. Start the web app

Open another terminal:

```bash
cd bloo-agentic-os/apps/web
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

The Vite development server proxies `/api/*` requests to the FastAPI backend.

---

## Try the demo

Once both services are running:

### 1. Start at the commercial thesis

The opening screen presents the highest-priority commercial opportunity.

### 2. Inspect the research gate

Notice that a strong opportunity can still remain blocked from outbound.

### 3. Follow the post-sale path

The prototype models:

```text
DEPLOY → PROVE → EXPAND
```

rather than stopping at lead generation.

### 4. Inspect the CEO Zone

See what required founder attention and what the operating layer handled without escalation.

### 5. Ask BLOO

Scroll to the Company Brain and ask:

> Why is MERIT Beauty blocked from outbound?

BLOO reads the Company Brain and live orchestration state, explains the blocker and proposes the next safe workflow.

---

## What is real today

Working in this repository:

- structured Company Brain
- typed company objects
- public-reference evidence fixture
- commercial opportunity intelligence
- Scout agent
- Researcher agent
- Seller agent
- research/outbound gate
- Operator agent
- Critic agent
- agent orchestrator
- enrichment connector contract
- Apollo connector
- FastAPI endpoints
- live React frontend
- interactive Ask BLOO experience
- workflow recommendation
- automated orchestration tests

---

## What is intentionally not claimed

This prototype does not claim to have:

- Blueberry internal data
- Blueberry CRM access
- private customer data
- live Mellow Sleep access
- permission to contact MERIT Beauty
- production-grade workflow execution
- autonomous writes into Blueberry systems

Those require authorization and real operating context.

---

## What I would do with real access

The next step would **not** be adding more UI.

It would be connecting BLOO to actual operating state:

- enterprise pipeline
- active implementations
- customer commitments
- campaign performance
- expansion opportunities
- product requests
- hiring priorities
- internal decisions
- Slack and Linear operating signals

Then I would measure whether the system actually:

1. reduces founder coordination load,
2. closes more operating loops,
3. improves enterprise execution,
4. increases expansion velocity,
5. turns repeated work into reusable systems.

---

## The point

This repository is not my attempt to guess Blueberry's internal architecture.

It is my answer to the Chief of Staff problem:

> **Can someone move between selling, customer execution, operations, systems and AI — and turn what they learn into leverage for the rest of the company?**

That's the job I want to do.
EOF
