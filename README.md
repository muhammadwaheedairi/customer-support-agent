# TaskFlow Customer Support Agent

**AI-powered 24/7 customer support system for SaaS businesses**

Built by WaheedAI Solutions | Production-Ready Implementation

## Overview

A complete customer success agent that handles support inquiries via web form, powered by OpenAI Agents SDK, FastAPI, Next.js, PostgreSQL, and Kubernetes.

**Key Features:**
- 🤖 AI-powered responses using OpenAI Agents SDK
- 📝 Beautiful web support form with real-time validation
- 🔄 Status polling with live updates
- 📊 Performance metrics and monitoring
- 🚀 Production-ready with Kubernetes deployment
- 💰 < $1,000/year operating cost (vs $75,000/year human FTE)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 15, Tailwind CSS, TypeScript |
| Backend | FastAPI (Python 3.11), asyncpg |
| AI Agent | OpenAI Agents SDK |
| Database | PostgreSQL 16 + pgvector |
| Orchestration | Kubernetes, Docker |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- OpenAI API key
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone and navigate
cd customer-support-agent

# 2. Set environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f backend

# Access the application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

**Backend Setup:**

```bash
cd backend

# Install uv (if not installed)
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/customer_support"
export OPENAI_API_KEY="your-openai-key-here"
export ENVIRONMENT="development"
export LOG_LEVEL="INFO"

# Initialize database
psql -U postgres -d customer_support -f database/schema.sql

# Start backend
uvicorn api.main:app --reload --port 8000
```

**Frontend Setup:**

```bash
cd frontend/support-form

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_URL="http://localhost:8000"

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## Testing the System

### Manual Test

1. Open http://localhost:3000
2. Fill out the support form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Subject: "Test inquiry"
   - Category: "General"
   - Message: "How do I reset my password?"
3. Submit the form
4. Watch as the AI agent processes your request
5. Receive a response within 5 seconds

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Submit support form via API
curl -X POST http://localhost:8000/support/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Test User",
    "email": "api@example.com",
    "subject": "API Test",
    "category": "technical",
    "message": "This is a test message from the API to verify everything works correctly.",
    "priority": "medium"
  }'

# Get ticket status (replace TICKET_ID)
curl http://localhost:8000/support/status/TICKET_ID

# Get metrics
curl http://localhost:8000/metrics/channels
```

### Automated Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Project Structure

```
customer-support-agent/
├── backend/
│   ├── agent/              # OpenAI Agents SDK implementation
│   │   ├── customer_success_agent.py
│   │   ├── tools.py
│   │   ├── prompts.py
│   │   └── formatters.py
│   ├── api/                # FastAPI application
│   │   └── main.py
│   ├── channels/           # Web form handler
│   │   └── web_form_handler.py
│   ├── database/           # Database schema and queries
│   │   ├── schema.sql
│   │   └── queries.py
│   ├── workers/            # Background workers
│   │   ├── message_processor.py
│   │   └── metrics_collector.py
│   ├── tests/              # Test suite
│   └── requirements.txt
├── frontend/support-form/  # Next.js frontend
│   ├── app/
│   ├── components/
│   │   ├── support-form.tsx
│   │   └── ticket-status.tsx
│   └── package.json
├── context/                # Context files for AI agent
│   ├── company-profile.md
│   ├── product-docs.md
│   ├── sample-tickets.json
│   ├── escalation-rules.md
│   └── brand-voice.md
├── k8s/                    # Kubernetes manifests
├── specs/                  # Technical specifications
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Support
- `POST /support/submit` - Submit support form
- `GET /support/status/{ticket_id}` - Get ticket status

### Customers
- `GET /customers/lookup?email={email}` - Lookup customer

### Tickets
- `GET /tickets/{ticket_id}` - Get ticket details

### Metrics
- `GET /metrics/channels?hours={hours}` - Get performance metrics

### Health
- `GET /health` - Health check

Full API documentation: http://localhost:8000/docs

## Environment Variables

### Backend

```env
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=sk-...
ENVIRONMENT=development|production
LOG_LEVEL=INFO|DEBUG
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

### Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl create secret generic customer-support-secrets \
  --from-literal=OPENAI_API_KEY=your-key \
  --from-literal=DATABASE_URL=postgresql://... \
  -n customer-support

# Deploy
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-backend.yaml
kubectl apply -f k8s/deployment-frontend.yaml
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get pods -n customer-support
kubectl get svc -n customer-support
```

### Production Checklist

- [ ] Set strong PostgreSQL password
- [ ] Configure production CORS origins
- [ ] Enable HTTPS/TLS
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backup strategy
- [ ] Set up log aggregation
- [ ] Configure resource limits
- [ ] Enable auto-scaling
- [ ] Set up CI/CD pipeline
- [ ] Configure alerting

## How It Works

1. **User submits form** → Frontend validates and sends to API
2. **API creates ticket** → Customer and ticket records created in PostgreSQL
3. **AI agent processes** → OpenAI Agents SDK runs with 5 function tools
4. **Agent searches knowledge base** → Finds relevant documentation
5. **Agent generates response** → Professional, helpful reply (150-300 words)
6. **Response stored** → Saved to database
7. **Frontend polls** → Gets response within 3-5 seconds
8. **User sees response** → Displayed in beautiful UI

### Agent Workflow

```
1. create_ticket() - ALWAYS FIRST
2. get_customer_history() - Check for context
3. search_knowledge_base() - Find relevant docs (if needed)
4. [Decision: Resolve or Escalate]
   - If resolvable: Generate helpful response
   - If needs human: escalate_to_human()
5. send_web_response() - ALWAYS LAST
```

### Escalation Triggers

The AI automatically escalates to human support for:
- Pricing negotiations or refunds
- Legal threats or compliance requests
- High frustration (profanity, anger)
- Cannot resolve after 2 knowledge base searches
- Explicit human request

## Performance

**Measured Performance (Local Testing):**
- Form submission: < 100ms
- Agent processing: 2-4 seconds
- Total response time: < 5 seconds
- Database queries: < 50ms
- API P95 latency: < 200ms

**Production Targets:**
- Uptime: > 99.9%
- Response time: < 3 seconds
- Escalation rate: < 20%
- Concurrent users: 1000+

## Cost Analysis

**Annual Operating Cost: ~$650-1,050**

- OpenAI API: $300-500/year
- Cloud hosting: $200-300/year
- PostgreSQL: $100-200/year
- Domain/SSL: $50/year

**vs. Human FTE: $75,000/year**

**ROI: 99% cost reduction** 🎉

## Troubleshooting

### Backend won't start

```bash
# Check database connection
psql -U postgres -d customer_support -c "SELECT 1;"

# Check environment variables
env | grep DATABASE_URL
env | grep OPENAI_API_KEY

# Check logs
docker-compose logs backend
```

### Frontend won't connect to backend

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings
# Make sure CORS_ORIGINS includes http://localhost:3000

# Check browser console for errors
```

### Agent not responding

```bash
# Verify OpenAI API key is valid
# Check backend logs for errors
docker-compose logs backend | grep ERROR

# Test agent directly
cd backend
python -c "from agent.customer_success_agent import customer_success_agent; print(customer_success_agent)"
```

### Database issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
docker-compose exec postgres psql -U postgres -d customer_support -f /docker-entrypoint-initdb.d/schema.sql
```

## Development

### Adding New Features

1. Backend changes: `backend/api/main.py` or create new router
2. Agent tools: `backend/agent/tools.py`
3. Agent prompts: `backend/agent/prompts.py`
4. Frontend components: `frontend/support-form/components/`
5. Database: `backend/database/schema.sql` and `queries.py`

### Running Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests (when implemented)
cd frontend/support-form
npm test
```

### Code Quality

```bash
# Format Python code
black backend/

# Lint Python code
ruff backend/

# Type check TypeScript
cd frontend/support-form
npm run type-check
```

## Contributing

This is a production showcase project for WaheedAI Solutions. For inquiries about custom implementations, contact: support@waheedai.com

## License

MIT License - See LICENSE file for details

## Support

- Documentation: See `specs/customer-success-agent-spec.md`
- Issues: GitHub Issues
- Email: support@waheedai.com

---

**Built with ❤️ by WaheedAI Solutions**

*Demonstrating enterprise-level AI automation at a fraction of traditional costs*
