# Pydantic models for lead data validation
"""first_name: str
last_name: str
email: pydantic.EmailStr (leverage Pydantic's built-in email validation)
company_name: str
company_size: int (must be a positive integer)
role: str"""

from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator


class Lead(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_name: str
    company_size: Annotated[int, Field(gt=0)]
    role: str

    @field_validator("company_size", mode="before")
    @classmethod
    def validate_company_size(cls, v):
        if isinstance(v, bool):
            raise ValueError("company_size must be an integer, not a boolean")
        return v
