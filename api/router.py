from fastapi import APIRouter

from api.interviewer import Interviewer
from schemas.chat import ChatRequest, ChatResponse


router = APIRouter(prefix="/interview", tags=["interview"])
interviewer = Interviewer()


@router.post("/ask", response_model=ChatResponse)
def ask(req: ChatRequest) -> ChatResponse:
    history_dicts = (
        [m.model_dump() for m in req.history] if req.history is not None else None
    )
    answer = interviewer.ask(req.question, history=history_dicts)
    return ChatResponse(answer=answer)


