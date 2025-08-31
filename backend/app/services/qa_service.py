from typing import Dict, Any
import asyncio
from ..models.schemas import QARequest, QAResponse
from ..core.config import settings
from .prompt_templates import qa_system_prompt, qa_user_prompt


async def _call_llm(messages: list[dict[str, str]]) -> Dict[str, Any]:
    # Placeholder to avoid hard dependency if key missing
    if not settings.openai_api_key:
        # Return a deterministic mock for local dev
        return {
            "subject": "General",
            "answer_steps": [
                "Step 1: Analyze the question",
                "Step 2: Provide the answer"
            ],
            "explanation_bn": "এটি একটি ডেমো উত্তর।",
            "explanation_en": "This is a demo response."
        }
    try:
        import openai  # type: ignore
        openai.api_key = settings.openai_api_key
        completion = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=settings.openai_model,
            messages=messages,
            temperature=0.2,
        )
        content = completion.choices[0].message["content"]
        # naive parse; production should return JSON from the model
        return {
            "subject": None,
            "answer_steps": [content],
            "explanation_bn": None,
            "explanation_en": content,
        }
    except Exception as exc:
        return {
            "subject": None,
            "answer_steps": [f"LLM error: {exc}"],
            "explanation_bn": None,
            "explanation_en": None,
        }


async def generate_answer(payload: QARequest) -> QAResponse:
    messages = [
        {"role": "system", "content": qa_system_prompt()},
        {"role": "user", "content": qa_user_prompt(payload.question, payload.preferred_language, payload.subject)},
    ]
    llm = await _call_llm(messages)
    return QAResponse(
        subject=llm.get("subject"),
        question=payload.question,
        answer_steps=llm.get("answer_steps", []),
        explanation_bn=llm.get("explanation_bn"),
        explanation_en=llm.get("explanation_en"),
    )

