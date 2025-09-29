# Test Suite for Enrichment Service

This test suite covers all acceptance criteria and edge cases for the enrichment service.

## Test Structure

- `test_acceptance_criteria.py` - Tests for all acceptance criteria (AC1-AC4)
- `test_models.py` - Tests for Pydantic models (Company, Job)
- `test_services.py` - Tests for EnrichmentService business logic
- `test_edge_cases.py` - Tests for edge cases and error scenarios
- `conftest.py` - Test configuration and fixtures

## Acceptance Criteria Coverage

### AC1: POST /enrich returns 202 status and job_id
- ✅ `test_ac1_post_enrich_returns_202_and_job_id`
- ✅ `test_job_id_uniqueness`

### AC2: GET /enrich/{job_id} returns 'pending' status within 15 seconds
- ✅ `test_ac2_get_enrich_status_pending_within_15_seconds`

### AC3: GET /enrich/{job_id} returns 'complete' status after 15 seconds
- ✅ `test_ac3_get_enrich_status_complete_after_15_seconds`

### AC4: GET request with non-existent UUID returns 404 error
- ✅ `test_ac4_get_enrich_status_nonexistent_job_returns_404`

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_acceptance_criteria.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_acceptance_criteria.py::TestAcceptanceCriteria::test_ac1_post_enrich_returns_202_and_job_id
```

## Test Categories

### Unit Tests
- Model validation and serialization
- Service business logic
- Error handling

### Integration Tests
- API endpoint behavior
- Dependency injection
- Background processing

### End-to-End Tests
- Complete workflow testing
- Concurrent job handling
- Status transitions

## Notes

- Tests use `asyncio.sleep(16)` to ensure background processing completes
- Mock data is generated with random company sizes (10-1000)
- All tests are isolated and can run independently
- Test fixtures provide clean state for each test
