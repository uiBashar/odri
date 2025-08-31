from typing import List
from sympy import symbols, Eq, solve, sympify
from sympy.core.sympify import SympifyError
from ..models.schemas import MathSolveRequest, MathSolveResponse


def _explain_result(result_expr) -> str:
    try:
        return str(result_expr)
    except Exception:
        return ""


def solve_expression(payload: MathSolveRequest) -> MathSolveResponse:
    steps: List[str] = []
    expr_text = payload.expression.strip()
    try:
        # Try to parse equations of form 'x^2 + 5x + 6 = 0'
        if "=" in expr_text:
            left, right = expr_text.split("=", 1)
            left_sym = sympify(left.replace("^", "**"))
            right_sym = sympify(right.replace("^", "**"))
            eq = Eq(left_sym, right_sym)
            steps.append("Parsed equation and formed equality")
            symbol_candidates = list(eq.free_symbols)
            result = solve(eq, symbol_candidates[0]) if symbol_candidates else solve(eq)
        else:
            sym = sympify(expr_text.replace("^", "**"))
            steps.append("Parsed expression for simplification/solution")
            result = solve(sym)
        explanation_bn = None
        explanation_en = None
        if payload.preferred_language == "bn":
            explanation_bn = "ধাপে ধাপে সমাধান উপরের স্টেপে দেখানো হলো।"
        else:
            explanation_en = "Step-by-step solution is shown above."
        return MathSolveResponse(
            steps=steps,
            result=_explain_result(result),
            explanation_bn=explanation_bn,
            explanation_en=explanation_en,
        )
    except SympifyError as exc:
        steps.append(f"Parse error: {exc}")
        return MathSolveResponse(steps=steps, result="", explanation_en="Invalid expression")

