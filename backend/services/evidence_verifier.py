import re
from typing import Dict, Any, List, Optional, Tuple

class EvidenceVerifier:
    """
    Validates that extracted quotations and excerpts genuinely exist in the source document.
    Performs normalized string comparison to accommodate harmless differences in line breaks,
    typographic quotes (curly vs straight), and multiple whitespaces while preserving substantive wording.
    """

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalizes whitespace and punctuation variants for reliable evidence matching.
        """
        if not text:
            return ""
        # Replace typographic quotes and dashes
        s = text.replace("\u201c", '"').replace("\u201d", '"')
        s = s.replace("\u2018", "'").replace("\u2019", "'")
        s = s.replace("\u2014", "-").replace("\u2013", "-")
        # Normalize multiple spaces and newlines into single spaces
        s = re.sub(r"\s+", " ", s)
        return s.strip()

    @staticmethod
    def verify_quotation(
        excerpt: str,
        full_text: str,
        pages_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Verifies whether an excerpt exists verbatim or substantially in the source document.
        Returns verification status, exact matched page number, and confidence score.
        """
        pages_list = pages_data or []
        if not excerpt or not full_text:
            return {
                "verified": False,
                "confidence": 0.0,
                "status": "UNVERIFIED",
                "matched_page": 1,
                "surrounding_context": "",
                "notes": "Empty excerpt or document text."
            }

        norm_excerpt = EvidenceVerifier.normalize_text(excerpt)
        norm_full = EvidenceVerifier.normalize_text(full_text)

        # 1. Exact match check
        if norm_excerpt in norm_full:
            matched_page = EvidenceVerifier.find_page_number(excerpt, pages_list)
            context = EvidenceVerifier.extract_context(norm_excerpt, norm_full)
            return {
                "verified": True,
                "confidence": 1.0,
                "status": "VERIFIED_VERBATIM",
                "matched_page": matched_page,
                "surrounding_context": context,
                "notes": "Exact verbatim match confirmed against extracted document stream."
            }

        # 2. Substring prefix match (for excerpts with trailing truncation)
        core_snippet = norm_excerpt[:min(len(norm_excerpt), 120)]
        if core_snippet in norm_full:
            matched_page = EvidenceVerifier.find_page_number(core_snippet, pages_list)
            context = EvidenceVerifier.extract_context(core_snippet, norm_full)
            return {
                "verified": True,
                "confidence": 0.90,
                "status": "VERIFIED_SUBSTRING",
                "matched_page": matched_page,
                "surrounding_context": context,
                "notes": "Core clause passage confirmed in source; trailing excerpt may be truncated."
            }

        # 3. Lowercase normalized match
        if norm_excerpt.lower() in norm_full.lower():
            matched_page = EvidenceVerifier.find_page_number(excerpt, pages_list)
            return {
                "verified": True,
                "confidence": 0.85,
                "status": "VERIFIED_CASE_INSENSITIVE",
                "matched_page": matched_page,
                "surrounding_context": "",
                "notes": "Matched source text with capitalization variations."
            }

        # 4. Fallback: unverified paraphrase
        return {
            "verified": False,
            "confidence": 0.35,
            "status": "UNVERIFIED_PARAPHRASE",
            "matched_page": EvidenceVerifier.find_page_number(excerpt, pages_data),
            "surrounding_context": "",
            "notes": "Passage could not be verified verbatim in extracted text. May represent an analytical paraphrase."
        }

    @staticmethod
    def find_page_number(excerpt: str, pages_data: List[Dict[str, Any]]) -> int:
        """
        Determines the exact page containing the excerpt.
        """
        if not pages_data:
            return 1

        norm_snippet = EvidenceVerifier.normalize_text(excerpt[:80])

        for page in pages_data:
            p_text = EvidenceVerifier.normalize_text(page.get("text", ""))
            if norm_snippet in p_text or excerpt[:50].lower() in p_text.lower():
                return page.get("page_number", 1)

        return 1

    @staticmethod
    def extract_context(snippet: str, full_normalized_text: str, context_len: int = 150) -> str:
        """
        Extracts surrounding context before and after the snippet.
        """
        pos = full_normalized_text.find(snippet)
        if pos == -1:
            return ""

        start = max(0, pos - context_len)
        end = min(len(full_normalized_text), pos + len(snippet) + context_len)

        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(full_normalized_text) else ""

        return prefix + full_normalized_text[start:end].strip() + suffix
