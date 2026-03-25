"""FastAPI router — OCR endpoints."""

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ocr_webapp.core.ocr_engine import OCREngine
from ocr_webapp.models.ocr import OCRResponse
from ocr_webapp.utils.config import settings
from ocr_webapp.utils.logging import get_logger

router = APIRouter(prefix="/ocr", tags=["OCR"])
logger = get_logger(__name__)
engine = OCREngine()

_MAX_BYTES = settings.max_upload_size_mb * 1024 * 1024


@router.post("/extract", response_model=OCRResponse, status_code=status.HTTP_200_OK)
async def extract_text(file: UploadFile = File(...)) -> OCRResponse:
    """Upload an image and receive the extracted text."""
    content = await file.read()
    if len(content) > _MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.max_upload_size_mb} MB limit.",
        )

    suffix = Path(file.filename or "upload").suffix or ".png"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        text, confidence = engine.extract_with_confidence(tmp_path)
    except Exception as exc:
        logger.exception("OCR failed for %s", file.filename)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    return OCRResponse(
        filename=file.filename or "unknown",
        text=text,
        confidence=confidence,
        language=engine.lang,
    )
