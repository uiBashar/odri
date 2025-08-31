from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.routes_qa import router as qa_router
from .api.routes_math import router as math_router
from .api.routes_quiz import router as quiz_router
from .api.routes_payments import router as payments_router


app = FastAPI(
    title="EduMateBD API",
    version="0.1.0",
    description="AI-powered education assistant for Bangladesh (Bangla/English).",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(qa_router, prefix="/api")
app.include_router(math_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(payments_router, prefix="/api")

