from fastapi import APIRouter, Depends
from app.dependencies import get_enrichment_service
from app.services.enrichment import EnrichmentService
from pydantic import BaseModel

router = APIRouter()


class EnrichmentResponse(BaseModel):
    job_id: str


@router.post("/enrich", status_code=202)
async def enrich_company_data(
    company_domain: str,
    enrichment_service: EnrichmentService = Depends(get_enrichment_service),
) -> EnrichmentResponse:
    """Enrich company data for the given domain."""
    response: EnrichmentResponse = EnrichmentResponse(
        job_id=await enrichment_service.enrich_company_data(company_domain)
    )
    return response


@router.get("/enrich/{job_id}")
async def get_enrichment_status(
    job_id: str, enrichment_service: EnrichmentService = Depends(get_enrichment_service)
):
    """Get enrichment status for a job."""
    return await enrichment_service.get_enrichment_status(job_id)
