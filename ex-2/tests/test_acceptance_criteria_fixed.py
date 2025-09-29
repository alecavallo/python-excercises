"""Test cases for acceptance criteria - Fixed version."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from app.services.enrichment import EnrichmentService


class TestAcceptanceCriteria:
    """Test cases covering all acceptance criteria."""

    def test_ac1_post_enrich_returns_202_and_job_id(
        self, client: TestClient, sample_domain: str
    ):
        """
        AC1: A POST to /enrich immediately returns a 202 status and a job_id.
        """
        response = client.post("/enrich", params={"company_domain": sample_domain})

        assert response.status_code == 202  # AC1: Should return 202 status
        assert "job_id" in response.json()

        job_id = response.json()["job_id"]
        assert isinstance(job_id, str)
        assert len(job_id) > 0

    def test_ac2_get_enrich_status_pending_within_15_seconds(
        self, client: TestClient, sample_domain: str
    ):
        """
        AC2: A GET to /enrich/{job_id} within 15 seconds of the POST call returns a status of 'pending'.
        """
        # Start enrichment job
        post_response = client.post("/enrich", params={"company_domain": sample_domain})
        job_id = post_response.json()["job_id"]

        # Check status immediately (should be pending)
        get_response = client.get(f"/enrich/{job_id}")

        assert get_response.status_code == 200
        response_data = get_response.json()
        assert response_data["status"] == "pending"
        assert response_data["job_id"] == job_id
        assert response_data["data"] is None

    @pytest.mark.asyncio
    async def test_ac3_get_enrich_status_complete_after_15_seconds(
        self, sample_domain: str
    ):
        """
        AC3: A GET to /enrich/{job_id} after 15 seconds returns a status of 'complete' and the mock data.
        """
        # Test the service directly to avoid TestClient background task issues
        service = EnrichmentService()

        # Start enrichment job
        job_id = await service.enrich_company_data(sample_domain)

        # Wait for background processing to complete
        await asyncio.sleep(16)

        # Check status after processing
        job = await service.get_enrichment_status(job_id)

        assert job.status == "complete"
        assert job.job_id == job_id
        assert job.data is not None

        # Verify the company data structure
        company_data = job.data
        assert company_data.domain == sample_domain
        assert company_data.industry == "Technology"
        assert isinstance(company_data.size, int)
        assert 10 <= company_data.size <= 1000

    def test_ac4_get_enrich_status_nonexistent_job_returns_404(
        self, client: TestClient
    ):
        """
        AC4: A GET request with a non-existent UUID returns a 404 error.
        """
        fake_job_id = "00000000-0000-0000-0000-000000000000"

        response = client.get(f"/enrich/{fake_job_id}")

        assert response.status_code == 404
        assert "Job not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_multiple_concurrent_jobs(self):
        """
        Test that multiple concurrent enrichment jobs work correctly.
        """
        service = EnrichmentService()
        domains = ["example1.com", "example2.com", "example3.com"]
        job_ids = []

        # Start multiple jobs
        for domain in domains:
            job_id = await service.enrich_company_data(domain)
            job_ids.append(job_id)

        # Check all jobs are pending initially
        for job_id in job_ids:
            job = service.jobs[job_id]
            assert job.status == "pending"

        # Wait for completion
        await asyncio.sleep(16)

        # Check all jobs are complete
        for job_id in job_ids:
            job = service.jobs[job_id]
            assert job.status == "complete"
            assert job.data is not None

    def test_job_id_uniqueness(self, client: TestClient, sample_domain: str):
        """
        Test that each enrichment request generates a unique job_id.
        """
        job_ids = set()

        # Create multiple jobs
        for _ in range(5):
            response = client.post("/enrich", params={"company_domain": sample_domain})
            job_id = response.json()["job_id"]
            job_ids.add(job_id)

        # All job IDs should be unique
        assert len(job_ids) == 5

    def test_invalid_domain_parameter(self, client: TestClient):
        """
        Test behavior with invalid or missing domain parameter.
        """
        # Test with missing parameter
        response = client.post("/enrich")
        assert response.status_code == 422  # Validation error

        # Test with empty domain
        response = client.post("/enrich", params={"company_domain": ""})
        assert response.status_code == 202  # Should still work, just empty domain
