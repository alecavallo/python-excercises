from sqlalchemy import select, func
from app.models.time_slot import TimeSlot
from app.configs.database import get_db
from app.models.responses import AvailableSlotsResponse
from app.exceptions import (
    PageSizeExceededError,
    TimeSlotNotFoundError,
    TimeSlotAlreadyBookedError,
)
from app.models.responses import TimeSlotBookingResponse


class SlotsService:
    """Service for managing time slots operations"""

    def __init__(self):
        self.db = get_db()

    async def get_available_slots(
        self, page: int = 1, page_size: int = 10
    ) -> AvailableSlotsResponse:
        """
        Get all available time slots with pagination

        Args:
            page: Page number (1-based)
            page_size: Number of items per page

        Returns:
            Dictionary with slots data and pagination info
        """
        # Calculate offset
        offset = (page - 1) * page_size
        if page_size > 16:
            raise PageSizeExceededError()

        # Base query for available slots (is_booked = False)
        base_query = select(TimeSlot).where(TimeSlot.is_booked == False)

        # Count query for total records
        count_query = (
            select(func.count("*"))
            .select_from(TimeSlot)
            .where(TimeSlot.is_booked == False)
        )

        # Use the class attribute db
        async for db in self.db:
            # Get total count efficiently
            count_result = await db.execute(count_query)
            total_count = count_result.scalar()

            # Apply pagination to get the actual records
            paginated_query = base_query.offset(offset).limit(page_size)
            result = await db.execute(paginated_query)
            slots = result.scalars().all()
            break

        # Calculate pagination info
        total_pages = (total_count + page_size - 1) // page_size
        has_next = page < total_pages
        has_prev = page > 1

        response: AvailableSlotsResponse = {
            "slots": [
                {
                    "id": slot.id,
                    "start_time": slot.start_time.isoformat(),
                    "end_time": slot.end_time.isoformat(),
                    "is_booked": slot.is_booked,
                    "booked_by_email": slot.booked_by_email,
                }
                for slot in slots
            ],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev,
            },
        }
        return response

    async def book_slot(self, slot_id: int, email: str) -> TimeSlotBookingResponse:
        """
        Book a time slot
        """
        async for db in self.db:
            slot = await db.get(TimeSlot, slot_id)
            if not slot:
                db.rollback()
                raise TimeSlotNotFoundError()
            if slot.is_booked:
                db.rollback()
                raise TimeSlotAlreadyBookedError()
            slot.is_booked = True
            slot.booked_by_email = email
            await db.commit()
            
            return TimeSlotBookingResponse(
                message=f"Slot {slot_id} booked successfully for {email}",
                slot_id=slot.id,
                email=email,
                start_time=slot.start_time,
                end_time=slot.end_time
            )
