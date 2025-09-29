"""
Main FastAPI application entry point
Creates and configures the FastAPI app with all routes and middleware
"""

from fastapi import FastAPI


# Import routers
# from app.routers import leads

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
    return {"status": "healthy", "service": "meeting-scheduler-api"}


# Include routers
# TODO: Add routers here
