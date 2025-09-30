"""
TimeSlot model for the Meeting Scheduler API
"""

from sqlalchemy import Column, Integer, DateTime, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.configs.database import Base


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    booked_by_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


# Pydantic models for API validation
class TimeSlotBase(BaseModel):
    """Base Pydantic model for TimeSlot"""

    start_time: datetime
    end_time: datetime
    is_booked: bool = False
    booked_by_email: Optional[str] = None


class TimeSlotCreate(TimeSlotBase):
    """Pydantic model for creating a TimeSlot"""

    pass


class TimeSlotUpdate(BaseModel):
    """Pydantic model for updating a TimeSlot"""

    is_booked: Optional[bool] = None
    booked_by_email: Optional[str] = None


class TimeSlotResponse(TimeSlotBase):
    """Pydantic model for TimeSlot API responses"""

    id: int

    class Config:
        from_attributes = True


class TimeSlotBookingRequest(BaseModel):
    """Pydantic model for booking a time slot"""

    slot_id: int = Field(..., description="ID of the time slot to book")
    email: str = Field(..., description="Email address of the person booking")


class TimeSlotBookingResponse(BaseModel):
    """Pydantic model for booking response"""

    message: str
    slot_id: int
    email: str
    start_time: datetime
    end_time: datetime
