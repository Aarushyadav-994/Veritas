import os
import io
import fitz  # PyMuPDF
from PIL import Image
from typing import Dict, Any, List, Optional
import base64

class DocumentExtractionError(Exception):
    pass

class DocumentExtractor:
    @staticmethod
    def extract_document(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Extracts document pages, text, metadata, and structural info from PDF or image.
        """
        ext = os.path.splitext(filename.lower())[1]
        if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
            raise DocumentExtractionError(f"Unsupported file format '{ext}'. Allowed: PDF, PNG, JPG, JPEG.")

        if len(file_bytes) == 0:
            raise DocumentExtractionError("The uploaded file is empty (0 bytes).")

        if len(file_bytes) > 25 * 1024 * 1024:
            raise DocumentExtractionError("File exceeds the maximum 25 MB limit.")

        if ext == ".pdf":
            return DocumentExtractor._extract_pdf(file_bytes, filename)
        else:
            return DocumentExtractor._extract_image(file_bytes, filename)

    @staticmethod
    def _extract_pdf(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            raise DocumentExtractionError(f"Corrupted or invalid PDF file: {str(e)}")

        if doc.is_encrypted:
            # Try empty password
            if not doc.authenticate(""):
                raise DocumentExtractionError("The uploaded PDF is password-protected. Please upload an unprotected document.")

        page_count = len(doc)
        if page_count == 0:
            raise DocumentExtractionError("PDF contains zero pages.")

        pages_data: List[Dict[str, Any]] = []
        full_text_list: List[str] = []
        page_images_base64: List[str] = []

        for page_idx in range(page_count):
            page = doc[page_idx]
            page_num = page_idx + 1
            text = page.get_text("text").strip()
            full_text_list.append(text)

            # Render page image (first 5 pages max for performance)
            img_b64 = ""
            if page_idx < 5:
                try:
                    pix = page.get_pixmap(dpi=130)
                    img_bytes = pix.tobytes("jpeg")
                    img_b64 = "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode("utf-8")
                except Exception:
                    img_b64 = ""
            page_images_base64.append(img_b64)

            # Count words/characters
            pages_data.append({
                "page_number": page_num,
                "text": text,
                "character_count": len(text),
                "word_count": len(text.split()),
                "has_images": len(page.get_images()) > 0,
                "preview_image": img_b64
            })

        total_text = "\n\n--- Page Break ---\n\n".join(full_text_list).strip()
        is_scanned_likely = len(total_text.replace("--- Page Break ---", "").strip()) < 50

        # Extract metadata
        raw_metadata = doc.metadata or {}
        sanitized_meta = {
            "title": raw_metadata.get("title", ""),
            "author": raw_metadata.get("author", ""),
            "creator": raw_metadata.get("creator", ""),
            "producer": raw_metadata.get("producer", ""),
            "creation_date": raw_metadata.get("creationDate", ""),
            "modification_date": raw_metadata.get("modDate", ""),
            "format": raw_metadata.get("format", "PDF"),
            "encryption": raw_metadata.get("encryption", "None"),
            "page_count": page_count,
            "file_size_bytes": len(file_bytes),
            "filename": filename
        }

        doc.close()

        return {
            "document_type": "PDF",
            "filename": filename,
            "page_count": page_count,
            "total_characters": sum(p["character_count"] for p in pages_data),
            "pages": pages_data,
            "full_text": total_text,
            "metadata": sanitized_meta,
            "is_scanned_likely": is_scanned_likely,
            "preview_images": [p for p in page_images_base64 if p]
        }

    @staticmethod
    def _extract_image(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img_format = img.format or "JPEG"
            width, height = img.size
        except Exception as e:
            raise DocumentExtractionError(f"Corrupted or invalid image file: {str(e)}")

        # Convert to base64 preview
        buffered = io.BytesIO()
        img.convert("RGB").save(buffered, format="JPEG", quality=85)
        img_b64 = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")

        # For images, we try PyMuPDF OCR or document container if possible, or provide structured image representation
        pages_data = [{
            "page_number": 1,
            "text": "[Image Document - Visual Forensic Analysis Enabled]",
            "character_count": 0,
            "word_count": 0,
            "has_images": True,
            "preview_image": img_b64
        }]

        sanitized_meta = {
            "title": filename,
            "format": img_format,
            "dimensions": f"{width}x{height}",
            "file_size_bytes": len(file_bytes),
            "filename": filename,
            "page_count": 1
        }

        return {
            "document_type": "IMAGE",
            "filename": filename,
            "page_count": 1,
            "total_characters": 0,
            "pages": pages_data,
            "full_text": "[Image Document - Visual Forensic Analysis Enabled]",
            "metadata": sanitized_meta,
            "is_scanned_likely": True,
            "preview_images": [img_b64],
            "raw_image_bytes": file_bytes
        }
