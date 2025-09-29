from fastapi import HTTPException
from app.models.company import Company
from app.models.job import Job
import uuid
import random
import asyncio


class EnrichmentService:
    """Service for handling company data enrichment."""

    def __init__(self):
        self.jobs: dict[str, Job] = {}

    async def enrich_company_data(self, company_domain: str) -> str:
        """Enrich company data for the given domain."""
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = Job(job_id=job_id, status="pending", data=None)

        # Start background processing, simulate a 15 second external API call
        asyncio.create_task(self._process_enrichment(job_id, company_domain))

        return job_id

    async def _process_enrichment(self, job_id: str, company_domain: str) -> None:
        """Background processing for enrichment."""
        headcount = random.randint(10, 1000)
        await asyncio.sleep(15)
        self.jobs[job_id].status = "complete"
        self.jobs[job_id].data = Company(
            domain=company_domain, size=headcount, industry="Technology"
        )

    async def get_enrichment_status(self, job_id: str) -> Job:
        """Get enrichment status for a job."""
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        return self.jobs[job_id]
