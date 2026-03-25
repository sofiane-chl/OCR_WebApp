"""Pydantic schemas for OCR request/response."""

from pydantic import BaseModel, Field


class OCRResponse(BaseModel):
    filename: str
    text: str
    confidence: float | None = Field(default=None, ge=0.0, le=100.0)
    language: str = "eng"
