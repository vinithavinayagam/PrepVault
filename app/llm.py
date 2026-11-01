from google import genai

from app.config import get_settings


def generate_answer(question: str) -> str:
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError("Gemini API key is missing")

    client = genai.Client(api_key=settings.gemini_api_key)

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=question,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return response.text