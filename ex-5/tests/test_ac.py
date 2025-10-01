"""
Test the acceptance criteria for the secure webhook ingestion point:

- **AC1**: A POST request to `/webhooks/crm` with a correctly calculated `X-CRM-Signature` header returns 202 Accepted
- **AC2**: A POST request with an incorrect signature returns 403 Forbidden
- **AC3**: A POST request that is missing the `X-CRM-Signature` header returns 400 Bad Request
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def test_client():
    """Create test client"""
    return TestClient(app)


class TestAcceptanceCriteria:
    """Test the acceptance criteria for the secure webhook ingestion point"""

    def test_ac1_correct_signature(self, test_client):
        """Test that a POST request with a correctly calculated `X-CRM-Signature` header returns 202 Accepted"""
        response = test_client.post(
            "/webhooks/crm",
            json={
                "event": "user.created",
                "data": {"user_id": "123", "email": "test@example.com"},
            },
            headers={
                "X-CRM-Signature": "6063ea5146f17c12c622f6f147c2a39cbe31a5a429cf9227b1818e435930a9b0"
            },
        )
        assert response.status_code == 202
        assert response.json() == {"status": "received"}

    def test_ac2_incorrect_signature(self, test_client):
        """Test that a POST request with an incorrect signature returns 403 Forbidden"""
        response = test_client.post(
            "/webhooks/crm",
            json={
                "event": "user.created",
                "data": {"user_id": "123", "email": "test@example.com"},
            },
            headers={"X-CRM-Signature": "1234567890"},
        )
        assert response.status_code == 403

    def test_ac3_missing_signature(self, test_client):
        """Test that a POST request that is missing the `X-CRM-Signature` header returns 400 Bad Request"""
        response = test_client.post(
            "/webhooks/crm",
            json={
                "event": "user.created",
                "data": {"user_id": "123", "email": "test@example.com"},
            },
        )
        assert response.status_code == 400
