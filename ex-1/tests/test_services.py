"""
Test cases for business logic services
"""

import pytest
from app.models.lead import Lead
from app.services.lead_qualification import LeadQualification, LeadQualificationResult


class TestLeadQualification:
    """Test class for lead qualification business logic."""

    def test_qualified_lead_returns_qualified_status(self):
        """Test that a qualified lead returns qualified status."""
        lead_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert isinstance(result, LeadQualificationResult)
        assert result.status == "Qualified"
        assert result.qualification_notes is None
        assert result.lead == lead
        assert result.lead_id is not None

    def test_small_company_returns_unqualified_with_notes(self):
        """Test that small company returns unqualified with appropriate notes."""
        lead_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@startup.com",
            "company_name": "Small Startup",
            "company_size": 5,
            "role": "CEO",
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Unqualified"
        assert result.qualification_notes is not None
        assert len(result.qualification_notes) == 1
        if result.qualification_notes is not None:
            assert "Company size is too small" in result.qualification_notes[0]

    def test_wrong_role_returns_unqualified_with_notes(self):
        """Test that wrong role returns unqualified with appropriate notes."""
        lead_data = {
            "first_name": "Bob",
            "last_name": "Manager",
            "email": "bob.manager@company.com",
            "company_name": "Big Corp",
            "company_size": 100,
            "role": "Manager",
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Unqualified"
        assert result.qualification_notes is not None
        assert len(result.qualification_notes) == 1
        assert "Role is not a decision-maker" in result.qualification_notes[0]

    def test_forbidden_email_returns_unqualified_with_notes(self):
        """Test that forbidden email domain returns unqualified with appropriate notes."""
        lead_data = {
            "first_name": "Alice",
            "last_name": "Developer",
            "email": "alice@gmail.com",
            "company_name": "Tech Company",
            "company_size": 25,
            "role": "CTO",
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Unqualified"
        assert result.qualification_notes is not None
        assert len(result.qualification_notes) == 1
        assert "Email domain is forbidden" in result.qualification_notes[0]

    def test_multiple_failures_returns_unqualified_with_all_notes(self):
        """Test that multiple failures return unqualified with all applicable notes."""
        lead_data = {
            "first_name": "Charlie",
            "last_name": "Intern",
            "email": "charlie@yahoo.com",
            "company_name": "Tiny Startup",
            "company_size": 3,
            "role": "Intern",
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Unqualified"
        assert result.qualification_notes is not None
        assert len(result.qualification_notes) >= 2

        notes = result.qualification_notes
        assert any("Company size is too small" in note for note in notes)
        assert any("Role is not a decision-maker" in note for note in notes)
        assert any("Email domain is forbidden" in note for note in notes)

    def test_case_insensitive_role_validation(self):
        """Test that role validation is case-insensitive."""
        lead_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "ceo",  # lowercase
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Qualified"

    def test_case_insensitive_role_validation_mixed_case(self):
        """Test that role validation is case-insensitive with mixed case."""
        lead_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "VP of Engineering",  # mixed case
        }

        lead = Lead(**lead_data)
        qualification = LeadQualification(lead)
        result = qualification.save()

        assert result.status == "Qualified"

    def test_qualification_notes_content(self):
        """Test the specific content of qualification notes."""
        # Test company size note
        small_company_lead = Lead(
            first_name="Test",
            last_name="User",
            email="test@company.com",
            company_name="Small Corp",
            company_size=5,
            role="CEO",
        )

        qualification = LeadQualification(small_company_lead)
        result = qualification.save()

        assert result.qualification_notes is not None
        if result.qualification_notes is not None:
            assert "Company size is too small" in result.qualification_notes[0]

        # Test role note
        wrong_role_lead = Lead(
            first_name="Test",
            last_name="User",
            email="test@company.com",
            company_name="Big Corp",
            company_size=50,
            role="Manager",
        )

        qualification = LeadQualification(wrong_role_lead)
        result = qualification.save()

        assert result.qualification_notes is not None
        if result.qualification_notes is not None:
            assert "Role is not a decision-maker" in result.qualification_notes[0]

        # Test email note
        forbidden_email_lead = Lead(
            first_name="Test",
            last_name="User",
            email="test@gmail.com",
            company_name="Big Corp",
            company_size=50,
            role="CEO",
        )

        qualification = LeadQualification(forbidden_email_lead)
        result = qualification.save()

        assert result.qualification_notes is not None
        if result.qualification_notes is not None:
            assert "Email domain is forbidden" in result.qualification_notes[0]
