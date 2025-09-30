"""Seed random appointments for 2025-09-30

Revision ID: 11c98c819761
Revises: f6b223fbca55
Create Date: 2025-09-29 17:02:46.774315

"""

import random
from datetime import datetime, timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11c98c819761"
down_revision: Union[str, Sequence[str], None] = "f6b223fbca55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed random appointments for 2025-09-30."""
    # Set random seed for reproducible results
    random.seed(42)

    # Define the date and time range (EST timezone)
    target_date = datetime(2025, 9, 30)  # September 30, 2025
    start_hour = 9  # 9:00 AM
    end_hour = 17  # 5:00 PM

    # Generate all possible 30-minute slots
    available_slots = []
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:  # 30-minute intervals
            slot_start = target_date.replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )
            slot_end = slot_start + timedelta(minutes=30)
            available_slots.append((slot_start, slot_end))

    # Randomly select 10 non-overlapping slots
    selected_slots = random.sample(available_slots, 10)

    # Random email addresses
    email_domains = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "company.com",
        "example.org",
    ]
    first_names = [
        "John",
        "Jane",
        "Mike",
        "Sarah",
        "David",
        "Lisa",
        "Chris",
        "Emma",
        "Alex",
        "Maria",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
    ]

    # Generate random emails
    emails = []
    for _ in range(10):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        domain = random.choice(email_domains)
        email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        emails.append(email)

    # Insert the appointments
    time_slots_table = sa.table(
        "time_slots",
        sa.column("start_time", sa.DateTime),
        sa.column("end_time", sa.DateTime),
        sa.column("is_booked", sa.Boolean),
        sa.column("booked_by_email", sa.String),
    )

    appointments_data = []
    for i, (start_time, end_time) in enumerate(selected_slots):
        appointments_data.append(
            {
                "start_time": start_time,
                "end_time": end_time,
                "is_booked": True,
                "booked_by_email": emails[i],
            }
        )

    op.bulk_insert(time_slots_table, appointments_data)


def downgrade() -> None:
    """Remove seeded appointments."""
    # Delete appointments for 2025-09-30
    op.execute(
        """
        DELETE FROM time_slots 
        WHERE start_time >= '2025-09-30 00:00:00' 
        AND start_time < '2025-10-01 00:00:00'
    """
    )
