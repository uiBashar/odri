from ..models.schemas import QuizRequest, QuizResponse, MCQ, ShortQuestion
from ..core.config import settings


async def generate_quiz(payload: QuizRequest) -> QuizResponse:
    # Minimal deterministic mock; replace with LLM prompt later
    mcqs = [
        MCQ(
            question=f"Sample MCQ {i+1} ({payload.subject} Grade {payload.grade})",
            options=["A", "B", "C", "D"],
            answer_index=0,
            explanation=("ব্যাখ্যা" if payload.preferred_language == "bn" else "Explanation"),
        )
        for i in range(payload.num_mcq)
    ]
    shorts = [
        ShortQuestion(
            question=f"Short Q{i+1} ({payload.subject} Grade {payload.grade})",
            answer=None,
        )
        for i in range(payload.num_short)
    ]
    return QuizResponse(subject=payload.subject, grade=payload.grade, mcqs=mcqs, shorts=shorts)

