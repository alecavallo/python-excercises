# Project 4: Config-Driven A/B Testing Service

**Ticket:** PROJ-104: Develop Stateless A/B Testing Assignment Microservice

## Story

As a data analyst, I want a simple, reliable service that can assign a user to an experimental group (A, B, C, etc.). The assignment must be deterministic (a user always gets the same group for the same experiment) and the configuration for experiments should be easily updatable without a code deployment.

## Technical Requirements

### Framework
- FastAPI

### Configuration
On startup, the application must load its configuration from a JSON file named `experiments.json`. The structure will be:

```json
{
  "new-signup-flow": {
    "variants": ["control", "new-design"],
    "weights": [50, 50]
  },
  "pricing-model-test": {
    "variants": ["tier-a", "tier-b", "tier-c"],
    "weights": [60, 20, 20]
  }
}
```

### Assignment Logic
The assignment must be stateless and deterministic. Use a hashing algorithm (e.g., sha256 from hashlib) on a combination of the `user_id` and the `experiment_name`. Use the resulting hash to calculate a number that can be mapped to the weighted variants. This ensures the same user is always assigned the same variant for a given test.

### Endpoint
**GET** `/assign`

**Query Parameters:** `experiment_name` (string) and `user_id` (string)

**Behavior:**
1. Check if the `experiment_name` exists in the loaded configuration. If not, return 404 Not Found
2. Apply the deterministic assignment logic to select a variant based on the configured weights

**Output:** Return a JSON object like `{"user_id": "...", "experiment_name": "...", "variant": "..."}`

## Acceptance Criteria

- **AC1**: A GET request to `/assign` with a valid `experiment_name` and `user_id` consistently returns the same variant every time it is called
- **AC2**: A GET request for an `experiment_name` not present in `experiments.json` returns a 404 status
- **AC3**: The distribution of assignments for a large number of unique users should roughly approximate the weights defined in the configuration file. (This is a design goal, not a strict test for the session)

## Out of Scope for this Task

- Tracking or storing the results of assignments. The service is purely for assignment logic
- Hot-reloading the configuration file. A server restart is required to pick up changes
- Authentication