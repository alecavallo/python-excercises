# Project 5: Secure Webhook Ingestion Point

**Ticket:** PROJ-105: Implement Secure Webhook Endpoint with HMAC Signature Validation

## Story

As a platform engineer, I need to create a secure endpoint to receive webhooks from a critical third-party partner (e.g., a CRM). To prevent unauthorized or malicious requests, every incoming webhook must be authenticated by validating a cryptographic signature sent in the request headers.

## Technical Requirements

### Framework
- FastAPI

### Security Scheme
- The endpoint must validate an HMAC-SHA256 signature

### Shared Secret
The secret key used for hashing should be read from an environment variable named `CRM_WEBHOOK_SECRET`. For this exercise, you can use a default value of `uniti-ai-is-hiring` if the environment variable is not set.

### Endpoint
**POST** `/webhooks/crm`

**Input:** The endpoint will receive a raw JSON body and a custom header `X-CRM-Signature`. The signature is computed by the third party as `HMAC-SHA256(secret, raw_request_body)`

### Validation Logic
1. You must access the raw request body, not the parsed Pydantic model, as the signature is based on the exact byte-for-byte payload. (Hint: This may require a custom dependency or middleware in FastAPI)
2. Compute your own HMAC-SHA256 signature of the raw body using the shared secret
3. Compare your computed signature with the one received in the `X-CRM-Signature` header. This comparison must be done in a timing-safe manner (use `hmac.compare_digest`)

### Response Behavior
- If the signature is valid, log a success message to the console (e.g., "Webhook from CRM verified and received.") and return a 202 Accepted status with a simple JSON body `{"status": "received"}`
- If the signature is invalid, return a 403 Forbidden error
- If the `X-CRM-Signature` header is missing, return a 400 Bad Request error

## Acceptance Criteria

- **AC1**: A POST request to `/webhooks/crm` with a correctly calculated `X-CRM-Signature` header returns 202 Accepted
- **AC2**: A POST request with an incorrect signature returns 403 Forbidden
- **AC3**: A POST request that is missing the `X-CRM-Signature` header returns 400 Bad Request

## Out of Scope for this Task

- Parsing or acting on the content of the webhook body. The focus is purely on the security validation layer
- Database interaction
- Generating the signature (you will need to write a small client script or use a tool like Postman to test your endpoint by generating the signature yourself)