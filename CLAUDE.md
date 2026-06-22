# CLAUDE.md — Web Form Customer Success Agent
## WaheedAI Solutions — Client Showcase Project

---

## Project Overview

**Goal:** Build a production-grade, 24/7 AI-powered Customer Success Agent for SaaS businesses — handling all customer support inquiries via an embeddable **Web Form**, fully automated and scalable.

**Positioning:** This is a **real client-facing product** built by WaheedAI Solutions. It demonstrates our capability to deliver enterprise-level AI automation at a fraction of the cost of a human support team ($75,000/year human FTE → under $1,000/year AI FTE).

**Scope:** Web Support Form → FastAPI Backend → OpenAI Agents SDK → PostgreSQL → Kafka → Kubernetes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js (React) — Web Support Form |
| Backend API | FastAPI (Python) |
| AI Agent | OpenAI Agents SDK |
| Database/CRM | PostgreSQL 16 + pgvector |
| Event Streaming | Apache Kafka (Confluent Cloud) |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | uv (Python) |

---

## Project Structure

```
customer-support-agent/
├── .claude/
│   └── skills/                    # Claude Code skill files
├── docs/
│   └── project-reference.md       # Full project spec
├── context/
│   ├── company-profile.md         # Client SaaS company profile
│   ├── product-docs.md            # Product documentation (KB)
│   ├── sample-tickets.json        # Sample web form tickets
│   ├── escalation-rules.md        # When to involve humans
│   └── brand-voice.md             # Company tone & voice
├── backend/
│   ├── agent/
│   │   ├── customer_success_agent.py   # OpenAI Agents SDK agent
│   │   ├── tools.py                    # @function_tool definitions
│   │   ├── prompts.py                  # System prompts
│   │   └── formatters.py              # Web response formatting
│   ├── channels/
│   │   └── web_form_handler.py         # Web form API handler
│   ├── workers/
│   │   ├── message_processor.py        # Kafka consumer + agent runner
│   │   └── metrics_collector.py        # Background metrics
│   ├── api/
│   │   └── main.py                     # FastAPI application
│   ├── database/
│   │   ├── schema.sql                  # PostgreSQL schema
│   │   └── queries.py                  # DB access functions
│   ├── tests/
│   │   ├── test_agent.py
│   │   ├── test_web_form.py
│   │   └── test_e2e.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── support-form/               # Next.js standalone form component
├── k8s/                            # Kubernetes manifests
├── specs/
│   └── customer-success-agent-spec.md
├── docker-compose.yml
└── CLAUDE.md
```

---

## Architecture Flow

```
User (Browser)
    │
    ▼
Next.js Web Support Form
    │  POST /support/submit
    ▼
FastAPI Endpoint (web_form_handler.py)
    │
    ▼
Kafka Topic: support.web_form.incoming
    │
    ▼
Kafka Consumer (message_processor.py)
    │
    ▼
OpenAI Agents SDK (customer_success_agent.py)
    │  Uses tools:
    │  - search_knowledge_base()
    │  - create_ticket()
    │  - get_customer_history()
    │  - escalate_to_human()
    │  - send_web_response()
    ▼
PostgreSQL (tickets, customers, messages, conversations)
    │
    ▼
API Response → Frontend (ticket ID + AI reply)
```

---

## Database Schema (PostgreSQL)

```sql
-- customers table
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- tickets table
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    subject VARCHAR(500),
    category VARCHAR(100),     -- 'general' | 'technical' | 'billing' | 'bug_report' | 'feedback'
    status VARCHAR(50) DEFAULT 'open',  -- 'open' | 'resolved' | 'escalated'
    priority VARCHAR(50) DEFAULT 'medium',
    channel VARCHAR(50) DEFAULT 'web_form',
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

-- messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES tickets(id),
    role VARCHAR(20),           -- 'customer' | 'agent' | 'system'
    content TEXT,
    sentiment_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES tickets(id),
    customer_id UUID REFERENCES customers(id),
    channel VARCHAR(50) DEFAULT 'web_form',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Agent Tools (OpenAI Agents SDK)

```python
@function_tool
async def search_knowledge_base(query: str) -> str:
    """Search product documentation. Returns top 3 relevant snippets."""

@function_tool
async def create_ticket(customer_id: str, subject: str, category: str, message: str) -> str:
    """Create a support ticket. Returns ticket_id."""

@function_tool
async def get_customer_history(email: str) -> str:
    """Get customer's past tickets and interactions."""

@function_tool
async def escalate_to_human(ticket_id: str, reason: str) -> str:
    """Mark ticket as escalated. Returns escalation confirmation."""

@function_tool
async def send_web_response(ticket_id: str, response: str) -> str:
    """Store AI response for web form polling. Returns status."""
```

---

## FastAPI Endpoints

```
POST   /support/submit          # Submit web form → creates ticket → Kafka
GET    /support/status/{ticket_id}  # Poll for AI response
GET    /customers/lookup        # Lookup customer by email
GET    /tickets/{ticket_id}     # Get ticket details
GET    /metrics/channels        # Metrics dashboard
GET    /health                  # Health check
```

---

## Kafka Topics

```
support.web_form.incoming     # New web form submissions
support.tickets.created       # Ticket creation events
support.responses.generated   # AI response ready
support.escalations           # Escalated tickets
support.metrics               # Metrics events
```

---

## Agent Behavior Rules (Guardrails)

- **NEVER** discuss competitor products
- **NEVER** promise features not in product-docs.md
- **ALWAYS** create a ticket before responding
- **ALWAYS** check sentiment before closing a conversation
- **ALWAYS** format response in semi-formal web style (max 300 words)
- **Escalate** when: sentiment < 0.3, pricing negotiation, refund requests, legal questions, 3+ failed resolution attempts

---

## Web Form Component (Next.js)

The form must collect:
- `name` (required)
- `email` (required, validated)
- `subject` (required)
- `category` (dropdown: General | Technical | Billing | Bug Report | Feedback)
- `message` (required, min 20 chars)

After submission:
1. Show ticket ID to user
2. Poll `/support/status/{ticket_id}` every 3 seconds
3. Display AI response when ready (max 30 second wait)

---

## Escalation Rules

| Trigger | Action |
|---------|--------|
| Sentiment score < 0.3 | Escalate immediately |
| Category = billing + refund keywords | Escalate |
| Category = legal/compliance | Escalate |
| 3 failed resolution attempts | Escalate |
| Customer explicitly requests human | Escalate |

---

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/customer_support

# OpenAI
OPENAI_API_KEY=sk-...

# Kafka (Confluent Cloud)
KAFKA_BOOTSTRAP_SERVERS=...
KAFKA_API_KEY=...
KAFKA_API_SECRET=...

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## Development Commands

```bash
# Backend
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000

# Frontend
cd frontend/support-form
npm install
npm run dev

# Docker Compose (local full stack)
docker-compose up -d

# Kubernetes (Minikube)
minikube start
kubectl apply -f k8s/
```

---

## Delivery Checklist

### Phase 1 — Core Agent (Client Demo Ready)
- [ ] PostgreSQL schema deployed (Neon production)
- [ ] OpenAI Agents SDK implementation with all 5 tools
- [ ] FastAPI backend with all endpoints
- [ ] Web Support Form (Next.js) — validation + status polling
- [ ] Kafka event streaming
- [ ] End-to-end flow working locally

### Phase 2 — Production Hardening
- [ ] Kubernetes manifests + health checks
- [ ] 99.9% uptime under load testing
- [ ] Monitoring + alerting configured
- [ ] API documentation for client handoff
- [ ] Deployment guide written

---


## Key Performance Targets

- Response time: < 3 seconds (processing)
- Uptime: > 99.9%
- Escalation rate: < 20%
- P95 latency: < 3 seconds

---

## Skills & MCP Usage Guide

This project has **11 skills** and **2 MCP servers** available in `.claude/skills/`. Always use the correct skill/MCP for each task — do not guess or write from memory.

---

### MCP Servers

#### 1. `context7` — Live Documentation
**Use for:** Getting latest, accurate docs for any library before writing code.

| When to use | Example prompt |
|-------------|----------------|
| Before writing any FastAPI code | `use context7 to get FastAPI latest docs` |
| Before using OpenAI Agents SDK | `use context7 to get openai-agents python sdk docs` |
| Before Next.js routing/form code | `use context7 to get Next.js 15 app router docs` |
| Before Kafka client code | `use context7 to get confluent-kafka-python docs` |
| Before SQLModel/PostgreSQL queries | `use context7 to get sqlmodel docs` |
| Any library you are unsure about | Always resolve library ID first, then query-docs |

**Rule:** Har naye module ya library ko use karne se pehle context7 se docs fetch karo. Training data outdated ho sakta hai.

---

#### 2. `magic` — UI Component Generation
**Use for:** Web Support Form ke UI components, icons, logos banate waqt.

| When to use | Tool to call |
|-------------|-------------|
| Support form component banana | `21st_magic_component_builder` |
| Design inspiration chahiye | `21st_magic_component_inspiration` |
| Component refine/improve karna | `21st_magic_component_refiner` |
| Company logo dhundhna | `logo_search` |

**Rule:** Jab bhi Next.js mein koi UI component scratch se banana ho — pehle magic se generate karo, phir customize karo.

---

### Skills (`.claude/skills/`)

#### Backend Skills

**`fastapi-expert`**
- Use when: FastAPI app likhna, endpoints banana, middleware, SQLModel models, dependency injection, async routes
- Specifically use for: `api/main.py`, `channels/web_form_handler.py`, `database/queries.py`
- Always combine with: context7 for latest FastAPI docs

**`building-with-openai-agents`**
- Use when: Agent definition likhna, `@function_tool` decorators, handoffs, agent runner, tracing
- Specifically use for: `agent/customer_success_agent.py`, `agent/tools.py`, `workers/message_processor.py`
- Always combine with: context7 for latest openai-agents SDK docs

---

#### Frontend Skills

**`building-nextjs-apps`**
- Use when: Next.js form component, App Router, API routes, server/client components, Turbopack config
- Specifically use for: `frontend/support-form/` — form component, status polling, submission logic
- Always combine with: context7 for Next.js 15 latest patterns

---

#### UI/UX Skills (7 sub-skills under `ui-ux-pro-max-skill`)

| Skill | Kab use karo |
|-------|-------------|
| `ui-ux-pro-max` | Overall form layout, UX flow, accessibility — use first for any UI decision |
| `ui-styling` | shadcn/ui components + Tailwind classes — form inputs, buttons, badges |
| `design-system` | Design tokens (colors, spacing, typography) — project-wide consistency ke liye |
| `design` | Logo, icons, visual assets banana |
| `brand` | Company tone, voice, messaging — context files (brand-voice.md) likhte waqt |
| `banner-design` | Hero section ya OG image banana ho to |
| `slides` | Client demo / product presentation slides banana ho to |

**Rule for UI work:** Pehle `ui-ux-pro-max` consult karo layout ke liye → phir `ui-styling` for shadcn/Tailwind → phir `magic` MCP for actual component generation.

---

### Quick Reference: Task → Tool Mapping

| Task | Skill | MCP |
|------|-------|-----|
| FastAPI endpoint likhna | `fastapi-expert` | context7 |
| OpenAI Agent + tools | `building-with-openai-agents` | context7 |
| Next.js form component | `building-nextjs-apps` | context7 + magic |
| Form UI design/styling | `ui-ux-pro-max` + `ui-styling` | magic |
| Design tokens setup | `design-system` | — |
| Brand voice / context files | `brand` | — |
| Client demo slides | `slides` | — |
| Any library docs | — | context7 |
| UI component generate | — | magic |

---

### Docs Folder Reference

The `docs/` folder contains `project-reference.md` — the full project spec. Consult it when:
- Clarifying any requirement
- Reviewing deliverables checklist
- Understanding Phase 1 → Phase 2 transition