"""
Test configuration and fixtures for the Lead Ingestion API
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def valid_lead_data():
    """Valid lead data that meets all qualification rules."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@company.com",
        "company_name": "Tech Corp",
        "company_size": 50,
        "role": "CEO",
    }


@pytest.fixture
def unqualified_lead_small_company():
    """Lead data that fails company size rule."""
    return {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@startup.com",
        "company_name": "Small Startup",
        "company_size": 5,
        "role": "CEO",
    }


@pytest.fixture
def unqualified_lead_wrong_role():
    """Lead data that fails role rule."""
    return {
        "first_name": "Bob",
        "last_name": "Manager",
        "email": "bob.manager@company.com",
        "company_name": "Big Corp",
        "company_size": 100,
        "role": "Manager",
    }


@pytest.fixture
def unqualified_lead_forbidden_email():
    """Lead data that fails email domain rule."""
    return {
        "first_name": "Alice",
        "last_name": "Developer",
        "email": "alice@gmail.com",
        "company_name": "Tech Company",
        "company_size": 25,
        "role": "CTO",
    }


@pytest.fixture
def unqualified_lead_multiple_failures():
    """Lead data that fails multiple rules."""
    return {
        "first_name": "Charlie",
        "last_name": "Intern",
        "email": "charlie@yahoo.com",
        "company_name": "Tiny Startup",
        "company_size": 3,
        "role": "Intern",
    }
