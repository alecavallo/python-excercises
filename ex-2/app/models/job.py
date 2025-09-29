"""Job model for processing company data."""

from pydantic import BaseModel
from .company import Company


class Job(BaseModel):
    """Job model representing a processing job with company data."""

    job_id: str
    status: str
    data: Company | None = None
