"""HTTP route handlers for backend API."""

from fastapi import APIRouter, HTTPException

from backend.app.models import (
    Approval,
    ApprovalDecisionRequest,
    ApprovalDecisionResponse,
    ChatRequest,
    ChatResponse,
    Conversation,
    HealthResponse,
)
from backend.app.state import store

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return store.get_health()


@router.get("/conversations", response_model=list[Conversation])
def conversations() -> list[Conversation]:
    return store.list_conversations()


@router.get("/approvals", response_model=list[Approval])
def approvals() -> list[Approval]:
    return store.list_approvals()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    result = store.create_chat(
        user_message=payload.message,
        conversation_id=payload.conversation_id,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result


@router.post(
    "/approvals/{approval_id}/decision", response_model=ApprovalDecisionResponse
)
def approval_decision(
    approval_id: str, payload: ApprovalDecisionRequest
) -> ApprovalDecisionResponse:
    result = store.set_approval_decision(
        approval_id=approval_id,
        decision=payload.decision,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    return result
