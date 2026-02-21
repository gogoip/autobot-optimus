"""In-memory state store and service layer functions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from backend.app.models import (
    Approval,
    ApprovalDecisionResponse,
    ChatResponse,
    Conversation,
    HealthResponse,
    Message,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class AppState:
    """State container for conversations and approvals."""

    conversations: dict[str, Conversation] = field(default_factory=dict)
    approvals: dict[str, Approval] = field(default_factory=dict)


class InMemoryStore:
    """Simple threadsafe in-memory store for API operations."""

    def __init__(self) -> None:
        self._state = AppState()
        self._lock = Lock()
        self._seed_approvals()

    def _seed_approvals(self) -> None:
        seeded = Approval(
            id="apr-1",
            description="Review and approve initial deployment plan",
            status="pending",
            created_at=_utcnow(),
        )
        self._state.approvals[seeded.id] = seeded

    def get_health(self) -> HealthResponse:
        return HealthResponse()

    def list_conversations(self) -> list[Conversation]:
        with self._lock:
            return list(self._state.conversations.values())

    def list_approvals(self) -> list[Approval]:
        with self._lock:
            return list(self._state.approvals.values())

    def create_chat(
        self, user_message: str, conversation_id: str | None = None
    ) -> ChatResponse | None:
        now = _utcnow()
        user = Message(role="user", content=user_message, created_at=now)
        assistant = Message(
            role="assistant",
            content=f"Received your message: {user_message}",
            created_at=now,
        )

        with self._lock:
            if conversation_id is not None:
                existing = self._state.conversations.get(conversation_id)
                if existing is None:
                    return None

                updated = existing.model_copy(
                    update={
                        "messages": [*existing.messages, user, assistant],
                        "updated_at": now,
                    }
                )
                self._state.conversations[conversation_id] = updated
                return ChatResponse(conversation=updated)

            new_conversation_id = str(uuid4())
            conversation = Conversation(
                id=new_conversation_id,
                messages=[user, assistant],
                created_at=now,
                updated_at=now,
            )
            self._state.conversations[new_conversation_id] = conversation

        return ChatResponse(conversation=conversation)

    def set_approval_decision(
        self, approval_id: str, decision: str
    ) -> ApprovalDecisionResponse | None:
        with self._lock:
            approval = self._state.approvals.get(approval_id)
            if approval is None:
                return None

            updated = approval.model_copy(
                update={"status": decision, "decided_at": _utcnow()}
            )
            self._state.approvals[approval_id] = updated

        return ApprovalDecisionResponse(approval=updated)


store = InMemoryStore()


def reset_state() -> None:
    """Reset in-memory state for deterministic tests."""
    global store
    store = InMemoryStore()


def get_health() -> HealthResponse:
    return store.get_health()


def list_conversations() -> list[Conversation]:
    return store.list_conversations()


def list_approvals() -> list[Approval]:
    return store.list_approvals()


def create_chat(
    user_message: str, conversation_id: str | None = None
) -> ChatResponse | None:
    return store.create_chat(user_message=user_message, conversation_id=conversation_id)


def set_approval_decision(
    approval_id: str, decision: str
) -> ApprovalDecisionResponse | None:
    return store.set_approval_decision(approval_id=approval_id, decision=decision)
