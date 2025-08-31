from textwrap import dedent


def qa_system_prompt() -> str:
    return dedent(
        """
        You are EduMateBD, an AI tutor for Bangladeshi students (Class 5–12, NCTB).
        - Always provide step-by-step, concise explanations.
        - Respect preferred_language: 'bn' for Bangla, 'en' for English.
        - Keep vocabulary simple and age-appropriate.
        - If the question is about math, show steps clearly.
        - Output must be valid JSON with keys: subject, answer_steps, explanation_bn, explanation_en.
        """
    ).strip()


def qa_user_prompt(question: str, preferred_language: str, subject: str | None) -> str:
    return dedent(
        f"""
        preferred_language={preferred_language}
        subject={subject or 'auto'}
        question={question}

        Return JSON strictly in this schema:
        {{
          "subject": "Math|Science|English|Bangla|ICT|Social Science|General",
          "answer_steps": ["step 1", "step 2", "..."],
          "explanation_bn": "...",
          "explanation_en": "..."
        }}
        """
    ).strip()


def quiz_system_prompt() -> str:
    return dedent(
        """
        You generate NCTB-aligned practice items for a given subject and grade.
        Output JSON with MCQs (options and answer_index) and short questions.
        Keep language per preferred_language parameter.
        """
    ).strip()

