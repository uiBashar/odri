import uuid
from ..models.schemas import CreateCheckoutRequest, CheckoutResponse, WebhookEvent


async def create_checkout(payload: CreateCheckoutRequest) -> CheckoutResponse:
    reference_id = str(uuid.uuid4())
    # In production, call provider SDK to create session and return redirect URL
    checkout_url = f"https://payments.example.com/{payload.provider}/checkout/{reference_id}"
    return CheckoutResponse(provider=payload.provider, checkout_url=checkout_url, reference_id=reference_id)


async def handle_webhook(event: WebhookEvent) -> None:
    # Verify signature (omitted), update subscription in DB (omitted)
    return None

