"""
Test cases for acceptance criteria of the Lead Ingestion API
"""

import pytest
from fastapi.testclient import TestClient


class TestAcceptanceCriteria:
    """Test class for all acceptance criteria."""

    def test_ac1_qualified_lead_returns_201_and_qualified_status(
        self, client, valid_lead_data
    ):
        """
        AC1: A POST request with a lead that meets all rules returns 201 status,
        a new lead_id, and status: 'Qualified'
        """
        response = client.post("/leads", json=valid_lead_data)

        # Assert 201 status code
        assert response.status_code == 201

        # Assert response structure
        data = response.json()
        assert "lead_id" in data
        assert "status" in data
        assert "qualification_notes" in data
        assert "lead" in data

        # Assert qualified status
        assert data["status"] == "Qualified"
        assert data["qualification_notes"] is None

        # Assert lead_id is a valid UUID format
        assert len(data["lead_id"]) == 36  # UUID string length

        # Assert original lead data is returned
        assert data["lead"]["first_name"] == valid_lead_data["first_name"]
        assert data["lead"]["last_name"] == valid_lead_data["last_name"]
        assert data["lead"]["email"] == valid_lead_data["email"]

    def test_ac2_single_rule_failure_returns_201_and_unqualified_with_notes(
        self, client, unqualified_lead_small_company
    ):
        """
        AC2: A POST request with a lead that fails one rule returns 201,
        a new lead_id, status: 'Unqualified', and qualification_notes with a single reason
        """
        response = client.post("/leads", json=unqualified_lead_small_company)

        # Assert 201 status code
        assert response.status_code == 201

        # Assert response structure
        data = response.json()
        assert "lead_id" in data
        assert "status" in data
        assert "qualification_notes" in data

        # Assert unqualified status
        assert data["status"] == "Unqualified"
        assert data["qualification_notes"] is not None
        assert len(data["qualification_notes"]) == 1
        assert "Company size is too small" in data["qualification_notes"][0]

    def test_ac2_wrong_role_returns_unqualified_with_role_notes(
        self, client, unqualified_lead_wrong_role
    ):
        """Test AC2 with wrong role."""
        response = client.post("/leads", json=unqualified_lead_wrong_role)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Unqualified"
        assert "Role is not a decision-maker" in data["qualification_notes"][0]

    def test_ac2_forbidden_email_returns_unqualified_with_email_notes(
        self, client, unqualified_lead_forbidden_email
    ):
        """Test AC2 with forbidden email domain."""
        response = client.post("/leads", json=unqualified_lead_forbidden_email)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Unqualified"
        assert "Email domain is forbidden" in data["qualification_notes"][0]

    def test_ac3_multiple_rule_failures_returns_201_and_unqualified_with_all_notes(
        self, client, unqualified_lead_multiple_failures
    ):
        """
        AC3: A POST request with a lead that fails multiple rules returns 201,
        a new lead_id, status: 'Unqualified', and qualification_notes with all applicable reasons
        """
        response = client.post("/leads", json=unqualified_lead_multiple_failures)

        # Assert 201 status code
        assert response.status_code == 201

        # Assert response structure
        data = response.json()
        assert "lead_id" in data
        assert "status" in data
        assert "qualification_notes" in data

        # Assert unqualified status
        assert data["status"] == "Unqualified"
        assert data["qualification_notes"] is not None
        assert len(data["qualification_notes"]) >= 2  # Multiple failures

        # Assert all expected failure reasons are present
        notes = data["qualification_notes"]
        assert any("Company size is too small" in note for note in notes)
        assert any("Role is not a decision-maker" in note for note in notes)
        assert any("Email domain is forbidden" in note for note in notes)

    def test_ac4_invalid_company_size_string_returns_422(self, client):
        """Test AC4 with invalid company_size as string."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": "fifty",  # Invalid: string instead of int
            "role": "CEO",
        }

        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_ac4_invalid_email_format_returns_422(self, client):
        """Test AC4 with malformed email."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format",  # Invalid email
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }

        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_ac4_negative_company_size_returns_422(self, client):
        """Test AC4 with negative company size."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": -10,  # Invalid: negative number
            "role": "CEO",
        }

        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_ac4_missing_required_fields_returns_422(self, client):
        """Test AC4 with missing required fields."""
        invalid_data = {
            "first_name": "John",
            # Missing last_name, email, company_name, company_size, role
        }

        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422
