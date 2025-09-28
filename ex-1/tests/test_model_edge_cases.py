"""
Edge case tests for Pydantic model validation
Tests boundary conditions and unusual data types
"""

import pytest
from pydantic import ValidationError
from app.models.lead import Lead


class TestModelEdgeCases:
    """Test class for model validation edge cases."""

    def test_empty_strings_raise_validation_error(self):
        """Test that empty strings raise ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="",
                last_name="",
                email="",
                company_name="",
                company_size=50,
                role="",
            )

    def test_whitespace_only_strings_raise_validation_error(self):
        """Test that whitespace-only strings raise ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="   ",
                last_name="   ",
                email="   ",
                company_name="   ",
                company_size=50,
                role="   ",
            )

    def test_none_values_raise_validation_error(self):
        """Test that None values raise ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name=None,
                last_name=None,
                email=None,
                company_name=None,
                company_size=50,
                role=None,
            )

    def test_boolean_values_raise_validation_error(self):
        """Test that boolean values raise ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name=True,
                last_name=False,
                email=True,
                company_name=False,
                company_size=50,
                role=True,
            )

    def test_numeric_strings_are_accepted(self):
        """Test that numeric strings are accepted."""
        lead = Lead(
            first_name="123",
            last_name="456",
            email="test@company.com",
            company_name="789",
            company_size=50,
            role="CEO",
        )
        assert lead.first_name == "123"
        assert lead.last_name == "456"
        assert lead.company_name == "789"

    def test_special_characters_are_accepted(self):
        """Test that special characters are accepted."""
        lead = Lead(
            first_name="Jean-Pierre",
            last_name="O'Connor",
            email="jean-pierre@company.com",
            company_name="O'Connor & Associates",
            company_size=50,
            role="CEO",
        )
        assert lead.first_name == "Jean-Pierre"
        assert lead.last_name == "O'Connor"
        assert lead.company_name == "O'Connor & Associates"

    def test_unicode_characters_are_accepted(self):
        """Test that unicode characters are accepted."""
        lead = Lead(
            first_name="José",
            last_name="García",
            email="josé@empresa.com",
            company_name="Empresa Española",
            company_size=50,
            role="CEO",
        )
        assert lead.first_name == "José"
        assert lead.last_name == "García"
        assert lead.company_name == "Empresa Española"

    def test_very_long_strings_are_accepted(self):
        """Test that very long strings are accepted."""
        long_string = "A" * 1000
        lead = Lead(
            first_name=long_string,
            last_name=long_string,
            email="test@company.com",
            company_name=long_string,
            company_size=50,
            role="CEO",
        )
        assert lead.first_name == long_string
        assert lead.last_name == long_string
        assert lead.company_name == long_string

    def test_negative_company_size_raises_validation_error(self):
        """Test that negative company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=-10,
                role="CEO",
            )

    def test_zero_company_size_raises_validation_error(self):
        """Test that zero company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=0,
                role="CEO",
            )

    def test_float_company_size_raises_validation_error(self):
        """Test that float company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=50.5,
                role="CEO",
            )

    def test_string_company_size_raises_validation_error(self):
        """Test that string company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size="fifty",
                role="CEO",
            )

    def test_boolean_company_size_raises_validation_error(self):
        """Test that boolean company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=True,
                role="CEO",
            )

    def test_list_company_size_raises_validation_error(self):
        """Test that list company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=[50],
                role="CEO",
            )

    def test_dict_company_size_raises_validation_error(self):
        """Test that dict company size raises ValidationError."""
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size={"size": 50},
                role="CEO",
            )

    def test_invalid_email_formats_raise_validation_error(self):
        """Test that invalid email formats raise ValidationError."""
        invalid_emails = [
            "invalid-email",
            "test@",
            "@company.com",
            "test@@company.com",
            "test @company.com",
            "test@company",
            "test@.com",
            "@.com",
            "",
            "   ",
        ]

        for email in invalid_emails:
            with pytest.raises(ValidationError):
                Lead(
                    first_name="John",
                    last_name="Doe",
                    email=email,
                    company_name="Tech Corp",
                    company_size=50,
                    role="CEO",
                )

    def test_valid_email_formats_are_accepted(self):
        """Test that valid email formats are accepted."""
        valid_emails = [
            "test@company.com",
            "user.name@company.co.uk",
            "test+tag@company.com",
            "test123@company123.com",
            "user_name@company-name.com",
            "test@subdomain.company.com",
        ]

        for email in valid_emails:
            lead = Lead(
                first_name="John",
                last_name="Doe",
                email=email,
                company_name="Tech Corp",
                company_size=50,
                role="CEO",
            )
            assert lead.email == email

    def test_boundary_company_size_values(self):
        """Test boundary company size values."""
        # Test minimum valid value
        lead = Lead(
            first_name="John",
            last_name="Doe",
            email="john@company.com",
            company_name="Tech Corp",
            company_size=1,  # Minimum positive integer
            role="CEO",
        )
        assert lead.company_size == 1

        # Test large valid value
        lead = Lead(
            first_name="John",
            last_name="Doe",
            email="john@company.com",
            company_name="Tech Corp",
            company_size=999999999,  # Very large number
            role="CEO",
        )
        assert lead.company_size == 999999999

    def test_missing_required_fields_raise_validation_error(self):
        """Test that missing required fields raise ValidationError."""
        # Missing first_name
        with pytest.raises(ValidationError):
            Lead(
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=50,
                role="CEO",
            )

        # Missing last_name
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=50,
                role="CEO",
            )

        # Missing email
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                company_name="Tech Corp",
                company_size=50,
                role="CEO",
            )

        # Missing company_name
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_size=50,
                role="CEO",
            )

        # Missing company_size
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                role="CEO",
            )

        # Missing role
        with pytest.raises(ValidationError):
            Lead(
                first_name="John",
                last_name="Doe",
                email="john@company.com",
                company_name="Tech Corp",
                company_size=50,
            )

    def test_extra_fields_are_ignored(self):
        """Test that extra fields are ignored."""
        lead = Lead(
            first_name="John",
            last_name="Doe",
            email="john@company.com",
            company_name="Tech Corp",
            company_size=50,
            role="CEO",
            extra_field="ignored",  # Extra field
            another_field=123,  # Another extra field
        )
        assert lead.first_name == "John"
        assert lead.last_name == "Doe"
        assert lead.email == "john@company.com"
        assert lead.company_name == "Tech Corp"
        assert lead.company_size == 50
        assert lead.role == "CEO"
        # Extra fields should not be accessible
        assert not hasattr(lead, "extra_field")
        assert not hasattr(lead, "another_field")
