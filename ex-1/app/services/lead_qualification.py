# Business logic for lead qualification

from app.models.lead import Lead
import uuid
from pydantic import BaseModel


class LeadQualificationResult(BaseModel):
    """Result of lead qualification."""

    lead_id: uuid.UUID
    status: str
    qualification_notes: list[str] | None = None
    lead: Lead


class LeadQualification:
    """Service for qualifying leads based on company size, role, and email domain."""

    def __init__(self, lead: Lead):
        self.forbidden_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        self.decision_maker_roles = ["ceo", "cto", "founder", "vp of engineering"]
        self.min_company_size = 10
        self.lead = lead

    def _qualify_lead(self) -> bool:
        return (
            self._qualify_by_company_size()
            and self._qualify_by_role()
            and self._qualify_by_email()
        )

    def _qualify_by_company_size(self) -> bool:
        return self.lead.company_size > self.min_company_size

    def _qualify_by_role(self) -> bool:
        return self.lead.role.lower().strip() in self.decision_maker_roles

    def _qualify_by_email(self) -> bool:
        email_domain = self.lead.email.split("@")[1]
        return email_domain not in self.forbidden_domains

    def _get_qualification_notes(self) -> list[str]:
        qualification_notes = []
        if not self._qualify_by_company_size():
            qualification_notes.append("Company size is too small")
        if not self._qualify_by_role():
            qualification_notes.append("Role is not a decision-maker")
        if not self._qualify_by_email():
            qualification_notes.append("Email domain is forbidden")
        return qualification_notes

    def save(self) -> LeadQualificationResult:
        """Save qualified lead and return UUID."""
        qualification_notes = self._get_qualification_notes()
        is_qualified = self._qualify_lead()

        result = LeadQualificationResult(
            lead_id=uuid.uuid4(),
            status="Qualified" if is_qualified else "Unqualified",
            qualification_notes=qualification_notes if not is_qualified else None,
            lead=self.lead,
        )

        return result
