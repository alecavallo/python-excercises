# Project 3: Simple Meeting Scheduler API

**Ticket:** PROJ-103: Implement API for Booking Available Meeting Slots

## Story

As a product manager, I want to provide qualified leads with an API to book a meeting from a sales representative's calendar. The system needs to show available times and prevent double-booking of any time slot.

## Technical Requirements

### Framework
- FastAPI

### Database
Use a local Postgres database. You will need one table: `time_slots`

- `id`: Integer (Primary Key)
- `start_time`: TIMESTAMP
- `end_time`: TIMESTAMP
- `is_booked`: BOOLEAN (default False)
- `booked_by_email`: VARCHAR (nullable)

### Data Seeding
On application startup, the service should check if the `time_slots` table is empty. If it is, it should populate it with 30-minute slots for the next business day (e.g., from 9:00 AM to 5:00 PM).

### Endpoint 1: List Available Slots
**GET** `/availability`

**Behavior:** Query the database for all time slots where `is_booked` is False

**Output:** Return a JSON array of the available time slot objects

### Endpoint 2: Book a Slot
**POST** `/book`

**Input:** A JSON object with `slot_id`: int and `email`: str

**Behavior:**
1. Find the time slot in the database by its `id`
2. If the slot does not exist, return 404 Not Found
3. If the slot exists but `is_booked` is True, return 409 Conflict (to indicate a race condition or stale data)
4. If the slot is available, update `is_booked` to True and set `booked_by_email`

**Output:** On successful booking, return 200 OK with a confirmation message

## Acceptance Criteria

- **AC1**: On first run, the database is seeded with time slots
- **AC2**: GET `/availability` returns only the slots where `is_booked` is False
- **AC3**: POST `/book` with a valid, available `slot_id` successfully updates the database record and returns 200. The booked slot no longer appears in `/availability`
- **AC4**: POST `/book` for a slot that is already booked is rejected with a 409 status
- **AC5**: POST `/book` for a `slot_id` that doesn't exist returns a 404 status

## Out of Scope for this Task

- User authentication
- Handling multiple calendars or sales reps
- Sending confirmation emails
- Advanced concurrency control (e.g., row-level locking). A simple check-then-update is sufficient