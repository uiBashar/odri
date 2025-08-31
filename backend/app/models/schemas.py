from typing import List, Optional, Literal
from pydantic import BaseModel, Field


Language = Literal["bn", "en"]


class QARequest(BaseModel):
    question: str
    preferred_language: Language = Field(description="bn or en")
    subject: Optional[str] = None


class QAResponse(BaseModel):
    subject: Optional[str]
    question: str
    answer_steps: List[str]
    explanation_bn: Optional[str] = None
    explanation_en: Optional[str] = None


class MathSolveRequest(BaseModel):
    expression: str
    preferred_language: Language


class MathSolveResponse(BaseModel):
    steps: List[str]
    result: str
    explanation_bn: Optional[str] = None
    explanation_en: Optional[str] = None


class QuizRequest(BaseModel):
    subject: str
    grade: int = Field(ge=5, le=12)
    preferred_language: Language
    num_mcq: int = 10
    num_short: int = 5


class MCQ(BaseModel):
    question: str
    options: List[str]
    answer_index: int
    explanation: Optional[str] = None


class ShortQuestion(BaseModel):
    question: str
    answer: Optional[str] = None


class QuizResponse(BaseModel):
    subject: str
    grade: int
    mcqs: List[MCQ]
    shorts: List[ShortQuestion]


class CreateCheckoutRequest(BaseModel):
    plan_id: str
    user_id: str
    provider: Literal["bkash", "nagad", "rocket", "card"]


class CheckoutResponse(BaseModel):
    provider: str
    checkout_url: str
    reference_id: str


class WebhookEvent(BaseModel):
    provider: str
    reference_id: str
    status: Literal["success", "failed", "cancelled"]
    amount: Optional[float] = None

