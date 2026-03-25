"""Core OCR engine — wraps pytesseract with a clean interface."""

from pathlib import Path

from PIL import Image

from ocr_webapp.utils.config import settings
from ocr_webapp.utils.logging import get_logger

logger = get_logger(__name__)


class OCREngine:
    """Thin wrapper around pytesseract. Swap this class to change the backend."""

    def __init__(self, lang: str | None = None) -> None:
        self.lang = lang or settings.tesseract_lang

    def extract_text(self, image_path: Path) -> str:
        """Return extracted text from *image_path*."""
        import pytesseract  # lazy import — optional dependency

        logger.debug("Running OCR on %s (lang=%s)", image_path, self.lang)
        image = Image.open(image_path)
        text: str = pytesseract.image_to_string(image, lang=self.lang)
        return text.strip()

    def extract_with_confidence(self, image_path: Path) -> tuple[str, float]:
        """Return (text, mean_confidence) tuple."""
        import pytesseract

        image = Image.open(image_path)
        data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
        confidences = [int(c) for c in data["conf"] if str(c).isdigit() and int(c) >= 0]
        mean_conf = sum(confidences) / len(confidences) if confidences else 0.0
        text = " ".join(w for w in data["text"] if w.strip())
        return text, round(mean_conf, 2)
