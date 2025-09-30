"""
Pytest configuration and fixtures for Meeting Scheduler API tests
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from main import app
from app.models.time_slot import TimeSlot


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def sample_time_slots():
    """Create sample time slots for testing"""
    slots = []
    base_date = datetime(2025, 9, 30)

    # Create 16 slots (8 available, 8 booked)
    for i in range(16):
        start_time = base_date.replace(hour=9 + (i // 2), minute=(i % 2) * 30)
        end_time = start_time + timedelta(minutes=30)

        slot = TimeSlot(
            id=i + 1,
            start_time=start_time,
            end_time=end_time,
            is_booked=i >= 8,  # First 8 are available, last 8 are booked
            booked_by_email=f"user{i}@example.com" if i >= 8 else None,
        )
        slots.append(slot)

    return slots


@pytest.fixture
def mock_db_session():
    """Create a mock database session"""
    session = AsyncMock()
    return session
