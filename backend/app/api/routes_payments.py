from fastapi import APIRouter, HTTPException
from ..models.schemas import CreateCheckoutRequest, CheckoutResponse, WebhookEvent
from ..services.payments_service import create_checkout, handle_webhook


router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout", response_model=CheckoutResponse)
async def payments_checkout(payload: CreateCheckoutRequest):
    try:
        return await create_checkout(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/webhook")
async def payments_webhook(event: WebhookEvent):
    try:
        await handle_webhook(event)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

