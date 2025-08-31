from fastapi import APIRouter, HTTPException
from ..models.schemas import QARequest, QAResponse
from ..services.qa_service import generate_answer


router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("/ask", response_model=QAResponse)
async def ask_question(payload: QARequest):
    try:
        return await generate_answer(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

