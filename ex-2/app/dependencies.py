"""Dependency injection functions for FastAPI."""

from app.services.enrichment import EnrichmentService

# Create service instance
enrichment_service = EnrichmentService()


def get_enrichment_service() -> EnrichmentService:
    """Dependency to provide enrichment service to routers."""
    return enrichment_service
