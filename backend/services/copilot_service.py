import os
import re
from typing import Dict, Any, List, Optional
from backend.config import settings

class CopilotService:
    @staticmethod
    def answer_question(
        question: str,
        full_text: str,
        clauses: List[Dict[str, Any]],
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answers user legal questions strictly grounded in the document text and analyzed clauses.
        Cites specific clause IDs and pages.
        """
        # Try Gemini if key is provided
        if settings.gemini_api_key and settings.gemini_api_key.strip():
            try:
                return CopilotService._answer_with_gemini(question, full_text, clauses)
            except Exception as e:
                print(f"[CopilotService] Gemini API call failed: {str(e)}. Using grounded fallback engine.")

        # Grounded heuristic retrieval answer
        return CopilotService._answer_grounded(question, full_text, clauses)

    @staticmethod
    def _answer_with_gemini(question: str, full_text: str, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)

        clauses_summary = "\n".join([
            f"- [{c.get('clause_id', 'Clause')}] (Page {c.get('page_number', 1)}) ({c.get('category', 'General')} - {c.get('risk_level', 'REVIEW')}): {c.get('plain_english_explanation', '')}"
            for c in clauses[:20]
        ])

        system_instruction = f"""
You are the Veritas AI Contextual Legal Copilot.
You assist users in understanding their specific uploaded legal contract.

RULES:
1. Base all answers strictly on the provided contract text and clauses.
2. Cite explicit clause identifiers (e.g., 'Clause 4.2' or 'Section 7') and page numbers whenever possible.
3. Clearly distinguish between explicit contract text and your analytical interpretation.
4. If a subject (e.g. governing law, IP ownership, non-compete) is not mentioned in the contract, explicitly state: 'This document does not contain provisions regarding [topic].'
5. Do NOT invent legal statutes or make definitive guarantees of legal enforceability.
6. Provide clear, objective, professional answers.

DOCUMENT SUMMARY & CLAUSES:
{clauses_summary}

FULL DOCUMENT EXCERPT:
\"\"\"
{full_text[:35000]}
\"\"\"
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=f"{system_instruction}\n\nUSER QUESTION: {question}"
        )

        # Extract cited clauses
        cited_clauses = []
        for c in clauses:
            cid = c.get("clause_id", "")
            if cid and cid.lower() in response.text.lower():
                cited_clauses.append(cid)

        return {
            "answer": response.text,
            "cited_clauses": cited_clauses,
            "engine": f"Google Gemini ({settings.gemini_model})"
        }

    @staticmethod
    def _answer_grounded(question: str, full_text: str, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Deterministic, grounded contextual retrieval Q&A engine for offline/unconfigured environments.
        """
        q_lower = question.lower()
        matched_clauses = []

        # Keyword mapping to contract topics
        topic_map = {
            "financial": ["payment", "fee", "penalty", "interest", "invoice", "liquidated"],
            "obligation": ["obligation", "duty", "shall", "must", "deliver", "provide"],
            "terminat": ["termination", "terminate", "cancel", "convenience", "breach"],
            "renew": ["renew", "renewal", "auto-renew", "term", "duration"],
            "penalt": ["penalty", "interest", "damages", "late payment"],
            "unfavorable": ["high risk", "unfavorable", "one-sided", "indemnify", "discretion"],
            "dates": ["effective date", "date", "term", "duration", "timeline"],
            "missing": ["missing", "protection", "omission", "lack", "absent"],
            "liability": ["liability", "limitation of liability", "cap", "consequential", "indemnification"],
            "dispute": ["dispute", "jurisdiction", "court", "arbitration", "governing law"],
            "ip": ["intellectual property", "ownership", "copyright", "trademark", "patent"],
            "confidential": ["confidential", "nda", "disclosure", "trade secret"]
        }

        # Find matching clauses
        relevant_categories = set()
        for topic_key, keywords in topic_map.items():
            if topic_key in q_lower or any(kw in q_lower for kw in keywords):
                for c in clauses:
                    cat = c.get("category", "").lower()
                    expl = c.get("plain_english_explanation", "").lower()
                    exc = c.get("original_excerpt", "").lower()
                    if any(kw in cat or kw in expl or kw in exc for kw in keywords):
                        matched_clauses.append(c)
                        relevant_categories.add(c.get("category"))

        # Deduplicate matched clauses
        unique_clauses = []
        seen_ids = set()
        for mc in matched_clauses:
            cid = mc.get("clause_id", "")
            if cid not in seen_ids:
                seen_ids.add(cid)
                unique_clauses.append(mc)

        if not unique_clauses and clauses:
            # Fallback to high risk clauses
            unique_clauses = [c for c in clauses if c.get("risk_level") == "HIGH RISK"][:3]

        # Construct structured response
        lines = []
        cited_cids = []

        if "terminat" in q_lower:
            term_clauses = [c for c in clauses if c.get("category") == "Termination"]
            if term_clauses:
                tc = term_clauses[0]
                cited_cids.append(tc.get("clause_id"))
                lines.append(f"**Termination Rights ({tc.get('clause_id')}, Page {tc.get('page_number', 1)})**:")
                lines.append(f"- **Document Provision**: {tc.get('original_excerpt')}")
                lines.append(f"- **Key Limitation**: {tc.get('plain_english_explanation')}")
                lines.append(f"- **Operational Impact**: {tc.get('why_it_matters')}")
            else:
                lines.append("The analyzed text does not include an explicit unilateral termination for convenience clause. Termination is governed solely by statutory breach provisions.")

        elif "renew" in q_lower:
            renew_clauses = [c for c in clauses if c.get("category") == "Automatic Renewal"]
            if renew_clauses:
                rc = renew_clauses[0]
                cited_cids.append(rc.get("clause_id"))
                lines.append(f"**Renewal Protocol ({rc.get('clause_id')}, Page {rc.get('page_number', 1)})**:")
                lines.append(f"- **Contractual Mechanism**: {rc.get('original_excerpt')}")
                lines.append(f"- **Analysis**: {rc.get('plain_english_explanation')}")
                lines.append(f"- **Action Required**: {rc.get('suggested_next_step')}")
            else:
                lines.append("No automatic renewal clause was identified in the extracted text.")

        elif "penalt" in q_lower or "financ" in q_lower:
            pay_clauses = [c for c in clauses if c.get("category") in ["Payment & Penalties", "Liability Limitations"]]
            if pay_clauses:
                for pc in pay_clauses[:2]:
                    cited_cids.append(pc.get("clause_id"))
                    lines.append(f"**{pc.get('category')} ({pc.get('clause_id')}, Page {pc.get('page_number', 1)})**:")
                    lines.append(f"- {pc.get('plain_english_explanation')}")
                    lines.append(f"- **Potential Consequence**: {pc.get('potential_consequence')}")
            else:
                lines.append("No unusual punitive financial obligations were extracted from the available text.")

        elif "unfavorable" in q_lower or "risk" in q_lower:
            high_risk = [c for c in clauses if c.get("risk_level") == "HIGH RISK"]
            lines.append(f"Based on analysis of the document, **{len(high_risk)} high-risk provisions** were identified:")
            for hr in high_risk:
                cited_cids.append(hr.get("clause_id"))
                lines.append(f"- **{hr.get('clause_id')} ({hr.get('category')}, Page {hr.get('page_number', 1)})**: {hr.get('plain_english_explanation')}")
                lines.append(f"  *Suggested Action*: {hr.get('suggested_next_step')}")

        else:
            # General synthesis
            lines.append(f"Analysis for query: *\"{question}\"*:")
            if unique_clauses:
                for uc in unique_clauses[:3]:
                    cited_cids.append(uc.get("clause_id"))
                    lines.append(f"- **{uc.get('clause_id')} ({uc.get('category')}, Page {uc.get('page_number', 1)})**: {uc.get('plain_english_explanation')}")
                    lines.append(f"  *Excerpt Reference*: \"{uc.get('original_excerpt')[:180]}...\"")
            else:
                lines.append("No specific clauses matching this inquiry were identified in the extracted text. Please review the clause breakdown or consult qualified legal counsel.")

        lines.append("\n*Disclaimer: Veritas AI answers are intended for decision-support and do not constitute formal legal advice.*")

        return {
            "answer": "\n\n".join(lines),
            "cited_clauses": cited_cids,
            "engine": "Veritas Contextual Semantic Grounding (Deterministic)"
        }

    @staticmethod
    def redraft_clause(
        clause_id: str,
        category: str,
        original_excerpt: str,
        negotiation_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates balanced, commercially reasonable alternative wording for an unfavorable clause.
        """
        # Try Gemini if key is provided
        if settings.gemini_api_key and settings.gemini_api_key.strip():
            try:
                return CopilotService._redraft_with_gemini(clause_id, category, original_excerpt, negotiation_goal)
            except Exception as e:
                print(f"[CopilotService] Gemini redraft failed: {str(e)}. Using standard redraft templates.")

        return CopilotService._redraft_heuristic(clause_id, category, original_excerpt, negotiation_goal)

    @staticmethod
    def _redraft_with_gemini(
        clause_id: str,
        category: str,
        original_excerpt: str,
        negotiation_goal: Optional[str]
    ) -> Dict[str, Any]:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)

        prompt = f"""
You are a senior contract attorney drafting a fair, bilateral negotiation counter-proposal.

TARGET CLAUSE:
Clause Identifier: {clause_id}
Category: {category}
Original Excerpt:
\"\"\"
{original_excerpt}
\"\"\"

USER NEGOTIATION GOAL:
{negotiation_goal or "Make the clause mutually balanced, introduce reasonable notice/cure periods, and cap exposure."}

Provide a response in strict JSON:
{{
  "clause_id": "{clause_id}",
  "category": "{category}",
  "original_wording": "{original_excerpt[:300]}",
  "why_unfavorable": "string explaining the risk of the original wording",
  "proposed_alternative": "string containing complete, professional contract clause language ready for insertion",
  "explanation_of_changes": "string detailing what rights were balanced or added",
  "negotiation_notes": "string giving tactical advice on how to present this to the counterparty"
}}
Return ONLY valid JSON.
"""
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        import json
        return json.loads(response.text)

    @staticmethod
    def _redraft_heuristic(
        clause_id: str,
        category: str,
        original_excerpt: str,
        negotiation_goal: Optional[str]
    ) -> Dict[str, Any]:
        cat_lower = category.lower()

        if "termination" in cat_lower:
            alt = (
                "Either party may terminate this Agreement for convenience at any time upon sixty (60) days' "
                "prior written notice to the other party. In the event of an alleged material breach, the non-breaching "
                "party shall provide detailed written notice thereof, and the breaching party shall be afforded thirty (30) "
                "days from receipt of such notice to cure said breach. Upon termination, Client shall only be liable for "
                "documented fees earned for services rendered prior to the effective termination date, and any unused prepaid "
                "fees shall be refunded on a pro-rata basis within fifteen (15) business days."
            )
            why = "The original clause granted asymmetric exit rights, penalty forfeitures, or lacked a mandatory cure period."
            changes = "Introduced bilateral 60-day notice, mandatory 30-day cure period for breach, and fair pro-rata refund of prepaid fees."
            notes = "Counterparties routinely accept 30-to-60 day mutual termination as standard enterprise commercial practice."

        elif "renewal" in cat_lower:
            alt = (
                "This Agreement shall automatically renew for successive one (1) year terms unless either party provides "
                "written notice of its intent not to renew at least thirty (30) days prior to the expiration of the then-current term. "
                "Service Provider shall send a written reminder notice of upcoming renewal to Client not less than forty-five (45) days "
                "prior to such non-renewal deadline. Any fee adjustments upon renewal shall not exceed the lesser of 3% or the annual Consumer Price Index (CPI)."
            )
            why = "The original term locked parties into renewal with excessively long advance notice or unconstrained price hikes."
            changes = "Shortened notice window to 30 days, added provider reminder obligation at 45 days, and instituted an annual price adjustment ceiling."
            notes = "Emphasize that a renewal reminder is necessary to prevent inadvertent administrative rollover."

        elif "indemnif" in cat_lower:
            alt = (
                "Each party ('Indemnifying Party') agrees to defend, indemnify, and hold harmless the other party, its officers, "
                "and employees against direct third-party claims, damages, and reasonable legal expenses arising solely from the "
                "Indemnifying Party's gross negligence, willful misconduct, or proven infringement of intellectual property rights. "
                "Neither party's aggregate indemnification liability under this Section shall exceed two times (2x) the total fees "
                "paid or payable under this Agreement in the twelve (12) months preceding the incident."
            )
            why = "The original provision created one-sided, uncapped indemnification for broad third-party liabilities."
            changes = "Made indemnity mutual, restricted scope to direct third-party claims arising from gross negligence or IP infringement, and capped liability at 2x annual contract value."
            notes = "Uncapped indemnification is unacceptable under standard risk management policies."

        elif "liability" in cat_lower:
            alt = (
                "Except for breaches of confidentiality obligations or gross negligence, neither party shall be liable to the "
                "other for any indirect, incidental, punitive, or consequential damages, including loss of profits. Each party's "
                "total aggregate liability arising out of or related to this Agreement shall be limited to the total fees paid or "
                "payable by Client under this Agreement during the twelve (12) month period immediately preceding the event giving rise to liability."
            )
            why = "Original clause severely capped provider liability to nominal sums while leaving your liability unrestricted."
            changes = "Created mutual aggregate liability ceiling tied to 12 months' trailing contract fees, with standard mutual waiver of consequential damages."
            notes = "A 12-month trailing fee cap is the recognized industry standard for commercial SaaS and services agreements."

        else:
            alt = (
                f"The parties agree that obligations under {clause_id} shall apply mutually and in good faith. "
                "Neither party shall unilaterally alter the agreed scope, deliverables, or operational standards without prior written consent signed by authorized representatives of both parties."
            )
            why = "Original wording afforded unilateral discretion without reciprocal balance."
            changes = "Replaced unilateral discretion with mutual written consent requirement."
            notes = "Standard mutualization request."

        return {
            "clause_id": clause_id,
            "category": category,
            "original_wording": original_excerpt,
            "why_unfavorable": why,
            "proposed_alternative": alt,
            "explanation_of_changes": changes,
            "negotiation_notes": notes
        }
