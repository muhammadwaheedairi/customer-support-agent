"""FastAPI application for LexDesk Customer Support Agent."""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import os
import httpx
import jwt
from dotenv import load_dotenv
load_dotenv()

from database.queries import (
    get_db_pool,
    close_db_pool,
    create_customer,
    get_customer_by_email,
    get_ticket_by_id,
    get_messages_by_ticket,
    get_metrics_summary,
)
from channels.web_form_handler import handle_form_submission

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Rate limiter — IP based
limiter = Limiter(key_func=get_remote_address)

# Clerk config
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY", "")
CLERK_JWKS_URL = None

def get_clerk_jwks_url():
    global CLERK_JWKS_URL
    if CLERK_JWKS_URL:
        return CLERK_JWKS_URL
    try:
        import base64
        key = CLERK_PUBLISHABLE_KEY.split("_")[2]
        padding = 4 - len(key) % 4
        if padding != 4:
            key += "=" * padding
        decoded = base64.b64decode(key).decode("utf-8").rstrip("$")
        CLERK_JWKS_URL = f"https://{decoded}/.well-known/jwks.json"
        logger.info(f"Clerk JWKS URL: {CLERK_JWKS_URL}")
        return CLERK_JWKS_URL
    except Exception as e:
        logger.error(f"Failed to decode Clerk publishable key: {e}")
        return None

_jwks_cache = {}

async def get_jwks():
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache
    jwks_url = get_clerk_jwks_url()
    if not jwks_url:
        raise HTTPException(status_code=500, detail="Clerk not configured")
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        _jwks_cache = response.json()
        return _jwks_cache

async def verify_clerk_token(token: str) -> Dict[str, Any]:
    try:
        jwks = await get_jwks()
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        public_key = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break
        if not public_key:
            raise HTTPException(status_code=401, detail="Invalid token key")
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials
    payload = await verify_clerk_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    return user_id

async def get_optional_user(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    try:
        token = auth_header.split(" ")[1]
        payload = await verify_clerk_token(token)
        return payload.get("sub")
    except Exception:
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LexDesk Customer Support Agent API...")
    try:
        await get_db_pool()
        logger.info("Database connection pool initialized")
        get_clerk_jwks_url()
        yield
    finally:
        logger.info("Shutting down LexDesk Customer Support Agent API...")
        await close_db_pool()
        logger.info("Database connection pool closed")


app = FastAPI(
    title="LexDesk Customer Support Agent API",
    description="AI-powered 24/7 customer support system for LexDesk",
    version="1.0.0",
    lifespan=lifespan
)

# Rate limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models

class SupportFormSubmission(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    subject: str = Field(..., min_length=5, max_length=500)
    category: str = Field(default="general", pattern="^(general|technical|billing|bug_report|feedback)$")
    message: str = Field(..., min_length=20, max_length=5000)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")

class SupportFormResponse(BaseModel):
    success: bool
    ticket_id: str
    message: str
    estimated_response_time: str = "Usually within 5 minutes"

class TicketStatusResponse(BaseModel):
    ticket_id: str
    status: str
    subject: str
    category: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    customer_email: str
    messages: List[Dict[str, Any]]

class TicketListItem(BaseModel):
    ticket_id: str
    status: str
    subject: str
    category: str
    created_at: datetime
    message_count: int
    has_agent_response: bool

class CustomerLookupResponse(BaseModel):
    customer_id: str
    email: str
    name: Optional[str]
    created_at: datetime
    ticket_count: int

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: str
    components: Dict[str, str]

class MetricsResponse(BaseModel):
    time_period: str
    channels: Dict[str, Dict[str, Any]]
    total_tickets: int
    avg_response_time: Optional[float]


# Endpoints

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "LexDesk Customer Support Agent API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    return HealthCheckResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        database=db_status,
        components={"api": "healthy", "database": db_status, "agent": "healthy"}
    )


@app.post("/support/submit", response_model=SupportFormResponse, tags=["Support"], status_code=201)
@limiter.limit("10/minute")
async def submit_support_form(
    request: Request,
    submission: SupportFormSubmission,
    background_tasks: BackgroundTasks,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        result = await handle_form_submission(
            name=submission.name,
            email=submission.email,
            subject=submission.subject,
            category=submission.category,
            message=submission.message,
            priority=submission.priority,
            clerk_user_id=clerk_user_id
        )
        logger.info(f"Form submitted: ticket_id={result['ticket_id']} user={clerk_user_id}")
        return SupportFormResponse(
            success=True,
            ticket_id=result["ticket_id"],
            message="Thank you for contacting LexDesk support! Our AI assistant is processing your request.",
            estimated_response_time="Usually within 5 minutes"
        )
    except Exception as e:
        logger.error(f"Form submission failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to submit support form. Please try again.")


@app.get("/support/status/{ticket_id}", response_model=TicketStatusResponse, tags=["Support"])
@limiter.limit("60/minute")
async def get_ticket_status(
    request: Request,
    ticket_id: str,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        ticket = await get_ticket_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
        if ticket.get("clerk_user_id") and ticket["clerk_user_id"] != clerk_user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        messages = await get_messages_by_ticket(ticket_id)
        return TicketStatusResponse(
            ticket_id=str(ticket["id"]),
            status=ticket["status"],
            subject=ticket["subject"],
            category=ticket["category"],
            created_at=ticket["created_at"],
            resolved_at=ticket.get("resolved_at"),
            customer_email=ticket["customer_email"],
            messages=[
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "created_at": msg["created_at"].isoformat(),
                    "sentiment_score": msg.get("sentiment_score")
                }
                for msg in messages
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get ticket status failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket status")


@app.get("/tickets/my", tags=["Tickets"])
@limiter.limit("30/minute")
async def get_my_tickets(
    request: Request,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT 
                    t.id, t.subject, t.category, t.status, 
                    t.created_at, t.resolved_at,
                    COUNT(m.id) as message_count,
                    BOOL_OR(m.role = 'agent') as has_agent_response
                FROM tickets t
                LEFT JOIN messages m ON m.ticket_id = t.id
                WHERE t.clerk_user_id = $1
                  AND t.deleted_at IS NULL
                GROUP BY t.id, t.subject, t.category, t.status, t.created_at, t.resolved_at
                ORDER BY t.created_at DESC
                """,
                clerk_user_id
            )
        tickets = [
            {
                "ticket_id": str(row["id"]),
                "subject": row["subject"],
                "category": row["category"],
                "status": row["status"],
                "created_at": row["created_at"].isoformat(),
                "resolved_at": row["resolved_at"].isoformat() if row["resolved_at"] else None,
                "message_count": row["message_count"],
                "has_agent_response": row["has_agent_response"] or False,
            }
            for row in rows
        ]
        return {"tickets": tickets, "total": len(tickets)}
    except Exception as e:
        logger.error(f"Get my tickets failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve tickets")


@app.delete("/tickets/{ticket_id}", tags=["Tickets"])
@limiter.limit("10/minute")
async def delete_ticket(
    request: Request,
    ticket_id: str,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            ticket = await conn.fetchrow(
                "SELECT id, clerk_user_id FROM tickets WHERE id = $1",
                ticket_id
            )
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            if ticket["clerk_user_id"] != clerk_user_id:
                raise HTTPException(status_code=403, detail="Access denied")
            await conn.execute(
                "UPDATE tickets SET deleted_at = NOW() WHERE id = $1",
                ticket_id
            )
        logger.info(f"Ticket {ticket_id} deleted by user {clerk_user_id}")
        return {"success": True, "message": "Ticket deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete ticket failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete ticket")


@app.get("/tickets/{ticket_id}", response_model=TicketStatusResponse, tags=["Tickets"])
@limiter.limit("60/minute")
async def get_ticket_details(
    request: Request,
    ticket_id: str,
    clerk_user_id: str = Depends(get_current_user)
):
    return await get_ticket_status(request, ticket_id, clerk_user_id)


@app.get("/customers/lookup", response_model=CustomerLookupResponse, tags=["Customers"])
@limiter.limit("20/minute")
async def lookup_customer(
    request: Request,
    email: EmailStr,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        customer = await get_customer_by_email(email)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            ticket_count = await conn.fetchval(
                "SELECT COUNT(*) FROM tickets WHERE customer_id = $1 AND deleted_at IS NULL",
                customer["id"]
            )
        return CustomerLookupResponse(
            customer_id=str(customer["id"]),
            email=customer["email"],
            name=customer.get("name"),
            created_at=customer["created_at"],
            ticket_count=ticket_count
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Customer lookup failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to lookup customer")


@app.get("/metrics/channels", response_model=MetricsResponse, tags=["Metrics"])
@limiter.limit("20/minute")
async def get_channel_metrics(
    request: Request,
    hours: int = 24,
    clerk_user_id: str = Depends(get_current_user)
):
    try:
        metrics = await get_metrics_summary(hours=hours)
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            total_tickets = await conn.fetchval(
                f"SELECT COUNT(*) FROM tickets WHERE created_at > NOW() - INTERVAL '{hours} hours' AND deleted_at IS NULL"
            )
            avg_response_time = await conn.fetchval(
                f"""
                SELECT AVG(EXTRACT(EPOCH FROM (m.created_at - t.created_at)))
                FROM messages m
                JOIN tickets t ON m.ticket_id = t.id
                WHERE m.role = 'agent'
                  AND t.created_at > NOW() - INTERVAL '{hours} hours'
                """
            )
        return MetricsResponse(
            time_period=f"Last {hours} hours",
            channels={
                "web_form": {
                    "total_tickets": total_tickets,
                    "avg_response_time_seconds": float(avg_response_time) if avg_response_time else None,
                    "metrics": metrics
                }
            },
            total_tickets=total_tickets,
            avg_response_time=float(avg_response_time) if avg_response_time else None
        )
    except Exception as e:
        logger.error(f"Get metrics failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@app.get("/help/search", tags=["Help"])
@limiter.limit("30/minute")
async def search_help(request: Request, q: str):
    try:
        from rag.retriever import retrieve
        results = await retrieve(query=q, top_k=5)
        return {
            "query": q,
            "results": [
                {
                    "title": r["title"],
                    "content": r["content"][:500],
                    "category": r["category"],
                    "relevance_score": r.get("relevance_score", r.get("score", 0))
                }
                for r in results
            ]
        }
    except Exception as e:
        logger.error(f"Help search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Search failed")


# Error handlers

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": "Not Found", "detail": "The requested resource was not found"})

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": "An unexpected error occurred."})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )