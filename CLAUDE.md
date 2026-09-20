# FlowSync AI Customer Support Agent

## Project Overview

AI-powered 24/7 customer support system for **FlowSync** — a conceptual project management and team collaboration SaaS platform created as a portfolio demonstration project. Built with OpenAI Agents SDK and Corrective RAG pipeline (Cohere embeddings + Qdrant vector DB + Cohere reranking). The agent demonstrates autonomous handling of customer inquiries via web form submissions with intelligent escalation logic.

**Purpose:** Portfolio project showcasing production-ready AI application architecture, full-stack development, and modern software engineering practices.

**Single-tenant architecture:** Each deployment serves one company with Clerk-based user authentication and authorization.

---

## Tech Stack

### Backend
- **Python 3.11+** with asyncio throughout
- **FastAPI 0.115+** — REST API with async/await
- **OpenAI Agents SDK** (`openai-agents` 0.0.10) — agentic function calling
- **PostgreSQL 16** with **pgvector** extension
- **Qdrant Cloud** — vector database for semantic search (1024-dim Cohere embeddings)
- **Cohere API** — embed-english-v3.0 for embeddings, rerank-english-v3.0 for reranking
- **asyncpg** — async PostgreSQL driver with connection pooling
- **Clerk** — JWT authentication (token verification only, no Clerk SDK)
- **Resend** — email notifications (missing from requirements.txt — needs manual install)
- **SlowAPI** — rate limiting per IP address

### Frontend
- **Next.js 16** (App Router) with React 19
- **TypeScript**
- **Clerk** (`@clerk/nextjs`) — full authentication with sign-in/sign-up UI
- **Tailwind CSS** + **Radix UI** — component library
- **DM Sans** font via next/font/google
- **Sonner** — toast notifications

### Infrastructure
- **Uvicorn** — ASGI server
- **pytest** + **pytest-asyncio** — testing
- **Black** + **Ruff** — code formatting/linting

---

## Project Structure

```
customer-support-agent/
├── backend/
│   ├── agent/                      # AI Agent implementation
│   │   ├── customer_success_agent.py   # Main agent (OpenAI Agents SDK Runner)
│   │   ├── prompts.py                  # System prompt with strict workflow rules
│   │   ├── tools.py                    # 6 function tools (search_kb, escalate, etc.)
│   │   └── formatters.py               # Response sanitization & formatting
│   ├── api/
│   │   └── main.py                 # FastAPI app — all endpoints, auth, rate limits
│   ├── channels/
│   │   └── web_form_handler.py     # Handles form submissions, triggers agent
│   ├── database/
│   │   ├── schema.sql              # PostgreSQL schema (missing clerk_user_id cols!)
│   │   └── queries.py              # All DB queries (asyncpg)
│   ├── rag/                        # Corrective RAG pipeline
│   │   ├── embedder.py             # Cohere embeddings (1024-dim)
│   │   ├── qdrant_store.py         # Qdrant operations (search, upsert)
│   │   ├── retriever.py            # Full pipeline: embed → search → rerank
│   │   └── seeder.py               # Script to seed knowledge base from product-docs.md
│   ├── services/
│   │   └── email_service.py        # Resend email notifications (NOT in requirements.txt)
│   ├── context/                    # Product knowledge & rules
│   │   ├── product-docs.md         # 500+ entries of FlowSync product docs
│   │   ├── escalation-rules.md     # Detailed escalation triggers & SLAs
│   │   ├── brand-voice.md          # Tone guidelines
│   │   ├── company-profile.md      # Company context
│   │   └── sample-tickets.json     # Example support tickets
│   ├── tests/                      # pytest test suite
│   │   ├── test_agent.py
│   │   ├── test_web_form.py
│   │   └── test_e2e.py
│   ├── requirements.txt            # Python dependencies (resend missing!)
│   └── .env                        # Environment variables (not in git)
│
├── frontend/support-form/          # Next.js 16 App Router
│   ├── app/
│   │   ├── page.tsx                # Landing page (Hero, Features, CTA)
│   │   ├── layout.tsx              # Root layout with ClerkProvider
│   │   ├── conversations/          # Ticket management workspace
│   │   │   ├── page.tsx            # List view with filters (All/Open/Resolved/Escalated)
│   │   │   └── [id]/page.tsx       # Single conversation thread view
│   │   ├── admin/
│   │   │   └── page.tsx            # Admin dashboard (stats, tickets, CSV export)
│   │   ├── help/
│   │   │   └── page.tsx            # Knowledge base browser
│   │   ├── sign-in/                # Clerk sign-in UI
│   │   └── sign-up/                # Clerk sign-up UI
│   ├── components/
│   │   ├── landing/                # Hero, product preview, feature grid, CTA
│   │   ├── ui/                     # Radix UI components (button, input, etc.)
│   │   ├── support-form.tsx        # Main support form component
│   │   ├── conversation-thread.tsx # Message display with role badges
│   │   ├── conversations-list.tsx  # Ticket list with status filters
│   │   ├── satisfaction-rating.tsx # 5-star rating component
│   │   └── top-nav.tsx             # Navigation with auth state
│   ├── lib/                        # Utilities
│   ├── package.json
│   ├── next.config.js              # NEXT_PUBLIC_API_URL config
│   ├── tailwind.config.ts
│   └── .env.local                  # Frontend env vars (Clerk keys)
│
├── README.md                       # Comprehensive project docs
└── design.md                       # Design decisions & architecture
```

---

## Important Gotchas & Quirks

### 1. **Schema Mismatch — clerk_user_id Missing in schema.sql**
The `schema.sql` file does **not** include `clerk_user_id` columns, but the code extensively uses them:
- `customers.clerk_user_id`
- `tickets.clerk_user_id`

**Fix before deploying:** Manually add these columns to your database:
```sql
ALTER TABLE customers ADD COLUMN clerk_user_id VARCHAR(255);
ALTER TABLE tickets ADD COLUMN clerk_user_id VARCHAR(255);
ALTER TABLE tickets ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE tickets ADD COLUMN satisfaction_rating INTEGER;
ALTER TABLE tickets ADD COLUMN satisfaction_comment TEXT;
```

### 2. **Resend Package Missing from requirements.txt**
`backend/services/email_service.py` imports `resend`, but it's not in `requirements.txt`.

**Fix:** Add `resend>=1.0.0` to requirements.txt or:
```bash
pip install resend
```

### 3. **Duplicate RAG Implementations (One Dead)**
- **Active:** Qdrant + Cohere (embedder.py, qdrant_store.py, retriever.py)
- **Dead code removed:** Old PostgreSQL pgvector full-text search was in queries.py but removed

Only Qdrant RAG is used. The `knowledge_base` table in schema.sql is **not used** by the agent — it's a leftover.

### 4. **Agent Workflow — Strict Tool Call Order**
The agent has a **hard-coded workflow** that must be followed (see `prompts.py`):

```
1. Check ticket context — if "TICKET ALREADY CREATED" → use that ticket_id, DO NOT call create_ticket
2. Call get_customer_history(customer_id)
3. (Optional) Call search_knowledge_base(query) for product questions
4. Call send_web_response(ticket_id, response)
5. Either:
   - Call resolve_ticket(ticket_id) if fully resolved
   - OR had called escalate_to_human() earlier (mutually exclusive with resolve)
```

**Never call `create_ticket` if ticket_id is already in context.** The ticket is created by `web_form_handler.py` before the agent runs.

### 5. **Escalation and Resolution are Mutually Exclusive**
If a ticket is escalated, **do not** call `resolve_ticket`. The agent is explicitly told this in prompts.py.

### 6. **Email Service Uses Hardcoded Test Email**
`email_service.py` sends all emails to `os.getenv("TEST_EMAIL", to_email)` — useful for dev, but remember to unset `TEST_EMAIL` in production.

### 7. **Rate Limiting is Per-Endpoint**
Different endpoints have different limits:
- `/support/submit` — 10 req/min
- `/health`, `/support/status/*` — 60 req/min
- `/admin/*` — 30 req/min

IP-based via SlowAPI.

### 8. **Admin Routes Require Hardcoded ADMIN_USER_ID**
Only one admin user is supported — set `ADMIN_USER_ID` env var to the Clerk user ID that should have admin access. No role-based system.

### 9. **Frontend Polls for Ticket Updates**
The frontend does **not** use WebSockets. It polls `/support/status/{ticket_id}` every few seconds for updates.

### 10. **Knowledge Base Seeding is Manual**
Run `backend/rag/seeder.py` to populate Qdrant from `context/product-docs.md`. Not automated — must be run once after setup.

---

## Commands

### Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt
pip install resend  # Missing from requirements.txt!

# Set up database (PostgreSQL)
psql -U postgres -d flowsync_support -f database/schema.sql

# Run migrations (manual — see Gotcha #1)
psql -U postgres -d flowsync_support -c "ALTER TABLE customers ADD COLUMN clerk_user_id VARCHAR(255);"
psql -U postgres -d flowsync_support -c "ALTER TABLE tickets ADD COLUMN clerk_user_id VARCHAR(255);"
psql -U postgres -d flowsync_support -c "ALTER TABLE tickets ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;"
psql -U postgres -d flowsync_support -c "ALTER TABLE tickets ADD COLUMN satisfaction_rating INTEGER;"
psql -U postgres -d flowsync_support -c "ALTER TABLE tickets ADD COLUMN satisfaction_comment TEXT;"

# Seed knowledge base into Qdrant
python -m rag.seeder

# Run development server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest
pytest -v --cov=. --cov-report=html

# Format code
black .
ruff check .
```

### Frontend

```bash
# Navigate to frontend
cd frontend/support-form

# Install dependencies
npm install

# Run development server
npm run dev
# Opens at http://localhost:3000

# Build for production
npm run build
npm run start

# Type check
npm run type-check

# Lint
npm run lint
```

---

## Environment Variables

### Backend `.env`

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/flowsync_support

# OpenAI
OPENAI_API_KEY=sk-...

# Cohere (for RAG)
COHERE_API_KEY=...

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=...

# Clerk Authentication
CLERK_PUBLISHABLE_KEY=pk_test_...  # Used to derive JWKS URL

# Admin User
ADMIN_USER_ID=user_...  # Clerk user ID for admin access

# Email (Resend)
RESEND_API_KEY=re_...
TEST_EMAIL=test@example.com  # Optional: redirect all emails here in dev

# API Config
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development  # or production
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com
```

### Frontend `.env.local`

```bash
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Clerk URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/conversations
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/conversations
```

---

## Key Files to Read First

1. **`backend/api/main.py`** — FastAPI app, all endpoints, auth logic
2. **`backend/agent/customer_success_agent.py`** — OpenAI Agents SDK Runner
3. **`backend/agent/prompts.py`** — System prompt with strict workflow
4. **`backend/agent/tools.py`** — 6 function tools the agent can call
5. **`backend/rag/retriever.py`** — Corrective RAG pipeline
6. **`backend/channels/web_form_handler.py`** — Entry point for form submissions
7. **`backend/context/escalation-rules.md`** — When to escalate to humans
8. **`frontend/support-form/app/conversations/page.tsx`** — Main UI workspace

---

## Development Workflow

1. **Start PostgreSQL** (local or Docker)
2. **Run schema.sql** to create tables
3. **Apply manual migrations** (clerk_user_id, deleted_at, etc.)
4. **Seed Qdrant** with `python -m rag.seeder`
5. **Start backend** with `uvicorn api.main:app --reload`
6. **Start frontend** with `npm run dev` in `frontend/support-form/`
7. **Sign up via Clerk** at http://localhost:3000/sign-up
8. **Copy your Clerk user ID** from Clerk Dashboard → Users
9. **Set ADMIN_USER_ID** in backend `.env` to your user ID (for admin access)
10. **Submit a test ticket** via support form
11. **Check conversation** in /conversations

---

## Testing

```bash
# Backend tests
cd backend
pytest tests/test_web_form.py -v
pytest tests/test_agent.py -v
pytest tests/test_e2e.py -v

# No frontend tests currently — add with Jest/Vitest if needed
```

---

## Deployment Notes

- **Backend:** Deploy FastAPI with Uvicorn + Gunicorn on any Python host (AWS ECS, Fly.io, Railway)
- **Frontend:** Deploy Next.js to Vercel (native support) or any Node.js host
- **Database:** Managed PostgreSQL (AWS RDS, Supabase, Neon)
- **Qdrant:** Use Qdrant Cloud (already configured)
- **Clerk:** Production keys from Clerk Dashboard
- **Resend:** Production API key from Resend Dashboard

---

## Architecture Decisions

See `design.md` for detailed architecture notes.

**Key patterns:**
- **Corrective RAG:** Embed → Vector Search (top 10) → Rerank (top 3) for high precision
- **Async-first:** All database & API calls use async/await
- **Single-tenant:** Each deployment = one company (no multi-tenancy)
- **Escalation-driven:** Agent escalates ~20% of tickets to humans
- **Stateless agent:** No conversation memory beyond database — each run is fresh

---

## Common Issues

### "Agent creates duplicate tickets"
The agent is told to check if `"TICKET ALREADY CREATED"` appears in the user message. If the prompt doesn't include this, it will call `create_ticket` again. Fix: Ensure `web_form_handler.py` passes ticket_id in context.

### "Knowledge base returns no results"
Qdrant collection is empty. Run `python -m rag.seeder` to seed from `context/product-docs.md`.

### "Email notifications not working"
1. Check `RESEND_API_KEY` is set
2. Install `resend` package (not in requirements.txt)
3. Check `TEST_EMAIL` env var — if set, all emails go there

### "Admin dashboard returns 403"
Your Clerk user ID doesn't match `ADMIN_USER_ID` env var. Get your user ID from Clerk Dashboard.

### "Frontend can't connect to backend"
Check `NEXT_PUBLIC_API_URL` in frontend `.env.local` matches backend URL.

---

## License

MIT
