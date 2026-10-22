"""
PDF Parser Service for extracting and validating resume documents.
Supports pdfplumber, pypdf, and pure-Python text extraction fallbacks.
Gracefully flags scanned/image-only PDFs and provides an OCR extension hook.
"""

import os
import re
from typing import Tuple, Dict, Any, Optional
from config import MAX_UPLOAD_SIZE_MB, ALLOWED_EXTENSIONS

def validate_pdf_file(filename: str, file_size_bytes: int) -> Tuple[bool, str]:
    """Validates file extension and size constraints."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type '{ext}'. Only PDF documents (.pdf) are permitted."

    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size_bytes <= 0:
        return False, "Uploaded file is empty (0 bytes)."
    if file_size_bytes > max_bytes:
        return False, f"File size ({file_size_bytes / (1024*1024):.1f} MB) exceeds maximum allowed size of {MAX_UPLOAD_SIZE_MB} MB."

    return True, "File is valid."

def extract_text_from_pdf(file_bytes: bytes, filename: str = "resume.pdf") -> Dict[str, Any]:
    """
    Extracts plain text from PDF bytes.
    Handles empty, corrupt, password-protected, and scanned PDFs gracefully.
    """
    is_valid, validation_msg = validate_pdf_file(filename, len(file_bytes))
    if not is_valid:
        return {
            "success": False,
            "raw_text": "",
            "is_scanned": False,
            "page_count": 0,
            "error": validation_msg
        }

    raw_text = ""
    page_count = 0
    extracted_method = "none"

    # Attempt 1: pdfplumber if installed
    try:
        import pdfplumber
        import io
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    raw_text += txt + "\n\n"
        extracted_method = "pdfplumber"
    except ImportError:
        # Attempt 2: pypdf if installed
        try:
            import pypdf
            import io
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    raw_text += txt + "\n\n"
            extracted_method = "pypdf"
        except ImportError:
            # Attempt 3: Standard Python PDF stream text decoder
            try:
                import io
                content = file_bytes.decode('latin-1', errors='ignore')
                # Find all text stream objects between BT (Begin Text) and ET (End Text)
                text_matches = re.findall(r'BT\s*(.*?)\s*ET', content, re.DOTALL)
                extracted_lines = []
                for match in text_matches:
                    strings = re.findall(r'\((.*?)\)\s*T[jJ]', match)
                    if strings:
                        extracted_lines.append(" ".join(strings))
                if extracted_lines:
                    raw_text = "\n".join(extracted_lines)
                    page_count = max(1, content.count("/Type /Page"))
                else:
                    # Strip nulls and extract basic ASCII chunks
                    ascii_strings = re.findall(r'[A-Za-z0-9 ,.\-@:/+]{4,}', content)
                    raw_text = "\n".join(ascii_strings)
                    page_count = 1
                extracted_method = "built_in_stream_decoder"
            except Exception as e:
                return {
                    "success": False,
                    "raw_text": "",
                    "is_scanned": False,
                    "page_count": 0,
                    "error": f"Failed to parse PDF file structure: {str(e)}"
                }
    except Exception as e:
        err_msg = str(e).lower()
        if "password" in err_msg or "encrypt" in err_msg:
            return {
                "success": False,
                "raw_text": "",
                "is_scanned": False,
                "page_count": 0,
                "error": "This PDF is password-protected. Please remove the password and re-upload."
            }
        return {
            "success": False,
            "raw_text": "",
            "is_scanned": False,
            "page_count": 0,
            "error": f"PDF parsing error: {str(e)}"
        }

    raw_text = raw_text.strip()
    is_scanned = len(raw_text) < 60

    if is_scanned:
        return {
            "success": True,
            "raw_text": raw_text,
            "is_scanned": True,
            "page_count": page_count,
            "method": extracted_method,
            "warning": (
                "Scanned or Image-Only PDF Detected: Extracted text contains fewer than 60 characters. "
                "Optical Character Recognition (OCR) is required for scanned documents. "
                "To run an OCR analysis, connect an OCR engine (e.g., Tesseract OCR or Google Document AI) "
                "or upload a text-selectable PDF."
            )
        }

    return {
        "success": True,
        "raw_text": raw_text,
        "is_scanned": False,
        "page_count": page_count,
        "method": extracted_method,
        "warning": None
    }

def ocr_extension_hook(file_bytes: bytes) -> Optional[str]:
    """
    Extension point for optional OCR integration (e.g. pytesseract / Google Cloud Vision).
    Returns extracted text if OCR provider is configured, otherwise None.
    """
    # Extension hook placeholder for future OCR providers
    return None
