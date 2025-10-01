import os
from fastapi import FastAPI, Header, Request, Body, HTTPException, Depends
import logging
import hmac
import hashlib
from typing import Annotated


app = FastAPI(
    title="Secure Webhook Ingestion Point",
    description="Secure Webhook Ingestion Point API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

logging.basicConfig(level=logging.INFO)

ENC_SECRET = os.getenv("CRM_WEBHOOK_SECRET", "uniti-ai-is-hiring")


class RawBodyMiddleware:
    """Custom dependency to capture raw body before FastAPI parses it."""

    def __init__(self):
        self.raw_body = None

    async def __call__(self, request: Request):
        self.raw_body = await request.body()
        return self.raw_body


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "secure-webhook-ingestion-point-api"}


@app.post(
    "/webhooks/crm",
    summary="Receive CRM webhook",
    description="""
    Receives webhook events from CRM system.
    
    **Authentication**: Include HMAC-SHA256 signature in `X-CRM-Signature` header.
    The signature is calculated as: `hmac.new(secret, body_bytes, hashlib.sha256).hexdigest()`
    """,
    status_code=202,
)
async def webhook(
    body: Annotated[
        dict,
        Body(
            openapi_examples={
                "user_created": {
                    "summary": "User created event",
                    "value": {
                        "event": "user.created",
                        "user_id": "123",
                        "email": "user@example.com",
                    },
                },
                "order_placed": {
                    "summary": "Order placed event",
                    "value": {
                        "event": "order.placed",
                        "order_id": "456",
                        "total": 99.99,
                    },
                },
            }
        ),
    ],
    x_crm_signature: Annotated[str | None, Header(alias="X-CRM-Signature")] = None,
    raw_body: bytes = Depends(RawBodyMiddleware()),
):
    if not x_crm_signature:
        logging.error("X-CRM-Signature header is missing")
        raise HTTPException(status_code=400, detail="X-CRM-Signature header is missing")

    logging.debug("Received webhook: %s", body)

    # Verify HMAC signature using raw body bytes
    hmac_signature = hmac.new(ENC_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    logging.info("HMAC signature: %s", hmac_signature)

    if hmac_signature != x_crm_signature:
        logging.error(
            "Invalid signature: %s. Expected: %s", x_crm_signature, hmac_signature
        )
        raise HTTPException(
            status_code=403, detail="You are not authorized to access this resource"
        )

    return {"status": "received"}
