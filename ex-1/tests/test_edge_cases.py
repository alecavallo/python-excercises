"""
Edge case tests for the Lead Ingestion API
Tests boundary conditions, malformed data, and unusual inputs
"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.models.lead import Lead


class TestEdgeCases:
    """Test class for edge cases and boundary conditions."""

    def test_empty_request_body_returns_422(self, client):
        """Test that empty request body returns 422."""
        response = client.post("/leads", json={})
        assert response.status_code == 422

    def test_null_request_body_returns_422(self, client):
        """Test that null request body returns 422."""
        response = client.post("/leads", json=None)
        assert response.status_code == 422

    def test_malformed_json_returns_422(self, client):
        """Test that malformed JSON returns 422."""
        response = client.post("/leads", data="invalid json")
        assert response.status_code == 422

    def test_very_long_email_returns_422(self, client):
        """Test that very long email returns 422."""
        long_email = "a" * 300 + "@company.com"  # 300+ character email
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": long_email,
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_email_without_at_symbol_returns_422(self, client):
        """Test that email without @ symbol returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_email_with_multiple_at_symbols_returns_422(self, client):
        """Test that email with multiple @ symbols returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_email_with_spaces_returns_422(self, client):
        """Test that email with spaces returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test @company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_negative_company_size_returns_422(self, client):
        """Test that negative company size returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": -5,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_zero_company_size_returns_422(self, client):
        """Test that zero company size returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 0,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_float_company_size_returns_422(self, client):
        """Test that float company size returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 50.5,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_string_company_size_returns_422(self, client):
        """Test that string company size returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": "fifty",
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_boolean_company_size_returns_422(self, client):
        """Test that boolean company size returns 422."""
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": True,
            "role": "CEO",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_very_large_company_size_returns_201(self, client):
        """Test that very large company size is accepted."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Mega Corp",
            "company_size": 1000000,  # 1 million employees
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"

    def test_company_size_at_boundary_returns_201(self, client):
        """Test that company size at boundary (11) returns qualified."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Small Corp",
            "company_size": 11,  # Just above minimum
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"

    def test_company_size_at_minimum_boundary_returns_unqualified(self, client):
        """Test that company size at minimum boundary (10) returns unqualified."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Small Corp",
            "company_size": 10,  # At minimum boundary
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Unqualified"
        assert "Company size is too small" in data["qualification_notes"][0]

    def test_multiple_valid_roles_in_string_returns_unqualified(self, client):
        """Test that role containing multiple valid roles returns unqualified (exact match required)."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO and CTO",  # Contains valid role but not exact match
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Unqualified"
        assert "Role is not a decision-maker" in data["qualification_notes"][0]

    def test_role_with_extra_spaces_returns_qualified(self, client):
        """Test that role with extra spaces returns qualified (whitespace is stripped)."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "  CEO  ",  # Extra spaces - should be stripped
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"
        assert data["qualification_notes"] is None

    def test_role_with_special_characters_returns_unqualified(self, client):
        """Test that role with special characters returns unqualified."""
        valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@company.com",
            "company_name": "Tech Corp",
            "company_size": 50,
            "role": "CEO@Company",  # Special characters
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Unqualified"
        assert "Role is not a decision-maker" in data["qualification_notes"][0]

    def test_empty_string_fields_returns_422(self, client):
        """Test that empty string fields return 422."""
        invalid_data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "company_name": "",
            "company_size": 50,
            "role": "",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_whitespace_only_fields_returns_422(self, client):
        """Test that whitespace-only fields return 422."""
        invalid_data = {
            "first_name": "   ",
            "last_name": "   ",
            "email": "   ",
            "company_name": "   ",
            "company_size": 50,
            "role": "   ",
        }
        response = client.post("/leads", json=invalid_data)
        assert response.status_code == 422

    def test_very_long_strings_returns_201(self, client):
        """Test that very long strings are accepted."""
        long_string = "A" * 1000  # 1000 character string
        valid_data = {
            "first_name": long_string,
            "last_name": long_string,
            "email": "john@company.com",
            "company_name": long_string,
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201

    def test_unicode_characters_returns_201(self, client):
        """Test that unicode characters are accepted."""
        valid_data = {
            "first_name": "José",
            "last_name": "García",
            "email": "josé@empresa.com",
            "company_name": "Empresa Española",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"

    def test_special_characters_in_names_returns_201(self, client):
        """Test that special characters in names are accepted."""
        valid_data = {
            "first_name": "Jean-Pierre",
            "last_name": "O'Connor",
            "email": "jean-pierre@company.com",
            "company_name": "O'Connor & Associates",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"

    def test_numeric_strings_in_names_returns_201(self, client):
        """Test that numeric strings in names are accepted."""
        valid_data = {
            "first_name": "John123",
            "last_name": "Doe456",
            "email": "john123@company.com",
            "company_name": "Company123",
            "company_size": 50,
            "role": "CEO",
        }
        response = client.post("/leads", json=valid_data)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "Qualified"

    def test_all_forbidden_email_domains_returns_unqualified(self, client):
        """Test that all forbidden email domains return unqualified."""
        forbidden_domains = ["gmail.com", "yahoo.com", "outlook.com"]

        for domain in forbidden_domains:
            valid_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john@{domain}",
                "company_name": "Tech Corp",
                "company_size": 50,
                "role": "CEO",
            }
            response = client.post("/leads", json=valid_data)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "Unqualified"
            assert "Email domain is forbidden" in data["qualification_notes"][0]

    def test_case_insensitive_forbidden_domains_returns_unqualified(self, client):
        """Test that case-insensitive forbidden domains return unqualified."""
        case_variations = ["GMAIL.COM", "Yahoo.Com", "OutLook.CoM"]

        for domain in case_variations:
            valid_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john@{domain}",
                "company_name": "Tech Corp",
                "company_size": 50,
                "role": "CEO",
            }
            response = client.post("/leads", json=valid_data)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "Unqualified"
            assert "Email domain is forbidden" in data["qualification_notes"][0]

    def test_all_valid_roles_returns_qualified(self, client):
        """Test that all valid roles return qualified."""
        valid_roles = ["CEO", "CTO", "Founder", "VP of Engineering"]

        for role in valid_roles:
            valid_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@company.com",
                "company_name": "Tech Corp",
                "company_size": 50,
                "role": role,
            }
            response = client.post("/leads", json=valid_data)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "Qualified"

    def test_case_insensitive_valid_roles_returns_qualified(self, client):
        """Test that case-insensitive valid roles return qualified."""
        case_variations = ["ceo", "CTO", "founder", "vp of engineering"]

        for role in case_variations:
            valid_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@company.com",
                "company_name": "Tech Corp",
                "company_size": 50,
                "role": role,
            }
            response = client.post("/leads", json=valid_data)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "Qualified"

    def test_mixed_case_valid_roles_returns_qualified(self, client):
        """Test that mixed case valid roles return qualified."""
        mixed_case_roles = ["Ceo", "cTo", "FOUNDER", "Vp Of Engineering"]

        for role in mixed_case_roles:
            valid_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@company.com",
                "company_name": "Tech Corp",
                "company_size": 50,
                "role": role,
            }
            response = client.post("/leads", json=valid_data)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "Qualified"
