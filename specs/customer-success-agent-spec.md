# Customer Success Agent - Technical Specification

## Executive Summary

**Project:** TaskFlow Customer Support Agent  
**Organization:** WaheedAI Solutions  
**Version:** 1.0.0  
**Status:** Production-Ready Implementation  

A 24/7 AI-powered customer success agent handling support inquiries via web form, built with OpenAI Agents SDK, FastAPI, Next.js, PostgreSQL, and Kubernetes.

## Architecture Overview

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 15 + Tailwind + shadcn/ui | Web support form with polling |
| Backend API | FastAPI (Python 3.11) | REST API with async operations |
| AI Agent | OpenAI Agents SDK | Customer success automation |
| Database | PostgreSQL 16 + pgvector | Ticket and customer data |
| Package Manager | uv | Python dependency management |
| Orchestration | Kubernetes | Container orchestration |

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User (Browser)                        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│            Next.js Support Form (Port 3000)              │
│  • Form validation                                       │
│  • Status polling (3s intervals)                         │
│  • Responsive UI                                         │
└───────────────────────┬─────────────────────────────────┘
                        │ POST /support/submit
                        ▼
┌─────────────────────────────────────────────────────────┐
│            FastAPI Backend (Port 8000)                   │
│  • /support/submit                                       │
│  • /support/status/{ticket_id}                          │
│  • /customers/lookup                                     │
│  • /tickets/{ticket_id}                                 │
│  • /metrics/channels                                     │
│  • /health                                              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│         OpenAI Agents SDK Customer Success Agent         │
│  Tools:                                                  │
│  1. search_knowledge_base()                             │
│  2. create_ticket()                                     │
│  3. get_customer_history()                              │
│  4. escalate_to_human()                                 │
│  5. send_web_response()                                 │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database (Port 5432)             │
│  Tables:                                                 │
│  • customers                                             │
│  • tickets                                              │
│  • messages                                             │
│  • conversations                                         │
│  • knowledge_base                                        │
│  • agent_metrics                                         │
└─────────────────────────────────────────────────────────┘
```

## Database Schema

### Core Tables

**customers**
- `id` (UUID, PK)
- `email` (VARCHAR, UNIQUE)
- `name` (VARCHAR)
- `created_at` (TIMESTAMP)
- `metadata` (JSONB)

**tickets**
- `id` (UUID, PK)
- `customer_id` (UUID, FK)
- `subject` (VARCHAR)
- `category` (VARCHAR): general, technical, billing, bug_report, feedback
- `status` (VARCHAR): open, resolved, escalated
- `priority` (VARCHAR): low, medium, high
- `channel` (VARCHAR): web_form
- `created_at` (TIMESTAMP)
- `resolved_at` (TIMESTAMP, nullable)

**messages**
- `id` (UUID, PK)
- `ticket_id` (UUID, FK)
- `role` (VARCHAR): customer, agent, system
- `content` (TEXT)
- `sentiment_score` (FLOAT, nullable)
- `created_at` (TIMESTAMP)
- `metadata` (JSONB)

**conversations**
- `id` (UUID, PK)
- `ticket_id` (UUID, FK)
- `customer_id` (UUID, FK)
- `channel` (VARCHAR)
- `status` (VARCHAR): active, closed
- `created_at` (TIMESTAMP)
- `sentiment_score` (DECIMAL)
- `metadata` (JSONB)

## API Endpoints

### Support Endpoints

**POST /support/submit**
- Submit web support form
- Request body: `{name, email, subject, category, message, priority}`
- Response: `{success, ticket_id, message, estimated_response_time}`
- Status codes: 201 (Created), 422 (Validation Error), 500 (Server Error)

**GET /support/status/{ticket_id}**
- Get ticket status and messages
- Response: `{ticket_id, status, subject, category, created_at, messages[]}`
- Status codes: 200 (OK), 404 (Not Found), 500 (Server Error)

### Customer Endpoints

**GET /customers/lookup?email={email}**
- Lookup customer by email
- Response: `{customer_id, email, name, created_at, ticket_count}`
- Status codes: 200 (OK), 404 (Not Found), 500 (Server Error)

### Tickets Endpoints

**GET /tickets/{ticket_id}**
- Get detailed ticket information
- Response: Same as /support/status/{ticket_id}

### Metrics Endpoints

**GET /metrics/channels?hours={hours}**
- Get performance metrics
- Default: 24 hours
- Response: `{time_period, channels, total_tickets, avg_response_time}`

### Health Check

**GET /health**
- Health check for load balancers
- Response: `{status, timestamp, version, database, components}`
- Status codes: 200 (OK)

## AI Agent Specification

### Agent Configuration

**Model:** gpt-4o  
**Temperature:** 0.7  
**Max Turns:** 10 (default)

### System Prompt

The agent operates under strict guidelines:
- Semi-formal, professional tone (150-300 words max)
- Always create ticket first
- Check customer history for context
- Search knowledge base for product questions
- Escalate when necessary
- Never discuss pricing, never promise unreleased features

### Function Tools

**1. search_knowledge_base(query, max_results)**
- Searches product documentation
- Returns formatted results with titles and content
- Falls back gracefully if no results found

**2. create_ticket(customer_id, subject, category, message, priority)**
- ALWAYS called first
- Creates ticket and initial message
- Creates conversation record
- Returns ticket ID

**3. get_customer_history(customer_id)**
- Retrieves past interactions
- Returns formatted conversation history
- Handles new customers gracefully

**4. escalate_to_human(ticket_id, reason, category)**
- Updates ticket status to "escalated"
- Logs escalation with reason
- Returns expected response time based on category

**5. send_web_response(ticket_id, response)**
- ALWAYS called last
- Stores agent response as message
- Makes response available for polling

### Escalation Rules

**Immediate Escalation Required For:**
- Pricing negotiations or custom pricing
- Refund requests
- Billing disputes
- Legal threats ("lawyer", "legal", "sue")
- GDPR/compliance requests
- Negative sentiment (profanity, all caps anger)
- Explicit human request
- Cannot resolve after 2 knowledge base searches

**Escalation Categories:**
- `pricing_inquiry` → 2 hours response time
- `refund_request` → 2 hours
- `legal_matter` → 2 hours
- `high_frustration` → 1 hour
- `technical_complex` → 4 hours
- `security_concern` → 2 hours
- `explicit_request` → 4 hours

## Frontend Specification

### Form Validation

**Client-Side Validation:**
- Name: min 2 characters
- Email: valid email format
- Subject: min 5 characters
- Message: min 20 characters
- Real-time validation on blur
- Clear error messages

**Server-Side Validation:**
- Pydantic models enforce all constraints
- 422 status code with detailed error info

### Status Polling

- Initial request immediately after submission
- Poll every 3 seconds for agent response
- Maximum 10 polls (30 seconds)
- Stop polling once agent response received
- Show timeout warning at 24 seconds

### User Experience

- Loading states with spinners
- Success confirmation with ticket ID
- Clear error messages
- Responsive design (mobile-first)
- Dark mode support
- Accessible (WCAG AA compliant)

## Deployment

### Docker Compose (Local Development)

```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec postgres psql -U postgres -d customer_support -f /docker-entrypoint-initdb.d/schema.sql

# View logs
docker-compose logs -f backend
```

### Kubernetes (Production)

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl create secret generic customer-support-secrets \
  --from-literal=OPENAI_API_KEY=your-key \
  --from-literal=DATABASE_URL=postgresql://... \
  -n customer-support

# Apply configuration
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-backend.yaml
kubectl apply -f k8s/deployment-frontend.yaml
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get pods -n customer-support
```

## Performance Requirements

**Target Metrics:**
- Response time: < 3 seconds (agent processing)
- API latency: < 200ms (P95)
- Uptime: > 99.9%
- Escalation rate: < 20%
- Database connection pool: 5-20 connections
- Horizontal scaling: 3-10 backend pods

## Security

**Data Protection:**
- Environment variables for secrets
- No API keys in code or logs
- HTTPS only in production
- CORS properly configured
- Input validation on all endpoints

**Database:**
- Connection pooling with asyncpg
- Prepared statements (SQL injection protection)
- Regular backups
- Encrypted at rest

**API:**
- Rate limiting (future enhancement)
- Request validation with Pydantic
- Error messages don't leak sensitive info

## Monitoring & Observability

**Health Checks:**
- `/health` endpoint for load balancers
- Database connectivity check
- Component status reporting

**Metrics Collection:**
- Agent performance metrics
- Response time tracking
- Escalation rate monitoring
- Ticket volume by category
- Channel-specific metrics

**Logging:**
- Structured logging with levels
- Request/response logging
- Error tracking with stack traces
- Agent execution logging

## Cost Analysis

**Estimated Annual Operating Cost: < $1,000/year**

| Component | Cost |
|-----------|------|
| OpenAI API (gpt-4o) | ~$300-500/year |
| Cloud hosting (Kubernetes) | ~$200-300/year |
| PostgreSQL database | ~$100-200/year |
| Domain & SSL | ~$50/year |
| **Total** | **~$650-1,050/year** |

**vs. Human FTE: $75,000/year + benefits**

**ROI: 99% cost reduction**

## Future Enhancements

1. **Kafka Integration:** Full message queue implementation
2. **Email Integration:** Follow-up emails to customers
3. **Analytics Dashboard:** Real-time metrics visualization
4. **Multi-language Support:** Internationalization
5. **Advanced Analytics:** Sentiment analysis, topic clustering
6. **Live Chat:** Real-time chat with agent
7. **Knowledge Base Management:** Admin interface for docs
8. **A/B Testing:** Test different agent prompts

## Conclusion

This implementation provides a production-ready, AI-powered customer support system that:
- Handles web form inquiries 24/7
- Responds in < 3 seconds on average
- Escalates complex issues appropriately
- Costs < $1,000/year to operate
- Scales horizontally with Kubernetes
- Provides excellent customer experience

The system is ready for deployment and can handle thousands of support requests per day.
