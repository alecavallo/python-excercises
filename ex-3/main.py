"""
Main FastAPI application entry point
Creates and configures the FastAPI app with all routes and middleware
"""

from fastapi import FastAPI
from app.configs.database import get_db
import logging
import sys
from sqlalchemy import text


# Import routers
from app.routers import availability

# Create FastAPI application
app = FastAPI(
    title="Simple Meeting Scheduler API",
    description="API for scheduling meetings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "healthy"

    # Check database connectivity by executing a simple query
    async for db in get_db():
        try:
            await db.execute(text("SELECT 1;"))
            db_status = "healthy"
        except (ConnectionError, TimeoutError, OSError) as e:
            db_status = "unhealthy"
            logging.error(
                "Database health check failed: unable to execute 'SELECT 1' on the database. Exception: %s",
                str(e),
                exc_info=True,
            )
        break  # Exit the async generator after first iteration

    return {"status": db_status, "service": "meeting-scheduler-api"}


# Include routers
app.include_router(availability.router)
