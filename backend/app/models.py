"""Pydantic schemas for backend API payloads."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    service: str = "backend"
    status: str = "ok"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime


class Conversation(BaseModel):
    id: str
    messages: list[Message]
    created_at: datetime
    updated_at: datetime


class ChatResponse(BaseModel):
    conversation: Conversation


class Approval(BaseModel):
    id: str
    description: str
    status: Literal["pending", "approved", "rejected"]
    created_at: datetime
    decided_at: datetime | None = None


class ApprovalDecisionRequest(BaseModel):
    decision: Literal["approved", "rejected"]


class ApprovalDecisionResponse(BaseModel):
    approval: Approval
