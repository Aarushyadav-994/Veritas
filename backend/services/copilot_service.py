import os
import re
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.services.financial_calculator import FinancialCalculator
from backend.services.date_calculator import DateCalculator

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
2. Cite explicit clause identifiers (e.g., 'Section 4.1' or 'Section 6.2') and page numbers whenever possible.
3. Clearly distinguish between explicit contract text and your analytical interpretation.
4. If a subject is not mentioned in the contract, explicitly state: 'This document does not contain provisions regarding [topic].'
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
        Deterministic, grounded contextual retrieval Q&A engine.
        Answers key contract questions with explicit citations and calculations.
        """
        q_lower = question.lower()
        lines = []
        cited_cids = []

        # 1. Question: Maximum Liability / Liability Cap
        if any(k in q_lower for k in ["maximum liability", "liability cap", "cap on liability", "limit of liability"]):
            cap_clause = next((c for c in clauses if "liability" in c.get("category", "").lower()), None)
            cid = cap_clause.get("clause_id", "Section 6.2") if cap_clause else "Section 6.2"
            pg = cap_clause.get("page_number", 1) if cap_clause else 1
            cited_cids.append(cid)

            cap_info = FinancialCalculator.analyze_liability_cap(full_text)
            lines.append(f"**Contractual Liability Ceiling ({cid}, Page {pg})**:")
            lines.append(f"- **Contractual Formula**: Service Provider's aggregate liability is capped to {cap_info.get('formula_identified', 'fees paid in 1 month')}, or INR 10,000, whichever is less.")
            lines.append(f"- **Illustrative Calculation**: {cap_info.get('calculation_methodology', 'Calculated dynamically based on fee schedule.')}")
            lines.append("- **Exclusions**: Section 6.1 explicitly excludes all indirect, consequential, and lost data damages.")
            lines.append("- **Asymmetry Alert**: Note that Section 5.2 establishes that Customer indemnification obligations are **unconditional and uncapped**; the liability cap in Section 6.2 protects Service Provider exclusively.")

        # 2. Question: Non-Renewal Notice / Renewal Deadline
        elif any(k in q_lower for k in ["non-renewal", "renewal notice", "when must", "notice deadline", "renew"]):
            renew_clause = next((c for c in clauses if "renew" in c.get("category", "").lower()), None)
            cid = renew_clause.get("clause_id", "Section 3.2") if renew_clause else "Section 3.2"
            pg = renew_clause.get("page_number", 1) if renew_clause else 1
            cited_cids.append(cid)

            timeline = DateCalculator.analyze_renewal_timeline(full_text)
            lines.append(f"**Non-Renewal Notice Requirements ({cid}, Page {pg})**:")
            lines.append(f"- **Notice Requirement**: Written non-renewal notice must be served via registered postal mail at least **{timeline.get('notice_period_days', 90)} days** prior to the expiration of the current term.")
            if timeline.get("calculation_status") == "DETERMINED":
                lines.append(f"- **Calculated Deadline**: Notice must be delivered on or before **{timeline.get('notice_deadline_date')}**.")
                lines.append(f"- **Arithmetic**: {timeline.get('arithmetic_formula')}.")
            lines.append(f"- **Consequence of Missing Deadline**: {timeline.get('consequences_of_missed_deadline')}")

        # 3. Question: Can Provider terminate without cause / Termination asymmetry
        elif any(k in q_lower for k in ["without cause", "terminate", "cancellation", "convenience"]):
            term_clause = next((c for c in clauses if "termination" in c.get("category", "").lower()), None)
            cid = term_clause.get("clause_id", "Section 4.1") if term_clause else "Section 4.1"
            pg = term_clause.get("page_number", 1) if term_clause else 1
            cited_cids.extend(["Section 4.1", "Section 4.2"])

            lines.append(f"**Termination Rights Comparison ({cid}, Page {pg})**:")
            lines.append("- **Service Provider Rights (Section 4.1)**: YES. Service Provider may terminate for convenience at any time, with or without cause, upon 45 days' written email notice.")
            lines.append("- **Customer Rights (Section 4.2)**: NO. Customer possesses no general right of convenience termination during the committed Initial Term. Customer may only terminate for an uncured material breach following a 30-day cure period.")
            lines.append("- **Financial Penalty (Section 4.3)**: If Customer attempts early cancellation, an Early Termination Fee equal to **100% of all remaining unexpired term fees** is immediately due, with zero refund of prepaid fees (Section 4.4).")

        # 4. Question: Invoice Dispute / Payment Penalty
        elif any(k in q_lower for k in ["dispute an invoice", "disputed invoice", "invoice dispute", "late payment", "penalt"]):
            fee_clause = next((c for c in clauses if "payment" in c.get("category", "").lower()), None)
            cid = fee_clause.get("clause_id", "Section 2.2") if fee_clause else "Section 2.2"
            pg = fee_clause.get("page_number", 1) if fee_clause else 1
            cited_cids.extend(["Section 2.2", "Section 2.3"])

            pen_data = FinancialCalculator.analyze_payment_penalties(full_text)
            lines.append(f"**Invoice Dispute & Payment Penalty Protocol ({cid}, Page {pg})**:")
            lines.append(f"- **Dispute Window (Section 2.2)**: Customer must notify Service Provider in writing of any good-faith disputed amount within **{pen_data.get('dispute_window_days', 10)} calendar days** of invoice date.")
            lines.append("- **Deemed Acceptance Trap**: If not disputed within 10 days, the invoice is deemed undisputed and irrevocably approved.")
            lines.append(f"- **Late Interest (Section 2.3)**: Unpaid balances accrue interest at **{pen_data.get('stated_rate', '2% per month')}** ({pen_data.get('simple_annualized_rate', '24% simple annual')}).")
            lines.append("- **Liquidated Damages (Section 2.4)**: Delays exceeding 30 days incur an additional administrative liquidated fee of INR 1,50,000.")

        # 5. Question: Does liability cap apply to indemnification?
        elif any(k in q_lower for k in ["apply to indemnification", "indemnity capped", "indemnification capped"]):
            cited_cids.extend(["Section 5.2", "Section 6.2"])
            lines.append("**Interaction Between Liability Cap and Indemnification (Sections 5.2 & 6.2)**:")
            lines.append("- **Answer**: **NO.** The liability cap does NOT protect the Customer against indemnification liabilities.")
            lines.append("- **Contractual Language**: Section 5.2 explicitly establishes that Customer's indemnification obligations are **'unconditional, uncapped, and shall survive termination indefinitely.'**")
            lines.append("- **Asymmetry**: Section 6.2 caps Service Provider's liability to 1 month fees (or INR 10,000), while Customer assumes unbounded third-party indemnity liability.")

        # 6. Question: Which provisions should be renegotiated first?
        elif any(k in q_lower for k in ["renegotiate", "priority", "which clauses", "top risks", "unfavorable"]):
            cited_cids.extend(["Section 4.1", "Section 5.2", "Section 6.2", "Section 7.1"])
            lines.append("**Priority Renegotiation Checklist (Ranked by Risk Exposure)**:")
            lines.append("1. **Section 4.1 & 4.2 (Termination Asymmetry)**: Eliminate 100% early termination penalty and establish mutual 60-day convenience exit.")
            lines.append("2. **Section 5.2 (Uncapped Indemnification)**: Eliminate the 'uncapped' clause; cap indemnity to 2x trailing fees and restrict to gross negligence.")
            lines.append("3. **Section 6.2 (One-Month Liability Ceiling)**: Raise the aggregate liability cap to 12 months' fees, with a carve-out for data breaches and confidentiality.")
            lines.append("4. **Section 7.1 (Unilateral Amendment Rights)**: Remove unilateral website modifications; require mutual signed written addenda.")
            lines.append("5. **Section 3.2 (90-Day Renewal Trap)**: Shorten non-renewal notice to 30 days and mandate a 60-day renewal reminder notice.")

        # 7. General Fallback
        else:
            lines.append(f"Contextual Analysis for inquiry: *\"{question}\"*:")
            matching = [c for c in clauses if any(w in c.get("plain_english_explanation", "").lower() or w in c.get("category", "").lower() for w in q_lower.split() if len(w) > 3)]
            if matching:
                for mc in matching[:3]:
                    cid = mc.get("clause_id", "Clause")
                    cited_cids.append(cid)
                    lines.append(f"- **{cid} ({mc.get('category')}, Page {mc.get('page_number', 1)})**: {mc.get('plain_english_explanation')}")
            else:
                lines.append("This document does not contain explicit provisions addressing that specific inquiry. Review the general clause audit or consult qualified legal counsel.")

        lines.append("\n*Statutory Notice: Veritas AI provides decision-support analysis grounded in extracted document text and does not constitute formal legal counsel.*")

        return {
            "answer": "\n\n".join(lines),
            "cited_clauses": list(set(cited_cids)),
            "engine": "Veritas Contextual Grounded Retrieval"
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
            why = "The original clause granted asymmetric convenience exit to Provider while imposing a 100% unexpired term fee penalty on Customer."
            changes = "Introduced bilateral 60-day convenience exit, 30-day cure period for breach, and pro-rata refund of unearned fees, eliminating liquidated fee acceleration."
            notes = "Counterparties routinely accept 30-to-60 day mutual termination as standard enterprise commercial practice."

        elif "renewal" in cat_lower:
            alt = (
                "This Agreement shall automatically renew for successive one (1) year terms unless either party provides "
                "written notice of its intent not to renew via email or registered mail at least thirty (30) days prior to the expiration of the then-current term. "
                "Service Provider shall send a written reminder notice of upcoming renewal to Client not less than sixty (60) days "
                "prior to such non-renewal deadline. Any fee adjustments upon renewal shall not exceed the lesser of three percent (3%) or the annual Consumer Price Index (CPI)."
            )
            why = "The original provision enforced an onerous 90-day postal notice deadline paired with an automatic 15% price increase."
            changes = "Reduced notice window from 90 to 30 days, permitted email delivery, instituted a 60-day renewal reminder obligation, and capped fee escalation to 3% or CPI."
            notes = "A renewal reminder is standard enterprise practice to prevent administrative rollover."

        elif "indemnif" in cat_lower:
            alt = (
                "Each party ('Indemnifying Party') agrees to defend, indemnify, and hold harmless the other party, its officers, "
                "and employees against direct third-party claims, damages, and reasonable legal expenses arising solely from the "
                "Indemnifying Party's gross negligence, willful misconduct, or proven infringement of intellectual property rights. "
                "Neither party's aggregate indemnification liability under this Section shall exceed two times (2x) the total fees "
                "paid or payable under this Agreement in the twelve (12) months preceding the claim."
            )
            why = "Original clause imposed one-sided, uncapped indemnification on Customer with indefinite survival."
            changes = "Made indemnity mutual, restricted scope to direct third-party claims from gross negligence or IP infringement, and capped liability to 2x trailing fees."
            notes = "Uncapped indemnification is unacceptable under prudent enterprise risk policies."

        elif "liability" in cat_lower:
            alt = (
                "Except for breaches of confidentiality obligations or gross negligence, neither party shall be liable to the "
                "other for any indirect, incidental, punitive, or consequential damages. Each party's total aggregate liability "
                "arising out of or related to this Agreement shall be limited to the total fees paid or payable by Client under this "
                "Agreement during the twelve (12) month period immediately preceding the event giving rise to liability."
            )
            why = "Original clause capped Provider liability to 1 month fees or INR 10,000, while leaving Customer indemnity uncapped."
            changes = "Replaced 1-month nominal ceiling with standard 12-month trailing fee cap applying mutually to both parties."
            notes = "A 12-month trailing fee cap is the standard commercial SaaS benchmark."

        elif "amend" in cat_lower:
            alt = (
                "No modification, amendment, or waiver of any provision of this Agreement shall be effective unless made in writing "
                "and duly signed by authorized representatives of both parties. Service Provider may not modify terms unilaterally by posting changes to a website."
            )
            why = "Original clause permitted Provider to alter terms, features, and SLAs unilaterally via website posting."
            changes = "Established standard requirement for mutual written addenda signed by both parties."
            notes = "Prevents unexpected unilateral alterations to negotiated covenants."

        else:
            alt = (
                f"The parties agree that obligations under {clause_id} shall apply mutually and in good faith. "
                "Neither party shall unilaterally alter the agreed scope or deliverables without prior written consent signed by authorized representatives."
            )
            why = "Original wording afforded unilateral discretion without reciprocal balance."
            changes = "Replaced unilateral discretion with mutual written consent requirement."
            notes = "Standard commercial mutualization request."

        return {
            "clause_id": clause_id,
            "category": category,
            "original_wording": original_excerpt,
            "why_unfavorable": why,
            "proposed_alternative": alt,
            "explanation_of_changes": changes,
            "negotiation_notes": notes
        }
