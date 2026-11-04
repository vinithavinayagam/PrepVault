from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_success(monkeypatch):
    def mock_generate_answer(question):
        return "A stack follows LIFO."

    monkeypatch.setattr(
        "app.main.generate_answer",
        mock_generate_answer,
    )

    response = client.post(
        "/chat",
        json={"question": "What is a Stack?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "A stack follows LIFO."
    assert data["status"] == "success"


def test_chat_llm_failure(monkeypatch):
    def mock_generate_answer(question):
        raise RuntimeError("Gemini service unavailable")

    monkeypatch.setattr(
        "app.main.generate_answer",
        mock_generate_answer,
    )

    response = client.post(
        "/chat",
        json={"question": "What is a Stack?"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == ("LLM service failed. Please try again.")
