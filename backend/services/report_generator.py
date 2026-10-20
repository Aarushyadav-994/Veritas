import io
import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class ReportGenerator:
    @staticmethod
    def generate_pdf_report(analysis_session: Dict[str, Any]) -> bytes:
        """
        Builds an evidence-driven, publication-grade Legal Intelligence Dossier PDF.
        Includes cross-clause reasoning, 4-tier missing protection status,
        dynamic calculations, and statutory disclaimers.
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Palette constants
        navy = colors.HexColor("#15202B")
        charcoal = colors.HexColor("#263238")
        brass = colors.HexColor("#AD925B")
        slate = colors.HexColor("#667085")
        light_bg = colors.HexColor("#F5F3ED")
        border_color = colors.HexColor("#D0D5DD")
        danger_red = colors.HexColor("#B42318")
        amber = colors.HexColor("#B54708")
        verified_green = colors.HexColor("#067647")

        doc_summary = analysis_session.get("document_summary", {})
        overall_risk = analysis_session.get("overall_risk", {})
        clauses = analysis_session.get("clauses", [])
        cross_clauses = analysis_session.get("cross_clause_analysis", [])
        missing_protections = analysis_session.get("missing_protections", [])
        renewal_timeline = analysis_session.get("renewal_timeline", {})
        financial_analytics = analysis_session.get("financial_analytics", {})
        privacy = analysis_session.get("privacy", {})
        integrity = analysis_session.get("integrity", {})
        tinyfish = analysis_session.get("tinyfish", {})

        score = overall_risk.get("score", 0)
        risk_cat = overall_risk.get("category", "NEEDS REVIEW")

        # =============================================================
        # PAGE 1: EXECUTIVE BRIEF, METHODOLOGY, TIMELINE & COUNTERPARTY
        # =============================================================
        # Header Band
        p.setFillColor(navy)
        p.rect(0, height - 85, width, 85, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(45, height - 38, "VERITAS AI  |  LEGAL INTELLIGENCE DOSSIER")
        p.setFont("Helvetica", 9.5)
        p.setFillColor(brass)
        p.drawString(45, height - 54, "EVIDENCE-GROUNDED CONTRACT INVESTIGATION & RISK AUDIT")

        p.setFont("Helvetica", 8)
        p.setFillColor(colors.HexColor("#D0D5DD"))
        gen_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        p.drawRightString(width - 45, height - 38, f"Ref: VERITAS-{int(datetime.datetime.now().timestamp())}")
        p.drawRightString(width - 45, height - 52, f"Audited: {gen_time}")

        # Metadata Card
        y = height - 110
        p.setFillColor(light_bg)
        p.rect(45, y - 50, width - 90, 50, fill=True, stroke=True)
        p.setStrokeColor(border_color)
        p.setLineWidth(0.5)

        p.setFillColor(charcoal)
        p.setFont("Helvetica-Bold", 8.5)
        p.drawString(55, y - 16, "DOCUMENT TYPE:")
        p.setFont("Helvetica", 8.5)
        p.drawString(160, y - 16, str(doc_summary.get("document_type", "Commercial Agreement"))[:45])

        p.setFont("Helvetica-Bold", 8.5)
        p.drawString(55, y - 30, "SIGNATORIES:")
        parties_str = ", ".join([pt.get("name", "") for pt in doc_summary.get("parties", [])]) or "Stated Signatories"
        p.setFont("Helvetica", 8.5)
        p.drawString(160, y - 30, parties_str[:55])

        p.setFont("Helvetica-Bold", 8.5)
        p.drawString(55, y - 44, "COMPOSITE RISK:")
        p.setFont("Helvetica-Bold", 9.5)
        p.setFillColor(danger_red if score >= 65 else amber if score >= 40 else verified_green)
        p.drawString(160, y - 44, f"{score}/100 - {risk_cat}")

        # Section 1: Executive Brief
        y -= 75
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "1. Executive Intelligence Brief")
        p.setStrokeColor(brass)
        p.setLineWidth(1)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        p.setFillColor(charcoal)
        p.setFont("Helvetica", 8.5)
        takeaway = doc_summary.get("executive_takeaway", "Contract review complete.")
        p.drawString(45, y, takeaway[:115])
        if len(takeaway) > 115:
            y -= 12
            p.drawString(45, y, takeaway[115:230])

        y -= 16
        p.setFont("Helvetica-Bold", 8.5)
        p.drawString(45, y, "Deterministic Scoring Methodology:")
        p.setFont("Helvetica", 8)
        method_text = overall_risk.get("methodology_explanation", "Multi-dimensional weighted model.")
        y -= 11
        p.drawString(45, y, method_text[:115])
        if len(method_text) > 115:
            y -= 11
            p.drawString(45, y, method_text[115:230])

        # Section 2: Calculated Renewal Timeline & Financial Analytics
        y -= 25
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "2. Contract Milestones & Dynamic Financial Calculations")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        p.setFillColor(light_bg)
        p.rect(45, y - 55, width - 90, 55, fill=True, stroke=True)
        p.setStrokeColor(border_color)

        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 8.5)
        p.drawString(55, y - 14, "Renewal Notice Deadline:")
        p.setFont("Helvetica", 8.5)
        p.setFillColor(charcoal)
        deadline_str = renewal_timeline.get("notice_deadline_date", "90 days prior to expiration")
        eff_str = renewal_timeline.get("effective_date", "Effective Date")
        p.drawString(195, y - 14, f"{deadline_str} (Effective: {eff_str})")

        p.setFont("Helvetica-Bold", 8.5)
        p.setFillColor(navy)
        p.drawString(55, y - 28, "Illustrative Liability Cap:")
        p.setFont("Helvetica", 8.5)
        p.setFillColor(charcoal)
        cap_val = financial_analytics.get("liability_cap", {}).get("illustrative_cap_amount", "Calculated dynamically")
        p.drawString(195, y - 28, f"{cap_val} (Subject to 1-month trailing fee formula)")

        p.setFont("Helvetica-Bold", 8.5)
        p.setFillColor(navy)
        p.drawString(55, y - 42, "Late Interest & Dispute:")
        p.setFont("Helvetica", 8)
        p.setFillColor(charcoal)
        pen_info = financial_analytics.get("payment_penalties", {})
        p.drawString(195, y - 42, f"{pen_info.get('stated_rate', '2% per month')} simple ({pen_info.get('simple_annualized_rate', '24% p.a.')}) | {pen_info.get('dispute_window_days', 10)}-day dispute window")

        # Section 3: Counterparty Investigation Status
        y -= 75
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "3. Counterparty Investigation (TinyFish Agent & Public Registries)")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        c_status = tinyfish.get("investigation_status", "Awaiting Execution")
        is_live = tinyfish.get("is_live_execution", False)
        p.setFont("Helvetica-Bold", 8.5)
        p.setFillColor(charcoal)
        p.drawString(45, y, f"Target Legal Entity: {tinyfish.get('entity_searched', 'N/A')}")
        p.drawRightString(width - 45, y, f"Status: {c_status} ({'Live TinyFish Web Agent' if is_live else 'Demo Preset'})")

        y -= 16
        for ev in tinyfish.get("evidence_items", [])[:3]:
            p.setFont("Helvetica-Bold", 8)
            p.setFillColor(navy)
            p.drawString(50, y, f"- {ev.get('source_name', 'Registry Record')}:")
            p.setFont("Helvetica", 7.5)
            p.setFillColor(charcoal)
            y -= 11
            p.drawString(58, y, ev.get("information_retrieved", "")[:110])
            y -= 13

        # Footer page 1
        p.setFont("Helvetica", 7.5)
        p.setFillColor(slate)
        p.drawString(45, 25, "CONFIDENTIAL  |  VERITAS AI  |  DECISION-SUPPORT PLATFORM")
        p.drawRightString(width - 45, 25, "Page 1 of 3")
        p.showPage()

        # =============================================================
        # PAGE 2: CLAUSE AUDIT & CROSS-CLAUSE REASONING
        # =============================================================
        p.setFillColor(navy)
        p.rect(0, height - 50, width, 50, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, height - 32, "CLAUSE-LEVEL RISK AUDIT & VERIFIED EVIDENCE")
        p.drawRightString(width - 45, height - 32, "VERITAS AI DOSSIER")

        y = height - 70
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "4. Key Clause-Level Risk Provisions")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        for cl in clauses[:3]:
            cid = cl.get("clause_id", "Clause")
            cat = cl.get("category", "")
            r_level = cl.get("risk_level", "MODERATE")
            pg = cl.get("page_number", 1)
            ben = cl.get("benefiting_party", "Unspecified")

            p.setFillColor(light_bg)
            p.rect(45, y - 68, width - 90, 68, fill=True, stroke=True)
            p.setStrokeColor(border_color)

            p.setFillColor(navy)
            p.setFont("Helvetica-Bold", 8.5)
            p.drawString(52, y - 13, f"{cid} - {cat} (Page {pg})")

            p.setFont("Helvetica-Bold", 7.5)
            p.setFillColor(danger_red if r_level == "HIGH RISK" else amber if r_level == "MODERATE RISK" else verified_green)
            p.drawRightString(width - 52, y - 13, f"{r_level} | Benefiting: {ben}")

            p.setFillColor(charcoal)
            p.setFont("Helvetica-Oblique", 7.5)
            exc = cl.get("exact_quotation", cl.get("original_excerpt", ""))[:110]
            p.drawString(52, y - 25, f'"{exc}"')

            p.setFont("Helvetica", 7.5)
            p.drawString(52, y - 37, f"Analysis: {cl.get('plain_english_explanation', '')[:105]}")
            p.drawString(52, y - 49, f"Consequence: {cl.get('potential_consequence', '')[:105]}")
            p.drawString(52, y - 61, f"Action: {cl.get('suggested_next_step', '')[:105]}")

            y -= 76

        # Section 5: Cross-Clause Analysis
        y -= 10
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "5. Cross-Clause Dependencies & Compounding Risks")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        for xcl in cross_clauses[:3]:
            p.setFillColor(light_bg)
            p.rect(45, y - 50, width - 90, 50, fill=True, stroke=True)
            p.setStrokeColor(border_color)

            p.setFillColor(navy)
            p.setFont("Helvetica-Bold", 8.5)
            p.drawString(52, y - 13, f"{xcl.get('relationship_type', 'Interaction')} ({', '.join(xcl.get('clauses_involved', []))})")

            p.setFont("Helvetica-Bold", 7.5)
            p.setFillColor(danger_red if xcl.get("risk_severity") == "HIGH RISK" else amber)
            p.drawRightString(width - 52, y - 13, xcl.get("risk_severity", "MODERATE RISK"))

            p.setFillColor(charcoal)
            p.setFont("Helvetica", 7.5)
            analysis_snip = xcl.get("analysis", "")[:110]
            p.drawString(52, y - 27, analysis_snip)
            if len(xcl.get("analysis", "")) > 110:
                p.drawString(52, y - 37, xcl.get("analysis", "")[110:220])

            y -= 58

        # Footer page 2
        p.setFont("Helvetica", 7.5)
        p.setFillColor(slate)
        p.drawString(45, 25, "CONFIDENTIAL  |  VERITAS AI  |  DECISION-SUPPORT PLATFORM")
        p.drawRightString(width - 45, 25, "Page 2 of 3")
        p.showPage()

        # =============================================================
        # PAGE 3: MISSING PROTECTIONS (4-STATE), INTEGRITY & PRIVACY
        # =============================================================
        p.setFillColor(navy)
        p.rect(0, height - 50, width, 50, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, height - 32, "PROTECTIONS MATRIX, INTEGRITY & PRIVACY AUDIT")
        p.drawRightString(width - 45, height - 32, "VERITAS AI DOSSIER")

        y = height - 70
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "6. Defensive Protections Audit (4-State Classification)")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        for mp in missing_protections[:3]:
            st = mp.get("status", "ABSENT")
            p.setFillColor(light_bg)
            p.rect(45, y - 45, width - 90, 45, fill=True, stroke=True)
            p.setStrokeColor(border_color)

            p.setFillColor(navy)
            p.setFont("Helvetica-Bold", 8.5)
            p.drawString(52, y - 13, mp.get("protection_name", "Protection"))

            st_color = verified_green if st == "PRESENT" else amber if st == "PARTIALLY PRESENT" else danger_red
            p.setFont("Helvetica-Bold", 7.5)
            p.setFillColor(st_color)
            p.drawRightString(width - 52, y - 13, f"STATUS: {st}")

            p.setFillColor(charcoal)
            p.setFont("Helvetica", 7.5)
            p.drawString(52, y - 25, f"Finding: {mp.get('why_it_matters', '')[:105]}")
            p.drawString(52, y - 36, f"Residual Gap / Addition: {mp.get('residual_gap', mp.get('recommended_addition', ''))[:105]}")

            y -= 52

        # Section 7: Document Integrity Indicators
        y -= 10
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "7. Document Integrity Indicators & ELA Forensics")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 16
        for ind in integrity.get("indicators", [])[:2]:
            p.setFont("Helvetica", 7.5)
            p.setFillColor(charcoal)
            p.drawString(50, y, f"- {ind.get('finding')}: {ind.get('observed_evidence', '')[:100]}")
            y -= 12

        # Section 8: Statutory Privacy Exposure
        y -= 10
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "8. Personal Data Exposure & Redaction Status")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 16
        p.setFont("Helvetica-Bold", 8)
        p.setFillColor(charcoal)
        p.drawString(45, y, f"Exposure Tier: {privacy.get('overall_exposure', 'LOW')} | Total Detections: {privacy.get('total_detections', 0)}")
        y -= 14
        for pf in privacy.get("findings", [])[:2]:
            p.setFont("Helvetica", 7.5)
            samples = ", ".join(pf.get("masked_samples", []))
            p.drawString(50, y, f"- {pf.get('info_type')}: {pf.get('count')} instance(s) on page(s) {pf.get('pages')}. Masked: {samples}")
            y -= 12

        # Statutory Disclaimer
        y -= 15
        p.setFillColor(colors.HexColor("#EAECF0"))
        p.rect(45, y - 32, width - 90, 32, fill=True, stroke=False)
        p.setFillColor(slate)
        p.setFont("Helvetica-Bold", 7)
        p.drawString(52, y - 10, "IMPORTANT STATUTORY DISCLAIMER:")
        p.setFont("Helvetica", 6.5)
        p.drawString(52, y - 18, "Veritas AI is an automated decision-support utility. It does not establish legal enforceability, signer authenticity,")
        p.drawString(52, y - 26, "or company solvency. All findings and drafted amendments require verification by qualified legal counsel.")

        # Footer page 3
        p.setFont("Helvetica", 7.5)
        p.setFillColor(slate)
        p.drawString(45, 20, "CONFIDENTIAL  |  VERITAS AI  |  DECISION-SUPPORT PLATFORM")
        p.drawRightString(width - 45, 20, "Page 3 of 3")
        p.showPage()

        p.save()
        buffer.seek(0)
        return buffer.getvalue()
