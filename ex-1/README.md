# Project 1 (Revised): Lead Ingestion & Qualification API

**Ticket:** PROJ-101: Create API Endpoint for New Lead Ingestion and Basic Qualification

## Story

As a sales operator, I want to programmatically submit new leads to our system via an API. To save time, I need the system to perform an initial, automatic qualification based on a simple set of business rules so that I can focus my attention on the most promising leads first.

## Technical Requirements

### Framework
- Use FastAPI

### Endpoint
- Create a single POST `/leads` endpoint

### Input Data Model
The endpoint must accept a JSON object representing a lead. Use Pydantic for strict validation.

- `first_name`: str
- `last_name`: str
- `email`: pydantic.EmailStr (leverage Pydantic's built-in email validation)
- `company_name`: str
- `company_size`: int (must be a positive integer)
- `role`: str

### Qualification Logic
The service must internally classify the lead based on the following rules. The logic should be case-insensitive where appropriate. All rules must be met for a lead to be "Qualified".

1. **Company Size**: `company_size` must be greater than 10
2. **Decision-Maker Role**: The role (case-insensitive) must be one of the following: CEO, CTO, Founder, VP of Engineering
3. **Business Email**: The email domain (case-insensitive) must not be from a free provider. For this task, the forbidden domains are: gmail.com, yahoo.com, outlook.com

### Output Data Model
Upon successful ingestion, the API should return a 201 Created status code and a JSON response containing:

- A new `lead_id`: UUID (generated on the server)
- `status`: A string, either 'Qualified' or 'Unqualified'
- `qualification_notes`: An optional list of strings. If the status is 'Unqualified', this list should contain human-readable reasons for the failure (e.g., ["Company size of 5 is too small.", "Role 'Manager' is not a decision-maker."])
- The original lead data that was submitted

## Acceptance Criteria

- **AC1**: A POST request with a lead that meets all rules (e.g., role: 'ceo', company_size: 50) returns a 201 status, a new lead_id, and status: 'Qualified'
- **AC2**: A POST request with a lead that fails one rule (e.g., company_size: 5) returns 201, a new lead_id, status: 'Unqualified', and a qualification_notes array with a single, clear reason
- **AC3**: A POST request with a lead that fails multiple rules (e.g., company_size: 5 and email: 'test@gmail.com') returns 201, a new lead_id, status: 'Unqualified', and qualification_notes with all applicable reasons
- **AC4**: A POST request with syntactically invalid data (e.g., company_size as a string, a malformed email) is rejected with a 422 Unprocessable Entity error

## Out of Scope for this Task

- Database persistence. All operations will be in-memory
- User authentication or API keys
- Interacting with any other services