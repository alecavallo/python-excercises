"""
Production server runner for the Lead Ingestion API
Handles environment detection and production setup
"""

import os
import uvicorn
from dotenv import load_dotenv


def is_production():
    """Detect if running in production environment"""
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def setup_environment():
    """Load environment variables and prepare the environment"""
    # Load environment variables from .env file
    load_dotenv()

    # Set default environment if not specified
    if not os.getenv("ENVIRONMENT"):
        os.environ["ENVIRONMENT"] = "development"


if __name__ == "__main__":
    # Setup environment
    setup_environment()

    # Production configuration
    if is_production():
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            workers=int(os.getenv("WORKERS", 1)),
            log_level="warning",
            access_log=False,
        )
    else:
        # Development mode - use fastapi dev instead
        print("🚀 Use 'fastapi dev app/main.py' for development")
        print("🔧 For production, set ENVIRONMENT=production")
