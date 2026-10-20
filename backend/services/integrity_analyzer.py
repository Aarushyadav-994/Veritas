import io
import base64
from typing import Dict, Any, List
from PIL import Image, ImageChops, ImageEnhance
import fitz

class IntegrityAnalyzer:
    @staticmethod
    def analyze_pdf_integrity(doc_metadata: Dict[str, Any], file_bytes: bytes) -> Dict[str, Any]:
        """
        Inspects PDF metadata, structure, and compression artifacts for forensic indicators.
        """
        indicators: List[Dict[str, Any]] = []
        creation_date = doc_metadata.get("creation_date", "")
        mod_date = doc_metadata.get("modification_date", "")
        creator = doc_metadata.get("creator", "")
        producer = doc_metadata.get("producer", "")
        filename = doc_metadata.get("filename", "")

        # 1. Metadata Timestamp Discrepancy Check
        if creation_date and mod_date:
            if creation_date != mod_date:
                indicators.append({
                    "finding": "Post-Creation Revision Detected",
                    "page_or_region": "Document Header Metadata",
                    "detection_method": "PDF Dictionary Date Tag Comparison",
                    "observed_evidence": f"Creation Date: {creation_date} | Modification Date: {mod_date}",
                    "severity": "MODERATE",
                    "interpretation": "The document was modified after initial generation. While routine for counter-signed or reviewed drafts, significant elapsed time may warrant revision verification.",
                    "limitations": "Does not identify specific modified fields or indicate unauthorized tampering.",
                    "recommended_manual_check": "Compare with counterpart's original execution copy or inspect PDF revision history."
                })
        elif not creation_date and not mod_date:
            indicators.append({
                "finding": "Missing Generation Timestamps",
                "page_or_region": "Document Metadata Stream",
                "detection_method": "XMP / Info Dictionary Audit",
                "observed_evidence": "Neither CreationDate nor ModDate fields are populated.",
                "severity": "LOW",
                "interpretation": "Document was created or processed by a tool that strips timestamp metadata.",
                "limitations": "Many privacy tools intentionally scrub metadata; does not indicate malicious tampering.",
                "recommended_manual_check": "Verify document provenance through email transmission logs or digital signatures."
            })

        # 2. Producer / Editor Profile Audit
        consumer_editors = ["canva", "photoshop", "gimp", "ilovepdf", "smallpdf", "pdfescape", "sejda", "nitro", "foxit"]
        producer_lower = (producer + " " + creator).lower()
        matched_editors = [ed for ed in consumer_editors if ed in producer_lower]

        if matched_editors:
            indicators.append({
                "finding": f"Consumer Modification Utility Identified ({', '.join(matched_editors).title()})",
                "page_or_region": "Producer / Creator Metadata",
                "detection_method": "Application Signature String Match",
                "observed_evidence": f"Producer: '{producer}' | Creator: '{creator}'",
                "severity": "MODERATE",
                "interpretation": "Document was processed using a consumer-grade PDF utility or graphic design software rather than standard enterprise document systems.",
                "limitations": "Parties may legitimately use consumer web tools to assemble or compress scans.",
                "recommended_manual_check": "Verify with the drafting party whether text or exhibits were altered using third-party tools."
            })
        else:
            indicators.append({
                "finding": "Standard Enterprise Producer Profile",
                "page_or_region": "Producer / Creator Metadata",
                "detection_method": "Application Signature String Match",
                "observed_evidence": f"Producer: '{producer or 'Standard PDF Engine'}'",
                "severity": "LOW",
                "interpretation": "Producer metadata aligns with typical business document generation pipelines.",
                "limitations": "Metadata fields can be spoofed or rewritten by determined actors.",
                "recommended_manual_check": "Verify digital signature certificate if available."
            })

        # 3. Incremental Update and Revision Analysis
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            page_count = len(doc)
            image_count = 0
            font_list = set()

            for page in doc:
                image_count += len(page.get_images())
                for f in page.get_fonts():
                    font_list.add(f[3]) # font family

            if len(font_list) > 12:
                indicators.append({
                    "finding": "High Typographic Heterogeneity",
                    "page_or_region": "Document Typography Layer",
                    "detection_method": "Font Descriptor Extraction",
                    "observed_evidence": f"Detected {len(font_list)} distinct font families across {page_count} pages.",
                    "severity": "NEEDS REVIEW",
                    "interpretation": "High number of distinct fonts may indicate spliced sections, merged annexures, or post-hoc text inserts.",
                    "limitations": "Multi-exhibit contracts and templates naturally combine multiple font families.",
                    "recommended_manual_check": "Manually inspect clause headings and body text for sudden font weight/kerning shifts."
                })

            doc.close()
        except Exception:
            pass

        # 4. Generate Error Level Analysis (ELA) for Page 1
        ela_result = IntegrityAnalyzer.perform_ela_on_first_page(file_bytes)

        return {
            "section_title": "Document Integrity Indicators",
            "overall_integrity_status": "Qualified - Heuristic Verification Only",
            "disclaimer": "These indicators reflect heuristic file analysis and do NOT constitute conclusive proof of document authenticity or fraudulent alteration.",
            "indicators": indicators,
            "ela": ela_result
        }

    @staticmethod
    def perform_ela_on_first_page(file_bytes: bytes) -> Dict[str, Any]:
        """
        Computes Error Level Analysis (ELA) on the primary document page or image.
        Re-encodes image at quality 90 and measures compression difference scaled 15x.
        """
        try:
            # Check if it's a PDF or direct image
            img: Image.Image
            if file_bytes.startswith(b"%PDF"):
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                if len(doc) == 0:
                    return {"enabled": False, "reason": "No pages in PDF"}
                pix = doc[0].get_pixmap(dpi=120)
                img = Image.open(io.BytesIO(pix.tobytes("jpeg"))).convert("RGB")
                doc.close()
            else:
                img = Image.open(io.BytesIO(file_bytes)).convert("RGB")

            # Resize if very large for performance
            max_dim = 1000
            if img.width > max_dim or img.height > max_dim:
                img.thumbnail((max_dim, max_dim))

            # Original image to base64
            orig_buf = io.BytesIO()
            img.save(orig_buf, format="JPEG", quality=95)
            orig_b64 = "data:image/jpeg;base64," + base64.b64encode(orig_buf.getvalue()).decode("utf-8")

            # Save temporary at quality 90
            ela_buf = io.BytesIO()
            img.save(ela_buf, format="JPEG", quality=90)
            ela_buf.seek(0)
            resaved_img = Image.open(ela_buf).convert("RGB")

            # Compute pixel difference
            diff = ImageChops.difference(img, resaved_img)

            # Amplify difference (15x scale)
            enhancer = ImageEnhance.Brightness(diff)
            amplified_diff = enhancer.enhance(15.0)

            diff_buf = io.BytesIO()
            amplified_diff.save(diff_buf, format="PNG")
            diff_b64 = "data:image/png;base64," + base64.b64encode(diff_buf.getvalue()).decode("utf-8")

            return {
                "enabled": True,
                "original_preview": orig_b64,
                "ela_preview": diff_b64,
                "explanation": "Error Level Analysis (ELA) highlights compression potential variations across the document surface. In a pristine digital export, compression levels are typically uniform. Brighter regions indicate areas where compression characteristics diverge from the background grid.",
                "limitations": "ELA reveals compression discrepancies only. Legitimate elements such as high-contrast vector lines, signatures, dark borders, and scanned annexures naturally produce elevated ELA response without indicating tampering.",
                "manual_check": "Examine if highlighted regions correspond to localized text additions, spliced signature blocks, or altered financial sums."
            }
        except Exception as e:
            return {
                "enabled": False,
                "reason": f"ELA processing unavailable for this file: {str(e)}"
            }
