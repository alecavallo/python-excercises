"""
Availability router for the Meeting Scheduler API
"""

from fastapi import APIRouter, Query, HTTPException
from app.services.slots_service import SlotsService
from app.exceptions import (
    PageSizeExceededError,
    TimeSlotNotFoundError,
    TimeSlotAlreadyBookedError,
)
import logging
from app.models.responses import BookSlotRequest

router = APIRouter(prefix="/availability", tags=["availability"])


@router.get("/")
async def get_available_slots(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    """
    Get all available time slots with pagination

    Returns:
        JSON response with available slots and pagination info
    """
    try:
        slots_service = SlotsService()
        result = await slots_service.get_available_slots(page, page_size)
        return result
    except PageSizeExceededError as e:
        logging.error("Page size exceeded: %s", e)
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Page size exceeded",
                "message": str(e),
                "max_page_size": 16,
            },
        ) from e


@router.post("/book")
async def book_slot(slot_id: int, email: str):
    """
    Book a time slot
    """
    try:
        slots_service = SlotsService()
        result = await slots_service.book_slot(slot_id, email)
        return result
    except TimeSlotAlreadyBookedError as e:
        logging.error("Time slot already booked: %s", e)
        raise HTTPException(status_code=409, detail=str(e)) from e
    except TimeSlotNotFoundError as e:
        logging.error("Time slot not found: %s", e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        logging.error("Error booking slot: %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
