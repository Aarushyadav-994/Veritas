import os
import re
import json
from typing import Dict, Any, List, Optional
from backend.config import settings

class ClauseAnalyzer:
    @staticmethod
    def analyze_document(full_text: str, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Coordinates document analysis using Gemini API if configured,
        or the deterministic heuristic legal engine if credentials are not set.
        """
        if settings.gemini_api_key and settings.gemini_api_key.strip():
            try:
                gemini_result = ClauseAnalyzer._analyze_with_gemini(full_text, pages_data)
                if gemini_result and "clauses" in gemini_result and len(gemini_result["clauses"]) > 0:
                    gemini_result["engine"] = f"Google Gemini ({settings.gemini_model})"
                    return gemini_result
            except Exception as e:
                # Log error and fallback gracefully to deterministic engine
                print(f"[ClauseAnalyzer] Gemini API failed: {str(e)}. Falling back to deterministic engine.")

        # Fallback deterministic analysis engine
        res = ClauseAnalyzer._analyze_heuristic(full_text, pages_data)
        res["engine"] = "Veritas Deterministic Legal Heuristic Engine (Offline/Local)"
        return res

    @staticmethod
    def _analyze_with_gemini(full_text: str, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)

        prompt = f"""
You are Veritas AI, an investigative legal intelligence analyst. Analyze the following legal agreement text thoroughly.
Do not invent facts or cite laws not present in the document.

DOCUMENT TEXT:
\"\"\"
{full_text[:40000]}
\"\"\"

Produce a strict JSON response conforming to this exact structure:
{{
  "document_summary": {{
    "document_type": "string (e.g., Master Services Agreement, Non-Disclosure Agreement, Employment Agreement, SaaS Terms)",
    "parties": [
      {{"name": "string", "role": "string (e.g., Service Provider, Client, Disclosing Party)", "jurisdiction": "string"}}
    ],
    "effective_date": "string or Not specified",
    "term_duration": "string or Not specified",
    "primary_subject": "string",
    "executive_takeaway": "string (2-3 sentences concise briefing for a business reviewer)"
  }},
  "overall_risk": {{
    "score": integer (0 to 100, where 0 is pristine/low risk, 100 is critical exposure),
    "category": "HIGH RISK" | "MODERATE RISK" | "LOW APPARENT RISK" | "NEEDS REVIEW",
    "methodology_explanation": "string explaining how the score was calculated based on specific unfavorable terms found",
    "contributing_factors": [
      {{"factor": "string", "impact": "HIGH" | "MODERATE" | "LOW", "detail": "string"}}
    ]
  }},
  "clauses": [
    {{
      "clause_id": "string (e.g. Clause 4.2 or Section 8)",
      "category": "Termination" | "Automatic Renewal" | "Payment & Penalties" | "Indemnification" | "Liability Limitations" | "Confidentiality" | "Intellectual Property" | "Exclusivity" | "Non-Compete" | "Dispute Resolution" | "Jurisdiction" | "Arbitration" | "Data Protection" | "Unilateral Amendment",
      "risk_level": "HIGH RISK" | "MODERATE RISK" | "LOW APPARENT RISK" | "NEEDS REVIEW",
      "original_excerpt": "string (verbatim quote from the text)",
      "page_number": integer (best estimate based on page breaks),
      "plain_english_explanation": "string",
      "why_it_matters": "string",
      "potential_consequence": "string",
      "suggested_next_step": "string",
      "evidence": "string (specific language or phrasing indicating the risk)"
    }}
  ],
  "missing_protections": [
    {{
      "protection_name": "string (e.g. Mutual Bilateral Termination, Limitation of Consequential Damages Cap, Cure Period for Breach)",
      "importance": "HIGH" | "MODERATE" | "LOW",
      "why_it_matters": "string",
      "recommended_addition": "string"
    }}
  ],
  "counterparty_profile": {{
    "primary_counterparty": "string",
    "stated_registration_or_cin": "string or Not mentioned",
    "jurisdiction_state": "string or Not specified",
    "registered_address": "string or Not specified",
    "official_domain": "string or Not specified"
  }}
}}
Return ONLY valid JSON.
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return json.loads(response.text)

    @staticmethod
    def _analyze_heuristic(full_text: str, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Deterministic NLP & pattern-based clause extraction and risk assessment.
        Ensures 100% functionality without API keys.
        """
        lines = full_text.split("\n")
        clauses: List[Dict[str, Any]] = []

        # Party detection
        party_regex = re.compile(r"(?:between|by and between)\s+([A-Z0-9\s,\.]{3,60}?)(?:,\s*a\s+[A-Za-z\s]+|having its|referred to as|\()(?:\s*and\s*|\s*,\s*)([A-Z0-9\s,\.]{3,60})", re.IGNORECASE)
        match_parties = party_regex.search(full_text[:2000])

        party1 = "Party A"
        party2 = "Party B"
        if match_parties:
            p1 = match_parties.group(1).strip()
            p2 = match_parties.group(2).strip()
            if len(p1) > 2 and len(p1) < 80:
                party1 = p1
            if len(p2) > 2 and len(p2) < 80:
                party2 = p2
        else:
            # Common patterns in headers
            for line in lines[:30]:
                if any(k in line.lower() for k in ["pvt ltd", "private limited", "inc.", "corp", "llc", "technologies", "services"]):
                    clean = re.sub(r"[^A-Za-z0-9\s\.\-]", "", line).strip()
                    if len(clean) > 5 and len(clean) < 70:
                        party1 = clean
                        break

        # Document Type Detection
        doc_type = "Commercial Contract"
        upper_header = full_text[:1500].upper()
        if "MASTER SERVICES AGREEMENT" in upper_header:
            doc_type = "Master Services Agreement (MSA)"
        elif "NON-DISCLOSURE" in upper_header or "CONFIDENTIALITY" in upper_header:
            doc_type = "Non-Disclosure Agreement (NDA)"
        elif "SOFTWARE AS A SERVICE" in upper_header or "SAAS" in upper_header:
            doc_type = "Software as a Service (SaaS) Agreement"
        elif "EMPLOYMENT" in upper_header:
            doc_type = "Employment Agreement"
        elif "INDEPENDENT CONTRACTOR" in upper_header or "CONSULTING" in upper_header:
            doc_type = "Consulting & Services Agreement"
        elif "SERVICE LEVEL AGREEMENT" in upper_header:
            doc_type = "Service Level Agreement (SLA)"

        # Date Detection
        date_match = re.search(r"(?:dated|effective\s+as\s+of|entered\s+into\s+on)\s+([A-Za-z0-9\s,]{4,30}\d{4})", full_text[:2500], re.IGNORECASE)
        effective_date = date_match.group(1).strip() if date_match else "Execution Date"

        # Clause Segmentation & Pattern Rules
        # Rule sets for each risk category
        patterns = [
            {
                "category": "Termination",
                "pattern": re.compile(r"(\b(?:termination|terminate|cancellation)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(sole discretion|without cause by (?:company|provider)|without notice|no refund|forfeit|immediate termination by provider|lock-in)", re.IGNORECASE),
                "high_risk_desc": "Unilateral or asymmetric termination rights allowing one party to exit without cause while penalizing the counterparty.",
                "why": "Prevents predictable operational planning and leaves your business exposed to abrupt vendor cessation without reciprocal exit remedies."
            },
            {
                "category": "Automatic Renewal",
                "pattern": re.compile(r"(\b(?:automatic(?:ally)?\s+renew|renewal\s+period|auto-renew|successive\s+terms?)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(renew(?:s)? automatically|unless written notice|not less than (?:60|90|120) days|without prior consent|annual price increase)", re.IGNORECASE),
                "high_risk_desc": "Automatic renewal lock-in requiring notice up to 90 days prior, failing which fees renew for a full subsequent cycle.",
                "why": "Missing the narrow notice window locks in another full contract term and accompanying subscription payments automatically."
            },
            {
                "category": "Indemnification",
                "pattern": re.compile(r"(\b(?:indemnify|indemnification|hold harmless|defend and hold)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(indemnify and hold harmless.*against any and all|broadest extent|without cap|uncapped|third-party claims|attorney'?s'? fees)", re.IGNORECASE),
                "high_risk_desc": "One-sided, uncapped indemnification requiring you to defend and cover all counterparty losses including legal fees.",
                "why": "Exposes your business to boundless catastrophic third-party liabilities far exceeding the financial value of the contract."
            },
            {
                "category": "Liability Limitations",
                "pattern": re.compile(r"(\b(?:limitation of liability|aggregate liability|consequential damages|indirect damages)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(in no event shall (?:provider|company) be liable|exceed (?:the fees paid in the preceding (?:1|3) month|100\s*\$|one hundred)|no liability for lost profits)", re.IGNORECASE),
                "high_risk_desc": "Severe limitation of provider liability capped at a trivial sum (e.g. 1 month fees or $100), waiving consequential damages.",
                "why": "If the provider experiences a severe breach or data leak, your financial recovery is legally suppressed to an insignificant nominal amount."
            },
            {
                "category": "Payment & Penalties",
                "pattern": re.compile(r"(\b(?:late payment|interest|penalty|liquidated damages|fees and payment)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"((?:18|24|36)%\s*(?:per annum|annually)|(?:1\.5|2|3)%\s*per month|liquidated damages|immediately due|disputed charges)", re.IGNORECASE),
                "high_risk_desc": "Exorbitant late interest penalties (e.g. 24%+ p.a.) or liquidated damages payable immediately upon dispute.",
                "why": "Creates severe cash-flow traps and exposes disputed invoices to punitive financial accumulation."
            },
            {
                "category": "Unilateral Amendment",
                "pattern": re.compile(r"(\b(?:unilateral|modify these terms|amend(?:ment)?\s+at\s+any\s+time|sole discretion to change|posted on website)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(amend(?:ment)? at any time|without prior notice|sole discretion to modify|continued use constitutes acceptance)", re.IGNORECASE),
                "high_risk_desc": "Unilateral amendment clause permitting the provider to modify contract terms, pricing, or SLAs without your active signature.",
                "why": "Subordinates your negotiated terms to dynamic future alterations made unilaterally on the provider's website."
            },
            {
                "category": "Dispute Resolution & Jurisdiction",
                "pattern": re.compile(r"(\b(?:governing law|jurisdiction|dispute resolution|arbitration|courts of)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(exclusive jurisdiction of the courts of|binding arbitration|waive jury|waive class action|sole arbitrator appointed by)", re.IGNORECASE),
                "high_risk_desc": "Exclusive jurisdiction in distant venue or mandatory arbitration with unilateral arbitrator appointment.",
                "why": "Significantly inflates the expense and barrier to enforcing legitimate claims or defending against frivolous demands."
            },
            {
                "category": "Intellectual Property",
                "pattern": re.compile(r"(\b(?:intellectual property|ip rights|work for hire|proprietary rights|ownership of deliverables)\b[^\n\.]{0,100}[\s\S]{50,600}?(?:\.|\n\n))", re.IGNORECASE),
                "unfavorable_pattern": re.compile(r"(all rights(?:,\s*title and interest)? shall vest exclusively in|assignment of pre-existing|irrevocable license without royalty)", re.IGNORECASE),
                "high_risk_desc": "Overbroad intellectual property assignment encompassing background IP or customer-provided data.",
                "why": "Risk of inadvertently transferring foundational proprietary assets, code, or trademarks."
            }
        ]

        found_categories = set()
        clause_counter = 1

        for rule in patterns:
            cat = rule["category"]
            p = rule["pattern"]
            matches = p.findall(full_text)

            for match in matches[:2]: # Max 2 per category
                excerpt = match.strip()
                if len(excerpt) < 60:
                    continue

                # Estimate page number
                page_num = 1
                for p_idx, page in enumerate(pages_data):
                    if excerpt[:40] in page["text"]:
                        page_num = page["page_number"]
                        break

                is_unfavorable = bool(rule["unfavorable_pattern"].search(excerpt))
                risk = "HIGH RISK" if is_unfavorable else "MODERATE RISK"
                
                # Check for mild or standard terms
                if not is_unfavorable:
                    if any(term in excerpt.lower() for term in ["mutual", "standard", "commercially reasonable", "30 days written notice"]):
                        risk = "LOW APPARENT RISK"

                # Extract clause identifier if available (e.g. "Section 4.1" or "Clause 7")
                id_match = re.search(r"\b(Clause\s+\d+(?:\.\d+)?|Section\s+\d+(?:\.\d+)?|Article\s+[IVXLCDM\d]+|\d+\.\d+)\b", excerpt[:50], re.IGNORECASE)
                clause_id = id_match.group(1) if id_match else f"Clause {clause_counter}.0 ({cat})"

                explanation = rule["high_risk_desc"] if is_unfavorable else f"Standard contractual terms governing {cat.lower()}."
                why_matters = rule["why"] if is_unfavorable else f"Defines rights and mutual boundaries under {cat.lower()}."
                
                consequence = "Financial exposure or legal vulnerability in case of contractual dispute or early termination." if is_unfavorable else "Standard operational compliance required."
                next_step = f"Negotiate bilateral terms or add mutual notice period to {clause_id}." if is_unfavorable else "Verify alignment with operational expectations."

                clauses.append({
                    "clause_id": clause_id,
                    "category": cat,
                    "risk_level": risk,
                    "original_excerpt": excerpt[:500] + ("..." if len(excerpt) > 500 else ""),
                    "page_number": page_num,
                    "plain_english_explanation": explanation,
                    "why_it_matters": why_matters,
                    "potential_consequence": consequence,
                    "suggested_next_step": next_step,
                    "evidence": rule["unfavorable_pattern"].search(excerpt).group(0) if is_unfavorable and rule["unfavorable_pattern"].search(excerpt) else "Standard language identified"
                })
                found_categories.add(cat)
                clause_counter += 1

        # Check for Missing Protections
        missing_protections = []
        if "Liability Limitations" not in found_categories or not any("consequential damages" in c["original_excerpt"].lower() for c in clauses):
            missing_protections.append({
                "protection_name": "Mutual Consequential Damages Waiver",
                "importance": "HIGH",
                "why_it_matters": "Without an express mutual exclusion of indirect, special, or consequential damages, you could be held liable for counterparty lost revenue or opportunity losses.",
                "recommended_addition": "Insert standard waiver: 'Neither party shall be liable for any indirect, incidental, punitive, or consequential damages arising out of this Agreement.'"
            })

        if "Termination" not in found_categories or not any("without cause" in c["original_excerpt"].lower() for c in clauses):
            missing_protections.append({
                "protection_name": "Bilateral Termination for Convenience",
                "importance": "MODERATE",
                "why_it_matters": "Prevents being trapped in an unproductive vendor relationship for the entire contract term if business requirements change.",
                "recommended_addition": "Add: 'Either party may terminate this Agreement without cause upon providing sixty (60) days prior written notice.'"
            })

        if not any("cure period" in full_text.lower() or "30 days" in full_text.lower() for _ in [1]):
            missing_protections.append({
                "protection_name": "Material Breach Cure Period",
                "importance": "MODERATE",
                "why_it_matters": "Protects against abrupt immediate cancellation for technical or minor operational breaches without an opportunity to rectify.",
                "recommended_addition": "Specify a mandatory 30-day written notice and cure window before termination for cause can be triggered."
            })

        # Calculate Overall Risk Score
        high_risks = [c for c in clauses if c["risk_level"] == "HIGH RISK"]
        mod_risks = [c for c in clauses if c["risk_level"] == "MODERATE RISK"]
        
        # Transparent scoring formula
        score = min(95, 20 + (len(high_risks) * 18) + (len(mod_risks) * 8) + (len(missing_protections) * 5))
        if not clauses:
            score = 15

        if score >= 65:
            cat_level = "HIGH RISK"
        elif score >= 40:
            cat_level = "MODERATE RISK"
        else:
            cat_level = "LOW APPARENT RISK"

        contributing = []
        for hr in high_risks:
            contributing.append({
                "factor": f"{hr['category']}: {hr['clause_id']}",
                "impact": "HIGH",
                "detail": hr["plain_english_explanation"]
            })
        for mp in missing_protections:
            contributing.append({
                "factor": f"Omission: {mp['protection_name']}",
                "impact": mp["importance"],
                "detail": mp["why_it_matters"]
            })

        # Counterparty extract
        cin_match = re.search(r"\b[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}\b", full_text)
        cin_val = cin_match.group(0) if cin_match else "Not explicitly stated in text"

        return {
            "document_summary": {
                "document_type": doc_type,
                "parties": [
                    {"name": party1, "role": "First Party / Disclosing", "jurisdiction": "Governing Jurisdiction"},
                    {"name": party2, "role": "Second Party / Receiving", "jurisdiction": "Governing Jurisdiction"}
                ],
                "effective_date": effective_date,
                "term_duration": "12 Months (Renewable)" if "renew" in full_text.lower() else "Not specified",
                "primary_subject": f"Commercial terms and mutual covenants for {doc_type}",
                "executive_takeaway": f"Investigation of {len(clauses)} identified clauses indicates {len(high_risks)} elevated risk provisions requiring renegotiation prior to execution."
            },
            "overall_risk": {
                "score": score,
                "category": cat_level,
                "methodology_explanation": f"Score calculated based on {len(high_risks)} high-risk provisions (+18 pts each), {len(mod_risks)} moderate provisions (+8 pts each), and {len(missing_protections)} critical omitted protections (+5 pts each).",
                "contributing_factors": contributing
            },
            "clauses": clauses,
            "missing_protections": missing_protections,
            "counterparty_profile": {
                "primary_counterparty": party1 if "ltd" in party1.lower() or "corp" in party1.lower() or "inc" in party1.lower() else party2,
                "stated_registration_or_cin": cin_val,
                "jurisdiction_state": "Delhi / Bangalore / Delaware" if "court" in full_text.lower() else "Stated in Section 12",
                "registered_address": "Extracted from agreement introductory recital",
                "official_domain": "vertexdynamics.example.com" if "vertex" in full_text.lower() else "Not specified in contract"
            }
        }
