"""Test cases for edge cases and error scenarios."""

from fastapi.testclient import TestClient


class TestEdgeCases:
    """Test cases for edge cases and error scenarios."""

    def test_empty_domain_parameter(self, client: TestClient):
        """Test behavior with empty domain parameter."""
        response = client.post("/enrich", params={"company_domain": ""})

        # Should still work with empty domain
        assert response.status_code == 202
        assert "job_id" in response.json()

    def test_very_long_domain(self, client: TestClient):
        """Test behavior with very long domain name."""
        long_domain = "a" * 1000 + ".com"
        response = client.post("/enrich", params={"company_domain": long_domain})

        assert response.status_code == 202
        assert "job_id" in response.json()

    def test_special_characters_in_domain(self, client: TestClient):
        """Test behavior with special characters in domain."""
        special_domain = "test-domain_with.special+chars.com"
        response = client.post("/enrich", params={"company_domain": special_domain})

        assert response.status_code == 202
        assert "job_id" in response.json()

    def test_missing_domain_parameter(self, client: TestClient):
        """Test behavior when domain parameter is missing."""
        response = client.post("/enrich")

        # Should return validation error
        assert response.status_code == 422

    def test_invalid_job_id_format(self, client: TestClient):
        """Test behavior with invalid job ID format."""
        invalid_job_ids = [
            "not-a-uuid",
            "123",
            "invalid-format",
            "",
            "00000000-0000-0000-0000-000000000000",
        ]

        for invalid_id in invalid_job_ids:
            response = client.get(f"/enrich/{invalid_id}")
            # Should return 404 for non-existent jobs, or 405 for invalid route patterns
            assert response.status_code in [404, 405]

    def test_concurrent_requests_same_domain(self, client: TestClient):
        """Test multiple concurrent requests for the same domain."""
        domain = "concurrent-same-domain.com"
        job_ids = []

        # Make multiple requests for the same domain
        for _ in range(5):
            response = client.post("/enrich", params={"company_domain": domain})
            assert response.status_code == 202
            job_ids.append(response.json()["job_id"])

        # All job IDs should be unique
        assert len(set(job_ids)) == 5

    def test_rapid_status_checks(self, client: TestClient):
        """Test rapid status checks on the same job."""
        domain = "rapid-checks.com"

        # Start job
        response = client.post("/enrich", params={"company_domain": domain})
        job_id = response.json()["job_id"]

        # Make rapid status checks
        for _ in range(10):
            status_response = client.get(f"/enrich/{job_id}")
            assert status_response.status_code == 200
            assert status_response.json()["job_id"] == job_id

    def test_unicode_domain(self, client: TestClient):
        """Test behavior with Unicode domain names."""
        unicode_domain = "tëst-ñame.com"
        response = client.post("/enrich", params={"company_domain": unicode_domain})

        assert response.status_code == 202
        assert "job_id" in response.json()

    def test_numeric_domain(self, client: TestClient):
        """Test behavior with numeric domain."""
        numeric_domain = "123.456.789"
        response = client.post("/enrich", params={"company_domain": numeric_domain})

        assert response.status_code == 202
        assert "job_id" in response.json()

    def test_very_long_job_id_path(self, client: TestClient):
        """Test behavior with very long job ID in path."""
        long_job_id = "a" * 1000
        response = client.get(f"/enrich/{long_job_id}")

        # Should return 404 for non-existent job
        assert response.status_code == 404

    def test_health_endpoint(self, client: TestClient):
        """Test health endpoint functionality."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

    def test_invalid_http_methods(self, client: TestClient):
        """Test behavior with invalid HTTP methods."""
        # PUT method not allowed
        response = client.put("/enrich")
        assert response.status_code == 405

        # DELETE method not allowed
        response = client.delete("/enrich")
        assert response.status_code == 405

        # PATCH method not allowed
        response = client.patch("/enrich")
        assert response.status_code == 405

    def test_malformed_json_request(self, client: TestClient):
        """Test behavior with malformed JSON in request body."""
        # POST with JSON body instead of query params
        response = client.post("/enrich", json={"company_domain": "test.com"})

        # FastAPI expects query parameters, not JSON body for this endpoint
        assert response.status_code == 422
