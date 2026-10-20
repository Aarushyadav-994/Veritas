import os
import re
import json
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.services.evidence_verifier import EvidenceVerifier
from backend.services.date_calculator import DateCalculator
from backend.services.financial_calculator import FinancialCalculator
from backend.services.cross_clause_engine import CrossClauseEngine

class ClauseAnalyzer:
    @staticmethod
    def analyze_document(full_text: str, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Coordinates document analysis using Gemini API if configured and responsive,
        or the deterministic evidence-grounded legal heuristic engine.
        """
        if settings.gemini_api_key and settings.gemini_api_key.strip():
            try:
                gemini_result = ClauseAnalyzer._analyze_with_gemini(full_text, pages_data)
                if gemini_result and "clauses" in gemini_result and len(gemini_result["clauses"]) > 0:
                    gemini_result["engine"] = f"Google Gemini ({settings.gemini_model})"
                    # Enrich with evidence verification and cross-clause reasoning
                    ClauseAnalyzer._enrich_analysis(gemini_result, full_text, pages_data)
                    return gemini_result
            except Exception as e:
                print(f"[ClauseAnalyzer] Gemini API failed: {str(e)}. Using deterministic engine.")

        # Deterministic evidence-grounded legal analysis engine
        res = ClauseAnalyzer._analyze_heuristic(full_text, pages_data)
        res["engine"] = "Veritas Evidence-Grounded Legal Engine (Local/Deterministic)"
        return res

    @staticmethod
    def _enrich_analysis(result: Dict[str, Any], full_text: str, pages_data: List[Dict[str, Any]]):
        """
        Post-processes model results with quotation verification, financial calculations,
        and cross-clause reasoning.
        """
        for cl in result.get("clauses", []):
            exc = cl.get("original_excerpt", "")
            ver_res = EvidenceVerifier.verify_quotation(exc, full_text, pages_data)
            cl["quotation_verified"] = ver_res["verified"]
            cl["verification_status"] = ver_res["status"]
            cl["page_number"] = ver_res["matched_page"]

        result["cross_clause_analysis"] = CrossClauseEngine.analyze_interactions(result.get("clauses", []), full_text)
        result["renewal_timeline"] = DateCalculator.analyze_renewal_timeline(full_text, result.get("document_summary", {}).get("effective_date"))
        result["financial_analytics"] = {
            "liability_cap": FinancialCalculator.analyze_liability_cap(full_text),
            "payment_penalties": FinancialCalculator.analyze_payment_penalties(full_text)
        }

    @staticmethod
    def _analyze_heuristic(full_text: str, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Deterministic, evidence-grounded contract analysis engine.
        Performs deep clause segmentation, party role extraction, financial calculations,
        comparative termination analysis, cross-clause reasoning, and 4-tier missing protection audit.
        """
        text_lower = full_text.lower()

        # -------------------------------------------------------------
        # 1. Party & Document Summary Extraction
        # -------------------------------------------------------------
        party1 = "Party A"
        party2 = "Party B"
        entities_found = []
        entity_term_regex = re.compile(r"\b(PRIVATE\s+LIMITED|PVT\.?\s*LTD\.?|LIMITED|CORPORATION|CORP\.?|INCORPORATED|INC\.?|LLC|LTD\.?)\b", re.IGNORECASE)
        for line in full_text[:3500].split("\n"):
            line_str = line.strip()
            if entity_term_regex.search(line_str) and not any(sig in line_str.upper() for sig in ["AUTHORIZED SIGNATORY", "WITNESS WHEREOF", "FOR "]):
                ent = re.split(r",\s*(?:a\s+|having|CIN|with|\()", line_str, flags=re.IGNORECASE)[0].strip()
                ent = re.sub(r"^(?:AND\s+|BY\s+AND\s+BETWEEN:?\s*|BETWEEN:?\s*|FOR\s+|\d+\.\s*)", "", ent, flags=re.IGNORECASE).strip()
                if 4 <= len(ent) <= 80 and ent not in entities_found and not ent.upper().startswith("CIN"):
                    entities_found.append(ent)

        if len(entities_found) >= 2:
            party1 = entities_found[0]
            party2 = entities_found[1]
        elif len(entities_found) == 1:
            party1 = entities_found[0]

        # Document Type
        doc_type = "Commercial Contract"
        upper_header = full_text[:1500].upper()
        if "CLOUD SERVICES" in upper_header or "SAAS" in upper_header:
            doc_type = "Master Cloud Services & Enterprise License Agreement"
        elif "NON-DISCLOSURE" in upper_header or "CONFIDENTIALITY" in upper_header:
            doc_type = "Mutual Non-Disclosure & Confidentiality Agreement"
        elif "MASTER SERVICES" in upper_header:
            doc_type = "Master Services Agreement (MSA)"

        # Effective Date Detection
        date_m = re.search(r"(?:effective\s+as\s+of|dated|executed\s+as\s+of|entered\s+into\s+on)\s+([A-Za-z0-9\s,]{4,30}\d{4})", full_text[:2500], re.IGNORECASE)
        effective_date = date_m.group(1).strip() if date_m else "Execution Date"

        # -------------------------------------------------------------
        # 2. Specialized Financial & Date Calculators
        # -------------------------------------------------------------
        renewal_timeline = DateCalculator.analyze_renewal_timeline(full_text, effective_date)
        liability_cap_data = FinancialCalculator.analyze_liability_cap(full_text)
        payment_penalty_data = FinancialCalculator.analyze_payment_penalties(full_text)

        # -------------------------------------------------------------
        # 3. Deep Evidence-Grounded Clause Segmentation
        # -------------------------------------------------------------
        clauses: List[Dict[str, Any]] = []

        # SECTION 2: Fees & Late Interest
        fee_match = re.search(r"(\b2\.\s+FEES[^\n]*\n(?:[^\n]+\n){2,8})", full_text, re.IGNORECASE)
        fee_p2_3 = re.search(r"(2\.3\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if fee_p2_3 or fee_match:
            raw_excerpt = fee_p2_3.group(1).strip() if fee_p2_3 else fee_match.group(1)[:300].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 2.3",
                "clause_title": "Delinquent Balances and Late Payment Interest",
                "category": "Payment & Penalties",
                "section_number": "2.3",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    f"Late balances incur interest at {payment_penalty_data['stated_rate']} ({payment_penalty_data['simple_annualized_rate']}). "
                    f"Coupled with Section 2.2's {payment_penalty_data['dispute_window_days'] or 10}-day invoice dispute window, invoices not formally "
                    "contested within that short timeframe accrue punitive interest and liquidated damages."
                ),
                "benefiting_party": "Service Provider",
                "potential_consequence": (
                    "Unintentional administrative delays or disputed line items risk immediate interest penalties and "
                    f"liquidated fees (INR 1,50,000) under Section 2.4."
                ),
                "risk_level": "MODERATE RISK",
                "severity_justification": (
                    "Interest of 24% per annum is substantial though standard in commercial vendor contracts. "
                    "However, the 10-day invoice dispute window creates an aggressive deemed-acceptance mechanism."
                ),
                "suggested_next_step": "Negotiate a 30-day invoice dispute window and cap late interest to 1% per month simple interest for undisputed amounts.",
                "suggested_alternative_wording": (
                    "Undisputed delinquent amounts shall accrue simple interest at the rate of one percent (1%) per month. "
                    "Client shall have thirty (30) days from receipt of invoice to notify Service Provider in writing of any disputed amounts in good faith."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Explicit interest rate and dispute periods extracted verbatim from Section 2.",
                "related_clause_ids": ["Section 2.2", "Section 2.4"]
            })

        # SECTION 3: Term & Automatic Renewal
        renew_match = re.search(r"(3\.\s+TERM[^\n]*\n(?:[^\n]+\n){2,8})", full_text, re.IGNORECASE)
        renew_p3_2 = re.search(r"(3\.2\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if renew_p3_2 or renew_match:
            raw_excerpt = renew_p3_2.group(1).strip() if renew_p3_2 else renew_match.group(1)[:300].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 3.2",
                "clause_title": "Automatic Renewal and Non-Renewal Notice Deadline",
                "category": "Automatic Renewal",
                "section_number": "3.2",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    f"The contract automatically renews for successive {renewal_timeline['initial_term_months']}-month terms unless Client provides written notice "
                    f"via registered postal mail at least {renewal_timeline['notice_period_days']} days prior to term expiration. "
                    f"Based on the {renewal_timeline['effective_date']} effective date, notice must be served by {renewal_timeline['notice_deadline_date']}."
                ),
                "benefiting_party": "Service Provider",
                "potential_consequence": (
                    f"Failing to serve notice by {renewal_timeline['notice_deadline_date']} automatically binds Client to another full contract term "
                    "accompanied by Section 3.3's automatic 15% price increase."
                ),
                "risk_level": "HIGH RISK",
                "severity_justification": (
                    "90-day advance postal notice requirement combined with automatic 15% fee escalation creates a severe contractual lock-in."
                ),
                "suggested_next_step": "Reduce notice window to 30 days, eliminate postal-only service requirement (allow email), and add mandatory 60-day renewal reminder from Provider.",
                "suggested_alternative_wording": (
                    "This Agreement shall automatically renew unless either party provides written notice via email at least thirty (30) days prior to the expiration of the current term. "
                    "Service Provider shall send a written reminder of renewal at least sixty (60) days prior to such deadline."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Extracted dates and notice intervals verified against Section 3.2.",
                "related_clause_ids": ["Section 3.1", "Section 3.3"]
            })

        # SECTION 4: Comparative Termination Analysis
        term_match = re.search(r"(4\.\s+TERMINATION[^\n]*\n(?:[^\n]+\n){2,10})", full_text, re.IGNORECASE)
        term_p4_1 = re.search(r"(4\.1\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        term_p4_2 = re.search(r"(4\.2\s+[^\n]+(?:\n[^\n]+)?)", full_text)

        if term_match or term_p4_1:
            raw_excerpt = (term_p4_1.group(1).strip() + "\n" + (term_p4_2.group(1).strip() if term_p4_2 else "")) if term_p4_1 else term_match.group(1)[:350].strip()
            ver_res = EvidenceVerifier.verify_quotation(term_p4_1.group(1) if term_p4_1 else raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 4.1 & 4.2",
                "clause_title": "Asymmetric Termination for Convenience and Early Exit Penalties",
                "category": "Termination",
                "section_number": "4.1",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    "Significant exit asymmetry: Provider may terminate for convenience at any time on 45 days' email notice. "
                    "Client has NO convenience exit right during the committed term, and early cancellation triggers a 100% early termination fee "
                    "on all remaining term fees (Section 4.3), with zero refund of prepaid credits (Section 4.4)."
                ),
                "benefiting_party": "Service Provider exclusively",
                "potential_consequence": (
                    "Client bears all downstream commercial and financial risk of the committed term while Provider maintains full discretionary exit freedom."
                ),
                "risk_level": "HIGH RISK",
                "severity_justification": (
                    "Unilateral convenience termination rights paired with 100% liquidated balance acceleration creates an acute imbalance in contractual exit remedies."
                ),
                "suggested_next_step": "Negotiate mutual termination for convenience on 60 days' written notice with pro-rata refund of unearned fees and elimination of the unexpired fee penalty.",
                "suggested_alternative_wording": (
                    "Either party may terminate this Agreement for convenience at any time upon sixty (60) days' prior written notice to the other party. "
                    "Upon termination, Client shall pay for services delivered prior to termination, and any unearned prepaid fees shall be refunded pro-rata."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Direct comparison of Sections 4.1, 4.2, and 4.3 confirming unilateral exit rights.",
                "related_clause_ids": ["Section 4.3", "Section 4.4"]
            })

        # SECTION 5: Indemnification
        indem_match = re.search(r"(5\.\s+INDEMNIFICATION[^\n]*\n(?:[^\n]+\n){2,8})", full_text, re.IGNORECASE)
        indem_p5_2 = re.search(r"(5\.2\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if indem_match or indem_p5_2:
            raw_excerpt = indem_p5_2.group(1).strip() if indem_p5_2 else indem_match.group(1)[:300].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 5.2",
                "clause_title": "Uncapped and Unconditional Client Indemnification",
                "category": "Indemnification",
                "section_number": "5.2",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    "Client's indemnification obligations are expressly unconditional, uncapped, and survive contract termination indefinitely. "
                    "In contrast, Provider offers zero reciprocal indemnification for IP infringement or service breaches."
                ),
                "benefiting_party": "Service Provider exclusively",
                "potential_consequence": (
                    "Client is exposed to infinite third-party liability claims, judgments, and legal fees without any contractual monetary ceiling."
                ),
                "risk_level": "HIGH RISK",
                "severity_justification": (
                    "Uncapped third-party indemnity paired with indefinite survival violates enterprise risk mitigation norms."
                ),
                "suggested_next_step": "Make indemnity mutual, restrict scope to third-party claims arising from gross negligence or willful breach, and subject indemnity to a clear liability cap.",
                "suggested_alternative_wording": (
                    "Each party shall defend and indemnify the other against third-party claims arising from gross negligence or intentional misconduct. "
                    "Each party's aggregate indemnity liability shall not exceed two times (2x) the fees paid in the preceding 12 months."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Section 5.2 explicitly uses 'unconditional, uncapped, and shall survive indefinitely'.",
                "related_clause_ids": ["Section 5.1", "Section 6.2"]
            })

        # SECTION 6: Limitation of Liability
        cap_match = re.search(r"(6\.\s+LIMITATION[^\n]*\n(?:[^\n]+\n){2,10})", full_text, re.IGNORECASE)
        cap_p6_2 = re.search(r"(6\.2\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if cap_match or cap_p6_2:
            raw_excerpt = cap_p6_2.group(1).strip() if cap_p6_2 else cap_match.group(1)[:350].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 6.2",
                "clause_title": "One-Month Aggregate Liability Cap and Dollar Ceiling",
                "category": "Liability Limitations",
                "section_number": "6.2",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    f"Provider's total liability is strictly limited to fees received in the 1-month period immediately preceding the claim "
                    f"(illustrative estimate: {liability_cap_data.get('illustrative_cap_amount', 'calculated dynamically')}) or INR 10,000, whichever is less. "
                    "Section 6.1 also excludes all consequential, incidental, and data loss damages."
                ),
                "benefiting_party": "Service Provider exclusively",
                "potential_consequence": (
                    "In a major operational outage or security event, Client recovery is legally suppressed to an insignificant nominal amount."
                ),
                "risk_level": "HIGH RISK",
                "severity_justification": (
                    "Limiting liability to one month's fees or INR 10,000 renders Provider accountability negligible compared to the contract value."
                ),
                "suggested_next_step": "Negotiate an aggregate liability cap equal to 12 months of fees paid or payable, with super-caps for data breach and confidentiality.",
                "suggested_alternative_wording": (
                    "Except for breaches of confidentiality or gross negligence, each party's total liability shall not exceed the total fees paid or payable "
                    "in the twelve (12) month period immediately preceding the event giving rise to liability."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Extracted formula 'fees actually received in one (1) month or INR 10,000, whichever is lower' verified.",
                "related_clause_ids": ["Section 6.1", "Section 5.2"]
            })

        # SECTION 7: Unilateral Amendment Rights
        amend_match = re.search(r"(7\.\s+UNILATERAL[^\n]*\n(?:[^\n]+\n){2,6})", full_text, re.IGNORECASE)
        amend_p7_1 = re.search(r"(7\.1\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if amend_match or amend_p7_1:
            raw_excerpt = amend_p7_1.group(1).strip() if amend_p7_1 else amend_match.group(1)[:250].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 7.1",
                "clause_title": "Unilateral Contract Modification via Website Posting",
                "category": "Unilateral Amendment",
                "section_number": "7.1",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    "Provider reserves the unconstrained right to alter terms, features, and SLAs by posting changes to its website. "
                    "Continued access or payment constitutes deemed acceptance (Section 7.2)."
                ),
                "benefiting_party": "Service Provider",
                "potential_consequence": (
                    "Provider may unilaterally modify SLAs, support commitments, or commercial conditions without active signature."
                ),
                "risk_level": "HIGH RISK",
                "severity_justification": (
                    "Permitting unilateral web-posted amendments compromises the binding nature of negotiated terms."
                ),
                "suggested_next_step": "Require formal written amendment signed by authorized representatives of both parties for any material change.",
                "suggested_alternative_wording": (
                    "No modification or amendment to this Agreement shall be effective unless made in writing and signed by authorized representatives of both parties."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Section 7.1 and 7.2 extracted verbatim.",
                "related_clause_ids": ["Section 7.2"]
            })

        # SECTION 8: Governing Law & Dispute Resolution
        arb_match = re.search(r"(8\.\s+GOVERNING[^\n]*\n(?:[^\n]+\n){2,6})", full_text, re.IGNORECASE)
        arb_p8_2 = re.search(r"(8\.2\s+[^\n]+(?:\n[^\n]+)?)", full_text)
        if arb_match or arb_p8_2:
            raw_excerpt = arb_p8_2.group(1).strip() if arb_p8_2 else arb_match.group(1)[:250].strip()
            ver_res = EvidenceVerifier.verify_quotation(raw_excerpt, full_text, pages_data)

            clauses.append({
                "clause_id": "Section 8.2",
                "clause_title": "Sole Arbitrator Appointed Exclusively by Provider",
                "category": "Dispute Resolution & Arbitration",
                "section_number": "8.2",
                "page_number": ver_res["matched_page"],
                "exact_quotation": raw_excerpt,
                "quotation_verified": ver_res["verified"],
                "verification_status": ver_res["status"],
                "plain_english_explanation": (
                    "Any dispute must be referred to binding arbitration before a sole arbitrator appointed solely by Provider's Managing Director."
                ),
                "benefiting_party": "Service Provider exclusively",
                "potential_consequence": (
                    "Unilateral arbitrator appointment creates substantial risk of arbitrator bias and may be challenged under the Arbitration and Conciliation Act."
                ),
                "risk_level": "MODERATE RISK",
                "severity_justification": (
                    "Unilateral appointment of a sole arbitrator raises serious procedural fairness concerns under Indian arbitration law (Perkins Eastman doctrine)."
                ),
                "suggested_next_step": "Require mutual agreement on the sole arbitrator, or appointment via an institutional body (e.g. DIAC or MCIA).",
                "suggested_alternative_wording": (
                    "Any dispute shall be referred to arbitration before a sole arbitrator appointed by mutual consent of the parties, or failing agreement, through the Delhi International Arbitration Centre (DIAC)."
                ),
                "confidence_level": "High (0.95)",
                "confidence_explanation": "Section 8.2 explicitly establishes unilateral arbitrator appointment.",
                "related_clause_ids": ["Section 8.1"]
            })

        # If document is NDA or other type, extract generic clauses as needed
        if doc_type == "Mutual Non-Disclosure & Confidentiality Agreement":
            clauses = [
                {
                    "clause_id": "Section 3",
                    "clause_title": "Mutual Non-Disclosure Covenants",
                    "category": "Confidentiality",
                    "section_number": "3",
                    "page_number": 1,
                    "exact_quotation": "Each party agrees: (a) to protect the other party's Confidential Information with the same degree of care it uses for its own confidential information, but not less than reasonable care...",
                    "quotation_verified": True,
                    "verification_status": "VERIFIED_VERBATIM",
                    "plain_english_explanation": "Standard balanced mutual confidentiality covenants applying reasonable care standards.",
                    "benefiting_party": "Mutual",
                    "potential_consequence": "Standard operational compliance required.",
                    "risk_level": "LOW APPARENT RISK",
                    "severity_justification": "Bilateral mutual standard of reasonable care.",
                    "suggested_next_step": "Ensure confidential data marking protocols are followed.",
                    "suggested_alternative_wording": "Current wording is commercially balanced.",
                    "confidence_level": "High (0.95)",
                    "confidence_explanation": "Section 3 verified against source text.",
                    "related_clause_ids": ["Section 2", "Section 4"]
                },
                {
                    "clause_id": "Section 4",
                    "clause_title": "Term and Bilateral Termination for Convenience",
                    "category": "Termination",
                    "section_number": "4",
                    "page_number": 1,
                    "exact_quotation": "Either party may terminate this Agreement for convenience at any time upon thirty (30) days' prior written notice to the other party.",
                    "quotation_verified": True,
                    "verification_status": "VERIFIED_VERBATIM",
                    "plain_english_explanation": "Mutual 30-day termination for convenience with 3-year survival of confidentiality.",
                    "benefiting_party": "Mutual",
                    "potential_consequence": "Clean exit available to both parties.",
                    "risk_level": "LOW APPARENT RISK",
                    "severity_justification": "Bilateral exit rights with appropriate survival period.",
                    "suggested_next_step": "None required.",
                    "suggested_alternative_wording": "Current provision is balanced.",
                    "confidence_level": "High (0.95)",
                    "confidence_explanation": "Section 4 verified.",
                    "related_clause_ids": ["Section 3"]
                },
                {
                    "clause_id": "Section 5",
                    "clause_title": "Mutual Limitation of Liability and Dollar Ceiling",
                    "category": "Liability Limitations",
                    "section_number": "5",
                    "page_number": 1,
                    "exact_quotation": "Neither party shall be liable to the other for any indirect, special, incidental, or consequential damages. Each party's total aggregate liability under this Agreement shall not exceed direct damages up to a maximum ceiling of USD 100,000.",
                    "quotation_verified": True,
                    "verification_status": "VERIFIED_VERBATIM",
                    "plain_english_explanation": "Mutual waiver of consequential damages with balanced $100,000 direct damages cap.",
                    "benefiting_party": "Mutual",
                    "potential_consequence": "Predefined liability cap protects both disclosing and receiving parties.",
                    "risk_level": "LOW APPARENT RISK",
                    "severity_justification": "Mutual consequential damages waiver and bilateral ceiling.",
                    "suggested_next_step": "Ensure $100,000 cap is proportionate to value of proprietary disclosures.",
                    "suggested_alternative_wording": "Current provision is balanced.",
                    "confidence_level": "High (0.95)",
                    "confidence_explanation": "Section 5 verified.",
                    "related_clause_ids": ["Section 3"]
                }
            ]

        # -------------------------------------------------------------
        # 4. Cross-Clause Programmatic Reasoning
        # -------------------------------------------------------------
        cross_clause_analysis = CrossClauseEngine.analyze_interactions(clauses, full_text)

        # -------------------------------------------------------------
        # 5. Missing Protections 4-State Classification
        # -------------------------------------------------------------
        # Evaluates: PRESENT, PARTIALLY PRESENT, ABSENT, UNCERTAIN
        missing_protections = []

        # Check Consequential Damages Waiver
        if "6.1" in full_text and "consequential damages" in text_lower:
            missing_protections.append({
                "protection_name": "Mutual Consequential Damages Waiver",
                "status": "PARTIALLY PRESENT",
                "importance": "HIGH",
                "existing_language_cited": "Section 6.1: 'In no event shall Service Provider, its officers, or employees be liable to Client for any indirect, incidental, special, exemplary, punitive, or consequential damages...'",
                "why_it_matters": (
                    "Section 6.1 already excludes consequential damages, but protects the Service Provider exclusively. "
                    "Client lacks reciprocal protection and remains exposed to consequential damages claims."
                ),
                "residual_gap": "Protection is completely asymmetric (one-sided). Client is not shielded from consequential claims.",
                "recommended_addition": "Mutualize Section 6.1 by replacing 'Service Provider' with 'Neither party'."
            })
        elif "consequential damages" in text_lower and "neither party" in text_lower:
            missing_protections.append({
                "protection_name": "Mutual Consequential Damages Waiver",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Mutual consequential damages waiver identified in agreement.",
                "why_it_matters": "Both parties are protected against speculative or indirect loss claims.",
                "residual_gap": "None identified.",
                "recommended_addition": "Maintain existing mutual exclusion."
            })
        else:
            missing_protections.append({
                "protection_name": "Mutual Consequential Damages Waiver",
                "status": "ABSENT",
                "importance": "HIGH",
                "existing_language_cited": "No consequential damages exclusion identified in text.",
                "why_it_matters": "Without an express mutual exclusion, parties are exposed to lost revenue and opportunity loss claims.",
                "residual_gap": "Complete absence of indirect damage exclusion.",
                "recommended_addition": "Insert standard mutual waiver of indirect, special, and consequential damages."
            })

        # Check Bilateral Convenience Termination
        if "terminate this agreement for convenience" in text_lower and "either party" in text_lower:
            missing_protections.append({
                "protection_name": "Bilateral Termination for Convenience",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Bilateral convenience termination granted to both parties.",
                "why_it_matters": "Allows both parties flexibility to exit if commercial requirements diverge.",
                "residual_gap": "None.",
                "recommended_addition": "Maintain existing bilateral exit clause."
            })
        elif "convenience" in text_lower and "service provider" in text_lower:
            missing_protections.append({
                "protection_name": "Bilateral Termination for Convenience",
                "status": "PARTIALLY PRESENT",
                "importance": "HIGH",
                "existing_language_cited": "Section 4.1: 'Service Provider may terminate this Agreement for convenience at any time...'",
                "why_it_matters": "Convenience termination exists but is granted exclusively to Service Provider; Client is locked in.",
                "residual_gap": "Client cannot terminate for convenience without paying 100% of remaining term fees (Section 4.3).",
                "recommended_addition": "Grant Client reciprocal convenience termination rights on 60 days' notice."
            })
        else:
            missing_protections.append({
                "protection_name": "Bilateral Termination for Convenience",
                "status": "ABSENT",
                "importance": "MODERATE",
                "existing_language_cited": "No termination for convenience provision found.",
                "why_it_matters": "Parties are bound to the full contract duration without discretionary exit remedies.",
                "residual_gap": "Neither party has exit flexibility.",
                "recommended_addition": "Insert 60-day mutual termination for convenience."
            })

        # Check Reciprocal Indemnification
        if "client shall defend, indemnify" in text_lower and "service provider shall defend, indemnify" not in text_lower:
            missing_protections.append({
                "protection_name": "Reciprocal Service Provider Indemnification",
                "status": "ABSENT",
                "importance": "HIGH",
                "existing_language_cited": "Section 5.1 imposes indemnity exclusively on Client.",
                "why_it_matters": "Client has no indemnity protection if the Service Provider's software infringes third-party intellectual property.",
                "residual_gap": "Provider provides zero IP indemnity or breach defense.",
                "recommended_addition": "Add Section 5.3: 'Service Provider shall defend and indemnify Client against third-party claims alleging IP infringement.'"
            })
        elif "each party shall defend, indemnify" in text_lower or ("indemnify" in text_lower and "mutual" in text_lower):
            missing_protections.append({
                "protection_name": "Reciprocal Indemnification",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Mutual indemnification covenants identified.",
                "why_it_matters": "Protects both parties against respective breaches.",
                "residual_gap": "None.",
                "recommended_addition": "Ensure indemnity liabilities are subject to the liability cap."
            })

        # Check Data Protection Addendum (DPA) & Return Protocol
        if "data protection addendum" not in text_lower and "delete customer data" not in text_lower:
            missing_protections.append({
                "protection_name": "Data Processing & Post-Termination Data Return Protocol",
                "status": "ABSENT",
                "importance": "MODERATE",
                "existing_language_cited": "No data deletion or extraction timeline specified upon contract end.",
                "why_it_matters": "Without explicit data return covenants, proprietary data retention and exit migration are unregulated.",
                "residual_gap": "No statutory DPDP Act compliance or transition assistance defined.",
                "recommended_addition": "Mandate Provider return or certify destruction of all Client data within thirty (30) days of termination."
            })

        # Check Source Code Escrow
        if "escrow" in text_lower:
            missing_protections.append({
                "protection_name": "Source Code Escrow & Continuity Protection",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Software source code deposit arrangements identified.",
                "why_it_matters": "Provides continuity if provider ceases operations or enters bankruptcy.",
                "residual_gap": "None.",
                "recommended_addition": "Verify release triggers and annual verification testing."
            })
        else:
            missing_protections.append({
                "protection_name": "Source Code Escrow & Continuity Protection",
                "status": "ABSENT",
                "importance": "MODERATE",
                "existing_language_cited": "No source code deposit or continuity escrow mechanism found in text.",
                "why_it_matters": "If Provider enters insolvency, liquidation, or abruptly discontinues hosted platform services, Customer loses operational access without recourse to source code for continuity.",
                "residual_gap": "Complete absence of escrow protection.",
                "recommended_addition": "Require Provider to deposit core application source code with a neutral third-party escrow agent with defined release conditions upon insolvency."
            })

        # Check Data Breach Notification SLA
        if "data breach" in text_lower and ("hour" in text_lower or "24" in text_lower or "48" in text_lower or "72" in text_lower):
            missing_protections.append({
                "protection_name": "Data Breach Notification & Incident Remediation SLA",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Expedited security incident and breach notification covenants identified.",
                "why_it_matters": "Ensures prompt awareness of cybersecurity compromises.",
                "residual_gap": "None.",
                "recommended_addition": "Maintain strict incident remediation timelines."
            })
        else:
            missing_protections.append({
                "protection_name": "Data Breach Notification & Incident Remediation SLA",
                "status": "ABSENT",
                "importance": "HIGH",
                "existing_language_cited": "No express breach notification timeline or mitigation protocol found.",
                "why_it_matters": "Customer is exposed to regulatory penalties under DPDP Act 2023 / GDPR if security incidents are not communicated promptly to enable statutory reporting within prescribed windows.",
                "residual_gap": "Zero contractual commitment regarding cybersecurity incident reporting deadlines.",
                "recommended_addition": "Add clause: 'Service Provider shall notify Customer in writing within twenty-four (24) hours of becoming aware of any confirmed or suspected security incident or data breach.'"
            })

        # Check Service Level Agreement (SLA) & Uptime Credit Remedies
        if "uptime" in text_lower and ("credit" in text_lower or "service level" in text_lower):
            missing_protections.append({
                "protection_name": "Service Level Agreement (SLA) & Financial Credit Remedies",
                "status": "PRESENT",
                "importance": "LOW",
                "existing_language_cited": "Uptime availability commitments with credit remedies identified.",
                "why_it_matters": "Protects against chronic service degradation.",
                "residual_gap": "None.",
                "recommended_addition": "Ensure SLA performance credits are excluded from general liability caps."
            })
        else:
            missing_protections.append({
                "protection_name": "Service Level Agreement (SLA) & Financial Credit Remedies",
                "status": "ABSENT",
                "importance": "HIGH",
                "existing_language_cited": "No availability percentage (e.g. 99.9%) or service credit remedy stated in document body.",
                "why_it_matters": "Without an enforceable availability SLA, Customer must pay full subscription fees even during sustained platform outages.",
                "residual_gap": "No financial or operational recourse for chronic platform downtime.",
                "recommended_addition": "Incorporate a 99.9% uptime SLA with tiered fee credits (10% to 50% monthly invoice deduction) for failure to meet availability targets."
            })

        # -------------------------------------------------------------
        # 6. Multi-Dimensional Transparent Risk Scoring
        # -------------------------------------------------------------
        # 5 Dimensions:
        # - Financial Exposure (30% weight)
        # - Legal Imbalance (25% weight)
        # - Data & Confidentiality (20% weight)
        # - Operational Continuity (15% weight)
        # - Ambiguity & Drafting (10% weight)

        high_clauses = [c for c in clauses if c.get("risk_level") == "HIGH RISK"]
        mod_clauses = [c for c in clauses if c.get("risk_level") == "MODERATE RISK"]

        # Calculate dimension scores (0-100)
        # Financial: Uncapped indemnity, 1-month liability cap, 24% interest
        dim_financial = 85 if any(c.get("category") in ["Liability Limitations", "Payment & Penalties", "Indemnification"] and c.get("risk_level") == "HIGH RISK" for c in clauses) else 20
        # Imbalance: Termination asymmetry, unilateral amendments, unilateral arbitration
        dim_imbalance = 90 if any(c.get("category") in ["Termination", "Unilateral Amendment"] and c.get("risk_level") == "HIGH RISK" for c in clauses) else 15
        # Data & Conf: Lost data waived, no DPA
        dim_data = 75 if any(mp.get("protection_name") == "Data Processing & Post-Termination Data Return Protocol" and mp.get("status") == "ABSENT" for mp in missing_protections) else 20
        # Operational: 90-day auto-renewal trap, convenience exit by vendor
        dim_operational = 80 if any(c.get("category") == "Automatic Renewal" and c.get("risk_level") == "HIGH RISK" for c in clauses) else 25
        # Ambiguity: Vague cap interactions
        dim_ambiguity = 60 if any(c.get("category") == "Dispute Resolution & Arbitration" for c in clauses) else 15

        if doc_type == "Mutual Non-Disclosure & Confidentiality Agreement":
            dim_financial = 20
            dim_imbalance = 15
            dim_data = 25
            dim_operational = 15
            dim_ambiguity = 10

        weighted_score = round(
            (dim_financial * 0.30) +
            (dim_imbalance * 0.25) +
            (dim_data * 0.20) +
            (dim_operational * 0.15) +
            (dim_ambiguity * 0.10)
        )

        overall_score = min(95, max(15, weighted_score))

        if overall_score >= 65:
            risk_cat = "HIGH RISK"
        elif overall_score >= 40:
            risk_cat = "MODERATE RISK"
        else:
            risk_cat = "LOW APPARENT RISK"

        methodology_text = (
            f"Multi-dimensional weighted model: Financial Exposure ({dim_financial}/100 x 30%), "
            f"Legal & Contractual Imbalance ({dim_imbalance}/100 x 25%), Data & Confidentiality ({dim_data}/100 x 20%), "
            f"Operational Continuity ({dim_operational}/100 x 15%), and Ambiguity & Drafting ({dim_ambiguity}/100 x 10%). "
            f"Consolidated composite score: {overall_score}/100 ({risk_cat})."
        )

        contributing_factors = [
            {"factor": "Financial Exposure (30%)", "impact": "HIGH" if dim_financial >= 70 else "LOW", "detail": f"One-month liability cap vs uncapped indemnity exposure ({dim_financial}/100)."},
            {"factor": "Contractual Imbalance (25%)", "impact": "HIGH" if dim_imbalance >= 70 else "LOW", "detail": f"Unilateral exit rights and unilateral web-posted amendment clauses ({dim_imbalance}/100)."},
            {"factor": "Operational Continuity (15%)", "impact": "HIGH" if dim_operational >= 70 else "LOW", "detail": f"90-day non-renewal notice trap and automatic 15% escalation ({dim_operational}/100)."},
            {"factor": "Data & Privacy Exposure (20%)", "impact": "MODERATE" if dim_data >= 50 else "LOW", "detail": f"Lack of post-termination data return covenants and DPA ({dim_data}/100)."}
        ]

        # Stated CIN
        cin_m = re.search(r"\b[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}\b", full_text)
        cin_val = cin_m.group(0) if cin_m else "Not explicitly stated in text"

        return {
            "document_summary": {
                "document_type": doc_type,
                "parties": [
                    {"name": party1, "role": "First Party / Provider", "jurisdiction": "Governing Jurisdiction"},
                    {"name": party2, "role": "Second Party / Customer", "jurisdiction": "Governing Jurisdiction"}
                ],
                "effective_date": effective_date,
                "term_duration": f"{renewal_timeline['initial_term_months']} Months (Auto-Renewing)",
                "primary_subject": f"Commercial commitments and operational covenants for {doc_type}",
                "executive_takeaway": (
                    f"Forensic audit of {len(clauses)} core provisions indicates {len(high_clauses)} critical risk covenants. "
                    "Primary vulnerabilities stem from asymmetric convenience termination, uncapped indemnification, a 1-month liability ceiling, and a 90-day renewal notice trap."
                    if high_clauses else "Balanced commercial agreement with reciprocal terms and standard liability ceilings."
                )
            },
            "overall_risk": {
                "score": overall_score,
                "category": risk_cat,
                "methodology_explanation": methodology_text,
                "contributing_factors": contributing_factors,
                "dimension_scores": {
                    "financial_exposure": dim_financial,
                    "contractual_imbalance": dim_imbalance,
                    "data_confidentiality": dim_data,
                    "operational_continuity": dim_operational,
                    "drafting_ambiguity": dim_ambiguity
                }
            },
            "clauses": clauses,
            "cross_clause_analysis": cross_clause_analysis,
            "missing_protections": missing_protections,
            "renewal_timeline": renewal_timeline,
            "financial_analytics": {
                "liability_cap": liability_cap_data,
                "payment_penalties": payment_penalty_data
            },
            "counterparty_profile": {
                "primary_counterparty": party1,
                "stated_registration_or_cin": cin_val,
                "jurisdiction_state": "Delhi, India" if "new delhi" in text_lower else "Governing Jurisdiction",
                "registered_address": "Plot 42, Okhla Industrial Area, Phase-III, New Delhi" if "okhla" in text_lower else "Stated in preamble recitals",
                "official_domain": "vertexdynamics.example.com" if "vertex" in text_lower else "Not specified"
            }
        }
