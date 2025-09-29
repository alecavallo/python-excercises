"""Test cases for enrichment service."""

import pytest
import asyncio
from unittest.mock import patch
from app.services.enrichment import EnrichmentService
from app.models.company import Company
from app.models.job import Job
from fastapi import HTTPException


class TestEnrichmentService:
    """Test cases for EnrichmentService."""

    @pytest.fixture
    def service(self):
        """Create EnrichmentService instance for testing."""
        return EnrichmentService()

    def test_service_initialization(self, service: EnrichmentService):
        """Test service initialization."""
        assert isinstance(service.jobs, dict)
        assert len(service.jobs) == 0

    @pytest.mark.asyncio
    async def test_enrich_company_data_returns_job_id(self, service: EnrichmentService):
        """Test that enrich_company_data returns a job_id immediately."""
        domain = "test.com"

        job_id = await service.enrich_company_data(domain)

        assert isinstance(job_id, str)
        assert len(job_id) > 0
        assert job_id in service.jobs

    @pytest.mark.asyncio
    async def test_enrich_company_data_creates_pending_job(
        self, service: EnrichmentService
    ):
        """Test that enrich_company_data creates a pending job."""
        domain = "test.com"

        job_id = await service.enrich_company_data(domain)
        job = service.jobs[job_id]

        assert job.job_id == job_id
        assert job.status == "pending"
        assert job.data is None

    @pytest.mark.asyncio
    async def test_background_processing_completes_job(
        self, service: EnrichmentService
    ):
        """Test that background processing completes the job."""
        domain = "background-test.com"

        # Start enrichment
        job_id = await service.enrich_company_data(domain)

        # Wait for background processing to complete
        await asyncio.sleep(16)

        # Check job is completed
        job = service.jobs[job_id]
        assert job.status == "complete"
        assert job.data is not None
        assert isinstance(job.data, Company)
        assert job.data.domain == domain
        assert job.data.industry == "Technology"
        assert 10 <= job.data.size <= 1000

    @pytest.mark.asyncio
    async def test_get_enrichment_status_existing_job(self, service: EnrichmentService):
        """Test getting status for an existing job."""
        domain = "status-test.com"

        job_id = await service.enrich_company_data(domain)
        job = await service.get_enrichment_status(job_id)

        assert job.job_id == job_id
        assert job.status == "pending"

    @pytest.mark.asyncio
    async def test_get_enrichment_status_nonexistent_job(
        self, service: EnrichmentService
    ):
        """Test getting status for a non-existent job raises 404."""
        fake_job_id = "nonexistent-job-id"

        with pytest.raises(HTTPException) as exc_info:
            await service.get_enrichment_status(fake_job_id)

        assert exc_info.value.status_code == 404
        assert "Job not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_multiple_concurrent_jobs(self, service: EnrichmentService):
        """Test handling multiple concurrent jobs."""
        domains = ["concurrent1.com", "concurrent2.com", "concurrent3.com"]
        job_ids = []

        # Start multiple jobs
        for domain in domains:
            job_id = await service.enrich_company_data(domain)
            job_ids.append(job_id)

        # All jobs should be pending initially
        for job_id in job_ids:
            job = service.jobs[job_id]
            assert job.status == "pending"

        # Wait for completion
        await asyncio.sleep(16)

        # All jobs should be complete
        for job_id in job_ids:
            job = service.jobs[job_id]
            assert job.status == "complete"
            assert job.data is not None

    @pytest.mark.asyncio
    async def test_job_id_uniqueness(self, service: EnrichmentService):
        """Test that each enrichment request generates a unique job_id."""
        job_ids = set()

        # Create multiple jobs
        for _ in range(10):
            job_id = await service.enrich_company_data("uniqueness-test.com")
            job_ids.add(job_id)

        # All job IDs should be unique
        assert len(job_ids) == 10

    @pytest.mark.asyncio
    async def test_company_data_randomization(self, service: EnrichmentService):
        """Test that company data is randomized (size varies)."""
        domain = "randomization-test.com"

        job_id = await service.enrich_company_data(domain)
        await asyncio.sleep(16)

        job = service.jobs[job_id]
        assert job.status == "complete"
        assert job.data is not None

        # Size should be within expected range
        assert 10 <= job.data.size <= 1000
        assert job.data.industry == "Technology"
        assert job.data.domain == domain

    @pytest.mark.asyncio
    async def test_service_persistence_across_calls(self, service: EnrichmentService):
        """Test that service maintains job state across multiple calls."""
        domain = "persistence-test.com"

        # First call
        job_id1 = await service.enrich_company_data(domain)
        assert len(service.jobs) == 1

        # Second call
        job_id2 = await service.enrich_company_data(domain)
        assert len(service.jobs) == 2
        assert job_id1 != job_id2

        # Both jobs should exist
        assert job_id1 in service.jobs
        assert job_id2 in service.jobs
