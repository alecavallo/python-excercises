"""
Test cases for Pydantic models
"""

import pytest
from pydantic import ValidationError
from app.models.lead import Lead


class TestLeadModel:
    """Test class for Lead model validation."""

    def test_valid_lead_creation(self):
        """Test creating a valid lead."""
        lead_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }

        lead = Lead(**lead_data)
        assert lead.first_name == "John"
        assert lead.last_name == "Doe"
        assert lead.email == "john.doe@company.com"
        assert lead.company_name == "Tech Corp"
        assert lead.company_size == 50
        assert lead.role == "CEO"

    def test_invalid_email_raises_validation_error(self):
        """Test that invalid email raises ValidationError."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }

        with pytest.raises(ValidationError):
            Lead(**invalid_data)

    def test_negative_company_size_raises_validation_error(self):
        """Test that negative company size raises ValidationError."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": -10,
            "role": "CEO",
        }

        with pytest.raises(ValidationError):
            Lead(**invalid_data)

    def test_zero_company_size_raises_validation_error(self):
        """Test that zero company size raises ValidationError."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 0,
            "role": "CEO",
        }

        with pytest.raises(ValidationError):
            Lead(**invalid_data)

    def test_string_company_size_raises_validation_error(self):
        """Test that string company size raises ValidationError."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": "fifty",
            "role": "CEO",
        }

        with pytest.raises(ValidationError):
            Lead(**invalid_data)

    def test_missing_required_fields_raises_validation_error(self):
        """Test that missing required fields raise ValidationError."""
        incomplete_data = {
            "first_name": "John",
            # Missing other required fields
        }

        with pytest.raises(ValidationError):
            Lead(**incomplete_data)
