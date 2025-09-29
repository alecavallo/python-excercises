"""Test cases for Pydantic models."""

import pytest
from app.models.company import Company
from app.models.job import Job


class TestCompanyModel:
    """Test cases for Company model."""

    def test_company_creation(self):
        """Test creating a Company instance."""
        company = Company(domain="example.com", size=100, industry="Technology")

        assert company.domain == "example.com"
        assert company.size == 100
        assert company.industry == "Technology"

    def test_company_validation(self):
        """Test Company model validation."""
        # Valid data
        company = Company(domain="test.com", size=50, industry="Finance")
        assert company.domain == "test.com"

        # Test with different data types
        with pytest.raises(ValueError):
            Company(domain="test.com", size="invalid", industry="Finance")

    def test_company_serialization(self):
        """Test Company model serialization."""
        company = Company(domain="serialize.com", size=200, industry="Healthcare")

        data = company.model_dump()
        assert data["domain"] == "serialize.com"
        assert data["size"] == 200
        assert data["industry"] == "Healthcare"


class TestJobModel:
    """Test cases for Job model."""

    def test_job_creation_with_company(self):
        """Test creating a Job instance with Company data."""
        company = Company(domain="jobtest.com", size=150, industry="Education")

        job = Job(job_id="test-job-123", status="complete", data=company)

        assert job.job_id == "test-job-123"
        assert job.status == "complete"
        assert job.data is not None
        assert job.data.domain == "jobtest.com"

    def test_job_creation_without_company(self):
        """Test creating a Job instance without Company data."""
        job = Job(job_id="pending-job-456", status="pending", data=None)

        assert job.job_id == "pending-job-456"
        assert job.status == "pending"
        assert job.data is None

    def test_job_validation(self):
        """Test Job model validation."""
        # Valid job
        job = Job(job_id="valid-job", status="processing", data=None)
        assert job.job_id == "valid-job"

        # Test required fields
        with pytest.raises(ValueError):
            Job(status="pending")  # Missing job_id

    def test_job_serialization(self):
        """Test Job model serialization."""
        company = Company(domain="serialize-job.com", size=300, industry="Retail")

        job = Job(job_id="serialize-test", status="complete", data=company)

        data = job.model_dump()
        assert data["job_id"] == "serialize-test"
        assert data["status"] == "complete"
        assert data["data"]["domain"] == "serialize-job.com"
