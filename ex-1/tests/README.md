# Test Suite for Lead Ingestion API

This directory contains comprehensive test cases for the Lead Ingestion & Qualification API.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                   # Pytest fixtures and configuration
├── test_acceptance_criteria.py   # Acceptance criteria tests (AC1-AC4)
├── test_models.py               # Pydantic model validation tests
├── test_services.py             # Business logic service tests
└── README.md                    # This file
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test files
```bash
pytest tests/test_acceptance_criteria.py
pytest tests/test_models.py
pytest tests/test_services.py
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage
```bash
pytest --cov=app
```

## Test Categories

### Acceptance Criteria Tests (`test_acceptance_criteria.py`)
- **AC1**: Qualified leads return 201 + Qualified status
- **AC2**: Single rule failures return 201 + Unqualified + specific notes
- **AC3**: Multiple rule failures return 201 + Unqualified + all notes
- **AC4**: Invalid data returns 422 Unprocessable Entity

### Model Tests (`test_models.py`)
- Pydantic model validation
- Email format validation
- Company size validation (positive integers)
- Required field validation

### Service Tests (`test_services.py`)
- Business logic validation
- Qualification rules testing
- Case-insensitive role validation
- Multiple failure scenarios

## Fixtures

The `conftest.py` file provides reusable test data:
- `valid_lead_data`: Meets all qualification rules
- `unqualified_lead_small_company`: Fails company size rule
- `unqualified_lead_wrong_role`: Fails role rule
- `unqualified_lead_forbidden_email`: Fails email domain rule
- `unqualified_lead_multiple_failures`: Fails multiple rules

## Test Data Examples

### Valid Lead (AC1)
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@company.com",
    "company_name": "Tech Corp",
    "company_size": 50,
    "role": "CEO"
}
```

### Invalid Data (AC4)
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "invalid-email",
    "company_name": "Tech Corp",
    "company_size": "fifty",
    "role": "CEO"
}
```

## Expected Responses

### Qualified Lead (AC1)
```json
{
    "lead_id": "uuid-string",
    "status": "Qualified",
    "qualification_notes": null,
    "lead": { ... original lead data ... }
}
```

### Unqualified Lead (AC2/AC3)
```json
{
    "lead_id": "uuid-string",
    "status": "Unqualified",
    "qualification_notes": [
        "Company size is too small",
        "Role is not a decision-maker"
    ],
    "lead": { ... original lead data ... }
}
```

### Validation Error (AC4)
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "value is not a valid email address",
            "type": "value_error.email"
        }
    ]
}
```
