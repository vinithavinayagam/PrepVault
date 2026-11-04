from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    question: str
    answer: str
    status: str


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    college_slug: str = Field(min_length=1, max_length=100)


class Citation(BaseModel):
    filename: str
    page: int


class AskResponse(BaseModel):
    question: str
    college_slug: str
    answer: str
    citations: list[Citation]
    status: str
