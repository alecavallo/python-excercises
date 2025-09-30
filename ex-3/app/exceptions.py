"""
Custom exceptions for the Meeting Scheduler API
"""


class PageSizeExceededError(Exception):
    """Raised when page size exceeds the maximum allowed value"""

    def __init__(self, max_size: int = 16):
        self.max_size = max_size
        super().__init__(f"Page size must be less than or equal to {max_size}")


class TimeSlotNotFoundError(Exception):
    """Raised when a time slot is not found"""

    def __init__(self):
        super().__init__("Time slot not found")


class TimeSlotAlreadyBookedError(Exception):
    """Raised when a time slot is already booked"""

    def __init__(self):
        super().__init__("Time slot is already booked")
