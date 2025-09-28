# API routes for lead management
from fastapi import APIRouter, HTTPException
from app.models.lead import Lead
from app.services.lead_qualification import LeadQualification

router = APIRouter()


@router.post("/leads", status_code=201)
async def create_lead(lead: Lead):
    """Create a new lead and return the qualification result."""
    try:
        qualification_service = LeadQualification(lead)
        result = qualification_service.save()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e
