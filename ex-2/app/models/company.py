"""Company model for business entity data."""

from pydantic import BaseModel


class Company(BaseModel):
    """Company model representing a business entity."""

    domain: str
    size: int
    industry: str
