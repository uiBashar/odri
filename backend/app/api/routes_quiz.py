from fastapi import APIRouter, HTTPException
from ..models.schemas import QuizRequest, QuizResponse
from ..services.quiz_service import generate_quiz


router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz_api(payload: QuizRequest):
    try:
        return await generate_quiz(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

