import io
import re
from pathlib import Path

from PIL import Image

def _extract_fields(text):
    patterns = {
        "name": [
            r"(?im)^\s*(?:applicant\s+)?name\s*[:\-]\s*(.+?)\s*$",
            r"(?im)^\s*full\s+name\s*[:\-]\s*(.+?)\s*$",
        ],
        "date_of_birth": [
            r"(?im)^\s*(?:date\s+of\s+birth|dob)\s*[:\-]\s*([0-9./-]+)\s*$",
        ],
        "id_number": [
            r"(?im)^\s*(?:id\s*(?:number|no)?|reference\s*(?:number|no))\s*[:\-]\s*([A-Za-z0-9-]+)\s*$",
        ],
        "address": [
            r"(?im)^\s*address\s*[:\-]\s*(.+?)\s*$",
        ],
        "phone": [
            r"(?im)^\s*(?:phone|mobile|contact)\s*[:\-]\s*([+0-9() -]{7,})\s*$",
        ],
        "email": [
            r"(?im)^\s*email\s*[:\-]\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\s*$",
        ],
    }
    out = {}
    for key, regexes in patterns.items():
        for pattern in regexes:
            match = re.search(pattern, text)
            if match:
                out[key] = match.group(1).strip()
                break
    return out

def _ocr_image(image):
    try:
        import pytesseract
        return pytesseract.image_to_string(image)
    except Exception as exc:
        return f"[OCR unavailable: {exc}]"

def extract_document(filename, raw):
    ext = Path(filename).suffix.lower()
    pages = []
    image_for_screening = None

    if ext == ".txt":
        text = raw.decode("utf-8", errors="replace")
        pages = [{"page": 1, "text": text}]
    elif ext == ".docx":
        from docx import Document
        doc = Document(io.BytesIO(raw))
        text = "\n".join(p.text for p in doc.paragraphs)
        pages = [{"page": 1, "text": text}]
    elif ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            for i, page in enumerate(reader.pages, start=1):
                pages.append({"page": i, "text": page.extract_text() or ""})
            text = "\n".join(p["text"] for p in pages)
            if not text.strip():
                text = "[This PDF appears image-based. Convert pages to images and use OCR externally for this prototype.]"
        except Exception as exc:
            text = ""
            pages = []
            raise RuntimeError(f"PDF extraction failed: {exc}")
    elif ext in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        image_for_screening = Image.open(io.BytesIO(raw)).convert("RGB")
        text = _ocr_image(image_for_screening)
        pages = [{"page": 1, "text": text}]
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return {
        "filename": filename,
        "text": text,
        "pages": pages,
        "fields": _extract_fields(text),
        "image": image_for_screening,
        "error": None,
    }
