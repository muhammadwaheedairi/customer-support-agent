"""FastAPI application for Customer Support Agent."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import os
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

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Starting Customer Support Agent API...")
    try:
        # Initialize database connection pool
        await get_db_pool()
        logger.info("Database connection pool initialized")
        
        yield
        
    finally:
        # Shutdown
        logger.info("Shutting down Customer Support Agent API...")
        await close_db_pool()
        logger.info("Database connection pool closed")


# Create FastAPI application
app = FastAPI(
    title="TaskFlow Customer Support Agent API",
    description="AI-powered 24/7 customer support system for TaskFlow",
    version="1.0.0",
    lifespan=lifespan
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation

class SupportFormSubmission(BaseModel):
    """Support form submission request model."""
    name: str = Field(..., min_length=2, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    subject: str = Field(..., min_length=5, max_length=500, description="Ticket subject")
    category: str = Field(
        default="general",
        description="Ticket category",
        pattern="^(general|technical|billing|bug_report|feedback)$"
    )
    message: str = Field(..., min_length=20, max_length=5000, description="Customer message")
    priority: str = Field(
        default="medium",
        description="Priority level",
        pattern="^(low|medium|high)$"
    )


class SupportFormResponse(BaseModel):
    """Support form submission response model."""
    success: bool
    ticket_id: str
    message: str
    estimated_response_time: str = "Usually within 5 minutes"


class TicketStatusResponse(BaseModel):
    """Ticket status response model."""
    ticket_id: str
    status: str
    subject: str
    category: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    customer_email: str
    messages: List[Dict[str, Any]]


class CustomerLookupResponse(BaseModel):
    """Customer lookup response model."""
    customer_id: str
    email: str
    name: Optional[str]
    created_at: datetime
    ticket_count: int


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    database: str
    components: Dict[str, str]


class MetricsResponse(BaseModel):
    """Metrics response model."""
    time_period: str
    channels: Dict[str, Dict[str, Any]]
    total_tickets: int
    avg_response_time: Optional[float]


# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": "TaskFlow Customer Support Agent API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        # Check database connection
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
        components={
            "api": "healthy",
            "database": db_status,
            "agent": "healthy"
        }
    )


@app.post(
    "/support/submit",
    response_model=SupportFormResponse,
    tags=["Support"],
    status_code=201
)
async def submit_support_form(
    submission: SupportFormSubmission,
    background_tasks: BackgroundTasks
):
    """
    Submit a support form inquiry.
    
    This endpoint:
    1. Validates the submission
    2. Creates/updates customer record
    3. Creates a support ticket
    4. Queues the message for AI agent processing
    5. Returns confirmation with ticket ID
    """
    try:
        # Process form submission (creates customer, ticket, and queues to Kafka)
        result = await handle_form_submission(
            name=submission.name,
            email=submission.email,
            subject=submission.subject,
            category=submission.category,
            message=submission.message,
            priority=submission.priority
        )
        
        logger.info(f"Form submitted successfully: ticket_id={result['ticket_id']}")
        
        return SupportFormResponse(
            success=True,
            ticket_id=result["ticket_id"],
            message="Thank you for contacting LexDesk support! Our AI assistant is processing your request.",
            estimated_response_time="Usually within 5 minutes"
        )
    
    except Exception as e:
        logger.error(f"Form submission failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to submit support form. Please try again or contact support@taskflow.com"
        )


@app.get(
    "/support/status/{ticket_id}",
    response_model=TicketStatusResponse,
    tags=["Support"]
)
async def get_ticket_status(ticket_id: str):
    """
    Get ticket status and conversation history.
    
    Use this endpoint to check the status of a support ticket and retrieve
    the conversation messages between the customer and the AI agent.
    """
    try:
        # Get ticket details
        ticket = await get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise HTTPException(
                status_code=404,
                detail=f"Ticket {ticket_id} not found"
            )
        
        # Get messages for the ticket
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
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve ticket status"
        )


@app.get(
    "/customers/lookup",
    response_model=CustomerLookupResponse,
    tags=["Customers"]
)
async def lookup_customer(email: EmailStr):
    """
    Look up customer by email address.
    
    Returns customer information and ticket count if customer exists.
    """
    try:
        customer = await get_customer_by_email(email)
        
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Customer with email {email} not found"
            )
        
        # Get ticket count
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            ticket_count = await conn.fetchval(
                "SELECT COUNT(*) FROM tickets WHERE customer_id = $1",
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
        raise HTTPException(
            status_code=500,
            detail="Failed to lookup customer"
        )


@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketStatusResponse,
    tags=["Tickets"]
)
async def get_ticket_details(ticket_id: str):
    """
    Get detailed ticket information.
    
    Alias for /support/status/{ticket_id} for consistency.
    """
    return await get_ticket_status(ticket_id)


@app.get(
    "/metrics/channels",
    response_model=MetricsResponse,
    tags=["Metrics"]
)
async def get_channel_metrics(hours: int = 24):
    """
    Get performance metrics for support channels.
    
    Returns metrics aggregated over the specified time period (default: 24 hours).
    """
    try:
        metrics = await get_metrics_summary(hours=hours)
        
        # Calculate total tickets
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            total_tickets = await conn.fetchval(
                "SELECT COUNT(*) FROM tickets WHERE created_at > NOW() - INTERVAL '%s hours'",
                hours
            )
            
            avg_response_time = await conn.fetchval(
                """
                SELECT AVG(EXTRACT(EPOCH FROM (m.created_at - t.created_at)))
                FROM messages m
                JOIN tickets t ON m.ticket_id = t.id
                WHERE m.role = 'agent'
                  AND t.created_at > NOW() - INTERVAL '%s hours'
                """,
                hours
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
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve metrics"
        )


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
