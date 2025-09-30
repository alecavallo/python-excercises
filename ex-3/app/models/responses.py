from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.time_slot import TimeSlotResponse


class Pagination(BaseModel):
    page: int
    page_size: int
    total_count: int
    total_pages: int


class AvailableSlotsResponse(BaseModel):
    slots: list[TimeSlotResponse]
    pagination: Pagination


class TimeSlotBookingResponse(BaseModel):
    message: str
    slot_id: int
    email: EmailStr
    start_time: datetime
    end_time: datetime


class BookSlotRequest(BaseModel):
    message: str
