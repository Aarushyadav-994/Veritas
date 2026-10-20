import re
from typing import Dict, Any, List

class CrossClauseEngine:
    """
    Evaluates cross-clause dependencies, conflicts, and compounding risk interactions
    across disparate sections of an agreement.
    """

    @staticmethod
    def analyze_interactions(
        clauses: List[Dict[str, Any]],
        full_text: str
    ) -> List[Dict[str, Any]]:
        """
        Detects and analyzes critical cross-clause interactions across the agreement.
        """
        interactions: List[Dict[str, Any]] = []
        text_lower = full_text.lower()

        # Map clauses by category or keyword
        cat_map = {}
        for c in clauses:
            cat = c.get("category", "")
            if cat not in cat_map:
                cat_map[cat] = []
            cat_map[cat].append(c)

        # -------------------------------------------------------------
        # Relationship A: Liability Cap + Indemnification
        # -------------------------------------------------------------
        has_indemnity = any("indemnif" in c.get("category", "").lower() or "indemnif" in c.get("original_excerpt", "").lower() for c in clauses)
        has_cap = any("liability" in c.get("category", "").lower() or "limitation of liability" in c.get("original_excerpt", "").lower() for c in clauses)

        if has_indemnity and has_cap:
            indemnity_clause = next((c for c in clauses if "indemnif" in c.get("category", "").lower()), None)
            cap_clause = next((c for c in clauses if "liability" in c.get("category", "").lower()), None)

            # Check if indemnity is carved out or capped
            is_expressly_uncapped = bool(re.search(r"(?:indemnification|indemnity|section\s+5)[\s\w,]+(?:are|is|shall\s+be)\s+(?:unconditional|uncapped|excluded|not\s+subject)", text_lower) or ("indemnif" in text_lower and "uncapped" in text_lower))
            is_expressly_capped = bool(re.search(r"(?:indemnification|indemnity|section\s+5)[\s\w,]+(?:are|is|shall\s+be)\s+(?:subject\s+to|included\s+within|limited\s+by)\s+(?:the\s+aggregate\s+liability\s+cap|this\s+section\s+6)", text_lower))

            if is_expressly_uncapped:
                nature = "ASYMMETRIC_UNCONSTRAINED_EXPOSURE"
                severity = "HIGH RISK"
                detail = (
                    "Customer indemnification obligations are expressly excluded from the liability cap (uncapped and unconditional), "
                    "while Service Provider's total aggregate liability is severely restricted to trailing subscription fees. "
                    "This creates catastrophic financial asymmetry: the Customer faces infinite third-party liability exposure, "
                    "whereas the Provider's maximum legal exposure is capped at nominal monthly sums."
                )
            elif is_expressly_capped:
                nature = "BILATERAL_CAP_APPLIED"
                severity = "LOW APPARENT RISK"
                detail = "Indemnification obligations are expressly subjected to the contractual aggregate liability ceiling, containing catastrophic third-party exposure."
            else:
                nature = "AMBIGUOUS_INDEMNITY_CAP_INTERACTION"
                severity = "MODERATE RISK"
                detail = (
                    "The agreement contains both an indemnification clause and a general aggregate liability cap, but fails to explicitly "
                    "state whether indemnity claims are subject to or carved out from the cap. This creates substantial judicial ambiguity."
                )

            interactions.append({
                "interaction_id": "X-CLAUSE-01",
                "relationship_type": "Liability Cap + Indemnification",
                "clauses_involved": [
                    indemnity_clause.get("clause_id", "Section 5") if indemnity_clause else "Indemnification Clause",
                    cap_clause.get("clause_id", "Section 6") if cap_clause else "Liability Cap Clause"
                ],
                "nature": nature,
                "risk_severity": severity,
                "analysis": detail,
                "negotiation_action": "Insert express reciprocal clarification: 'In no event shall either party's indemnification obligations exceed two times (2x) the total fees paid or payable under this Agreement.'"
            })

        # -------------------------------------------------------------
        # Relationship B: Liability Cap + Data Security / Confidentiality
        # -------------------------------------------------------------
        if has_cap:
            has_data_conf = bool(re.search(r"(?:confidentiality|data\s+loss|security\s+incident|data\s+protection|personal\s+data)", text_lower))
            has_conf_carveout = bool(re.search(r"(?:breach\s+of\s+confidentiality|data\s+security)[\s\w,]*shall\s+be\s+(?:excepted|carved\s+out|excluded\s+from\s+the\s+cap)", text_lower))
            has_conf_cap = bool(re.search(r"(?:in\s+no\s+event|for\s+any\s+claim|whether\s+in\s+contract\s+or\s+tort)[\s\w,]*lost\s+data|business\s+interruption", text_lower))

            if has_conf_cap and not has_conf_carveout:
                interactions.append({
                    "interaction_id": "X-CLAUSE-02",
                    "relationship_type": "Liability Cap + Data Security / Breaches",
                    "clauses_involved": [
                        cap_clause.get("clause_id", "Section 6") if cap_clause else "Section 6 (Liability Cap)",
                        "Confidentiality & Data Protection"
                    ],
                    "nature": "SUPPRESSED_DATA_INCIDENT_REMEDY",
                    "risk_severity": "HIGH RISK",
                    "analysis": (
                        "The limitation of liability waives all consequential and lost data claims while capping total recovery to trailing monthly fees. "
                        "Because there is no super-cap or carve-out for data breaches or gross negligence, a major cybersecurity incident "
                        "or proprietary data loss caused by Provider negligence provides the Customer with negligible financial recourse."
                    ),
                    "negotiation_action": "Establish an independent 'Super-Cap' (e.g. 5x contract value or $1,000,000) specifically dedicated to data protection, security breaches, and confidentiality violations."
                })

        # -------------------------------------------------------------
        # Relationship C: Initial-Term Pricing + Renewal Pricing
        # -------------------------------------------------------------
        has_auto_renew = any("renew" in c.get("category", "").lower() for c in clauses)
        has_price_escalation = bool(re.search(r"(?:increase|escalat(?:e|ion)|adjust(?:ment)?)[\s\w,]*by\s+(?:\d{1,2}%)", text_lower))

        if has_auto_renew:
            renew_clause = next((c for c in clauses if "renew" in c.get("category", "").lower()), None)
            if has_price_escalation:
                pct_m = re.search(r"increase[\s\w,]*by\s*(\d{1,2}%)", text_lower)
                pct_str = pct_m.group(1) if pct_m else "unilateral percentage"
                interactions.append({
                    "interaction_id": "X-CLAUSE-03",
                    "relationship_type": "Initial-Term Pricing vs Renewal Escalation",
                    "clauses_involved": [
                        renew_clause.get("clause_id", "Section 3") if renew_clause else "Section 3 (Renewal)",
                        "Section 2 (Fees)"
                    ],
                    "nature": "AUTOMATIC_COMPOUNDING_PRICE_ESCALATION",
                    "risk_severity": "MODERATE RISK",
                    "analysis": (
                        f"Pricing is stabilized during the Initial Term but escalates automatically by {pct_str} upon each successive renewal "
                        "without requiring affirmative Customer consent. Combined with the 90-day non-renewal notice requirement, missing the cancellation "
                        "window automatically binds the Customer to both a term extension and compounding price increases."
                    ),
                    "negotiation_action": "Cap renewal price increases to the lesser of 3% or the Consumer Price Index (CPI), and require Provider to send an explicit price change notice at least 60 days before the non-renewal deadline."
                })

        # -------------------------------------------------------------
        # Relationship D: Automatic Renewal + Non-Renewal Notice
        # -------------------------------------------------------------
        if has_auto_renew:
            notice_m = re.search(r"(?:ninety|90|sixty|60|one\s+hundred\s+twenty|120)\s*days?", text_lower)
            notice_days = notice_m.group(0) if notice_m else "advance notice"
            interactions.append({
                "interaction_id": "X-CLAUSE-04",
                "relationship_type": "Automatic Renewal + Notice Window Trap",
                "clauses_involved": [
                    renew_clause.get("clause_id", "Section 3") if renew_clause else "Section 3 (Term & Renewal)"
                ],
                "nature": "NARROW_OPT_OUT_WINDOW",
                "risk_severity": "MODERATE RISK",
                "analysis": (
                    f"The contract renews automatically unless written non-renewal notice is served at least {notice_days} prior to term expiration. "
                    "The contract places zero obligation on the Provider to issue a reminder notice. A Customer failing to track this specific calendar "
                    "anniversary will be locked into subsequent multi-year commitments."
                ),
                "negotiation_action": "Reduce non-renewal notice from 90 to 30 days, and mandate a contractual reminder notice from Provider 60 days prior to the expiration date."
            })

        # -------------------------------------------------------------
        # Relationship E: Termination Rights vs Committed Term
        # -------------------------------------------------------------
        term_clause = next((c for c in clauses if "termination" in c.get("category", "").lower()), None)
        has_conv_provider = bool(re.search(r"(?:provider|company)[\s\w,]*terminate[\s\w,]*(?:without\s+cause|for\s+convenience|at\s+any\s+time)", text_lower))
        has_lockin_client = bool(re.search(r"(?:early\s+termination\s+fee|100%|all\s+remaining\s+fees|unexpired\s+portion)", text_lower))

        if has_conv_provider and has_lockin_client:
            interactions.append({
                "interaction_id": "X-CLAUSE-05",
                "relationship_type": "Termination Asymmetry + Committed Term",
                "clauses_involved": [
                    term_clause.get("clause_id", "Section 4") if term_clause else "Section 4 (Termination)",
                    "Section 3 (Committed Term)"
                ],
                "nature": "UNILATERAL_EXIT_EQUITY_DEFICIT",
                "risk_severity": "HIGH RISK",
                "analysis": (
                    "Severe contractual exit asymmetry: Provider possesses discretionary exit rights (convenience termination on 45 days or immediately), "
                    "whereas Customer cannot terminate for convenience without paying 100% of all fees across the remainder of the committed term. "
                    "Customer assumes full downside commercial risk of the committed term while Provider maintains optionality."
                ),
                "negotiation_action": "Require reciprocal bilateral termination for convenience on 60 days' notice with pro-rata refund of unearned prepaid fees, eliminating the 100% unexpired fee penalty."
            })

        # -------------------------------------------------------------
        # Relationship F: Online Policy Updates + Objection Window
        # -------------------------------------------------------------
        has_unilateral_amend = any("unilateral" in c.get("category", "").lower() or "website" in c.get("original_excerpt", "").lower() for c in clauses)
        if has_unilateral_amend:
            amend_clause = next((c for c in clauses if "amend" in c.get("category", "").lower()), None)
            interactions.append({
                "interaction_id": "X-CLAUSE-06",
                "relationship_type": "Online Policy Updates vs Fixed Covenants",
                "clauses_involved": [
                    amend_clause.get("clause_id", "Section 7") if amend_clause else "Section 7 (Unilateral Amendment)"
                ],
                "nature": "DYNAMIC_COVENANT_SUBORDINATION",
                "risk_severity": "HIGH RISK",
                "analysis": (
                    "Provider reserves unilateral discretion to alter terms, features, and SLAs simply by publishing updates to a website URL. "
                    "Continued access or payment constitutes deemed acceptance without an objection window or exit remedy. "
                    "This undermines the stability of all negotiated baseline covenants."
                ),
                "negotiation_action": "Require written notice of material changes at least 30 days in advance, and grant Customer the affirmative right to terminate without penalty if revised terms materially degrade service or rights."
            })

        return interactions
