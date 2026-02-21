"""API tests for backend FastAPI routes."""

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.state import store


client = TestClient(app)


def setup_function() -> None:
    store.reset_state()


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"service": "backend", "status": "ok"}


def test_conversations_initially_empty() -> None:
    response = client.get("/conversations")

    assert response.status_code == 200
    assert response.json() == []


def test_approvals_seeded() -> None:
    response = client.get("/approvals")

    assert response.status_code == 200
    approvals = response.json()
    assert len(approvals) == 1
    assert approvals[0]["id"] == "apr-1"
    assert approvals[0]["status"] == "pending"


def test_chat_creates_conversation() -> None:
    response = client.post("/chat", json={"message": "hello"})

    assert response.status_code == 200
    body = response.json()
    assert body["conversation"]["messages"][0]["role"] == "user"
    assert body["conversation"]["messages"][0]["content"] == "hello"
    assert body["conversation"]["messages"][1]["role"] == "assistant"


def test_chat_validation_error_for_empty_message() -> None:
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_approval_decision_updates_status() -> None:
    response = client.post("/approvals/apr-1/decision", json={"decision": "approved"})

    assert response.status_code == 200
    assert response.json()["approval"]["status"] == "approved"


def test_approval_decision_not_found() -> None:
    response = client.post(
        "/approvals/apr-missing/decision",
        json={"decision": "approved"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Approval not found"}
