from fastapi import APIRouter, HTTPException
from ..models.schemas import MathSolveRequest, MathSolveResponse
from ..services.math_service import solve_expression


router = APIRouter(prefix="/math", tags=["math"])


@router.post("/solve", response_model=MathSolveResponse)
async def solve_math(payload: MathSolveRequest):
    try:
        return solve_expression(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

