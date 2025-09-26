# Project 2: Asynchronous Data Enrichment Service

**Ticket:** PROJ-102: Build Non-Blocking API for Asynchronous Lead Data Enrichment

## Story

As a backend developer, I need to enrich lead data by calling slow, third-party APIs (e.g., to find company headcount, industry, etc.). To ensure our primary services remain responsive, I need to build an asynchronous service that can kick off these long-running jobs and allow a client to check the status later without blocking.

## Technical Requirements

### Framework
- Use FastAPI and its async capabilities

### State Management
- Use a simple in-memory Python dictionary to track the state of enrichment jobs. No database is required

### Endpoint 1: Start Enrichment
**POST** `/enrich`

**Input:** A JSON object with a `company_domain`: str (e.g., "getuniti.com")

**Behavior:**
1. Generate a unique `job_id` (UUID)
2. Store the job's initial state as 'pending'
3. Start a simulated long-running task in the background. Use `await asyncio.sleep(15)` to simulate a 15-second external API call
4. Once the "task" completes, update the job's state to 'complete' and store some mock enrichment data (e.g., `{"company_size": 50, "industry": "AI Software"}`)

**Output:** Immediately return a 202 Accepted status code with the `job_id`

### Endpoint 2: Get Enrichment Status
**GET** `/enrich/{job_id}`

**Behavior:** Look up the job by its `job_id` in your in-memory store

**Output:**
- If the job is still running, return `{"job_id": job_id, "status": "pending"}`
- If the job is complete, return `{"job_id": job_id, "status": "complete", "data": {...}}`
- If the `job_id` does not exist, return a 404 Not Found error

## Acceptance Criteria

- **AC1**: A POST to `/enrich` immediately returns a 202 status and a `job_id`
- **AC2**: A GET to `/enrich/{job_id}` within 15 seconds of the POST call returns a status of 'pending'
- **AC3**: A GET to `/enrich/{job_id}` after 15 seconds returns a status of 'complete' and the mock data
- **AC4**: A GET request with a non-existent UUID returns a 404 error

## Out of Scope for this Task

- Calling any real third-party APIs
- Error handling for the background task (i.e., a 'failed' state)
- Persistence. All job states are lost if the server restarts