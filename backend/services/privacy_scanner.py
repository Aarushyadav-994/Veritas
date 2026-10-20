import re
from typing import Dict, Any, List
import fitz

class PrivacyScanner:
    # Compile robust patterns
    PATTERNS = {
        "PAN Card (Tax ID)": {
            "regex": re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"),
            "risk": "HIGH",
            "disclosure_risk": "Direct tax and corporate identity identifier. Exposure risks tax identity fraud or unauthorized credit checks.",
            "mitigation": "Redact alphanumeric identifier in copies transmitted to external vendors or subcontractors.",
            "mask_func": lambda s: s[:5] + "****" + s[-1]
        },
        "Aadhaar / National ID": {
            "regex": re.compile(r"\b[2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b"),
            "risk": "HIGH",
            "disclosure_risk": "Unique personal identification number. Direct violation of Indian Aadhaar Act regulations if shared unmasked.",
            "mitigation": "Mandatorily mask first 8 digits; retain only final 4 digits per UIDAI regulations.",
            "mask_func": lambda s: "XXXX-XXXX-" + re.sub(r"\s", "", s)[-4:]
        },
        "Email Address": {
            "regex": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
            "risk": "MODERATE",
            "disclosure_risk": "Direct point-of-contact exposure susceptible to targeted phishing, spear-phishing, and social engineering.",
            "mitigation": "Substitute with general corporate aliases (e.g. legal@domain.com) for public filings.",
            "mask_func": lambda s: s.split("@")[0][:2] + "***@" + s.split("@")[1]
        },
        "Phone Number": {
            "regex": re.compile(r"(?:\+?91[\-\s]?)?[6-9]\d{9}\b|\b(?:\+?1[\-\s]?)?\(?\d{3}\)?[\-\s]?\d{3}[\-\s]?\d{4}\b"),
            "risk": "MODERATE",
            "disclosure_risk": "Personal mobile or direct telephone number. Facilitates unsolicited outreach, SMS spoofing, or credential social engineering.",
            "mitigation": "Replace with official company switchboard or mask central digits.",
            "mask_func": lambda s: s[:4] + "*****" + s[-3:] if len(s) > 7 else "****"
        },
        "Bank Account Number": {
            "regex": re.compile(r"(?:(?:Account|A/C|Acct|Bank)\s*(?:No\.?|Number|#)?\s*[:\-]?\s*)(\d{9,18})\b", re.IGNORECASE),
            "risk": "HIGH",
            "disclosure_risk": "Direct bank routing and account data. Exposes corporate or individual liquidity details to account takeover attempts.",
            "mitigation": "Mask central 6-10 digits in operational agreements; verify billing via secure payment gateway tokens.",
            "mask_func": lambda s: "************" + s[-4:]
        },
        "IFSC Code": {
            "regex": re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b"),
            "risk": "MODERATE",
            "disclosure_risk": "Identifies exact bank branch and financial institution holding party accounts.",
            "mitigation": "Mask or withhold until final payment invoice execution.",
            "mask_func": lambda s: s[:4] + "0******"
        }
    }

    @staticmethod
    def scan_document(pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans page text for sensitive personal and corporate data with context validation.
        """
        findings: List[Dict[str, Any]] = []
        all_matches_for_redaction: List[Dict[str, Any]] = []

        for info_type, config in PrivacyScanner.PATTERNS.items():
            pattern = config["regex"]
            risk = config["risk"]
            mitigation = config["mitigation"]
            disc_risk = config["disclosure_risk"]
            masker = config["mask_func"]

            matched_items: List[Dict[str, Any]] = []

            for page in pages_data:
                page_num = page["page_number"]
                text = page["text"]

                # Special handling for regex with capturing groups (e.g. Bank Account)
                for match in pattern.finditer(text):
                    raw_val = match.group(1) if match.groups() else match.group(0)
                    raw_val = raw_val.strip()

                    # Contextual filter for bank accounts to avoid plain numbers
                    if info_type == "Bank Account Number" and (len(raw_val) < 9 or len(raw_val) > 18):
                        continue

                    masked_val = masker(raw_val)

                    item_entry = {
                        "page": page_num,
                        "raw_val": raw_val,
                        "masked_val": masked_val
                    }
                    matched_items.append(item_entry)
                    all_matches_for_redaction.append({
                        "page": page_num,
                        "text": raw_val,
                        "type": info_type
                    })

            if matched_items:
                unique_masked = list({m["masked_val"] for m in matched_items})
                pages_found = sorted(list({m["page"] for m in matched_items}))

                findings.append({
                    "info_type": info_type,
                    "count": len(matched_items),
                    "pages": pages_found,
                    "risk_level": risk,
                    "disclosure_risk": disc_risk,
                    "mitigation": mitigation,
                    "masked_samples": unique_masked[:4]
                })

        # Calculate exposure score
        high_count = sum(1 for f in findings if f["risk_level"] == "HIGH")
        mod_count = sum(1 for f in findings if f["risk_level"] == "MODERATE")
        total_detections = sum(f["count"] for f in findings)

        if high_count > 0:
            overall_exposure = "CRITICAL" if total_detections > 5 else "HIGH"
        elif mod_count > 0:
            overall_exposure = "MODERATE"
        elif total_detections > 0:
            overall_exposure = "LOW"
        else:
            overall_exposure = "MINIMAL"

        return {
            "overall_exposure": overall_exposure,
            "total_detections": total_detections,
            "findings": findings,
            "can_redact": len(all_matches_for_redaction) > 0,
            "redaction_targets_count": len(all_matches_for_redaction)
        }

    @staticmethod
    def generate_redacted_pdf(file_bytes: bytes, pages_data: List[Dict[str, Any]]) -> bytes:
        """
        Applies permanent, unrecoverable PDF text redaction using PyMuPDF.
        Genuinely removes underlying text stream and replaces with solid redaction marks.
        """
        if not file_bytes.startswith(b"%PDF"):
            return file_bytes

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        for info_type, config in PrivacyScanner.PATTERNS.items():
            pattern = config["regex"]

            for page_idx in range(len(doc)):
                page = doc[page_idx]
                page_text = page.get_text("text")

                for match in pattern.finditer(page_text):
                    raw_val = match.group(1) if match.groups() else match.group(0)
                    raw_val = raw_val.strip()

                    if len(raw_val) < 4:
                        continue

                    # Search text instances on the page
                    quads = page.search_for(raw_val)
                    for rect in quads:
                        # True redaction annotation
                        page.add_redact_annot(rect, fill=(0.1, 0.1, 0.1))

                # Apply redactions to permanently scrub text
                page.apply_redactions()

        output_bytes = doc.tobytes(garbage=4, deflate=True)
        doc.close()
        return output_bytes
