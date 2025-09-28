"""
Main FastAPI application entry point
Creates and configures the FastAPI app with all routes and middleware
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import leads


# Import routers
# from app.routers import leads

# Create FastAPI application
app = FastAPI(
    title="Lead Ingestion & Qualification API",
    description="API for submitting and qualifying sales leads",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
""" app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, tags=["leads"]) """


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "lead-ingestion-api"}


# Include routers
app.include_router(leads.router, tags=["leads"])
