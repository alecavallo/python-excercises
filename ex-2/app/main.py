"""
Main FastAPI application entry point
Creates and configures the FastAPI app with all routes and middleware
"""

from fastapi import FastAPI
from app.services.enrichment import EnrichmentService
from app.routers import enrichment


# Import routers
# from app.routers import leads

# Create FastAPI application
app = FastAPI(
    title="Lead Ingestion & Qualification API",
    description="API for leads data enrichment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "asynchronous-data-enrichment-service"}


# Include routers
app.include_router(enrichment.router, tags=["enrichment"])
