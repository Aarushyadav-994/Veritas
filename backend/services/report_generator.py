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
        Builds a comprehensive, publication-grade Legal Intelligence Brief PDF.
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Color Palette constants
        navy = colors.HexColor("#15202B")
        charcoal = colors.HexColor("#263238")
        brass = colors.HexColor("#AD925B")
        slate = colors.HexColor("#667085")
        light_bg = colors.HexColor("#F5F3ED")
        danger_red = colors.HexColor("#B42318")
        amber = colors.HexColor("#B54708")
        verified_green = colors.HexColor("#067647")

        doc_summary = analysis_session.get("document_summary", {})
        overall_risk = analysis_session.get("overall_risk", {})
        clauses = analysis_session.get("clauses", [])
        privacy = analysis_session.get("privacy", {})
        integrity = analysis_session.get("integrity", {})
        tinyfish = analysis_session.get("tinyfish", {})

        score = overall_risk.get("score", 0)
        risk_cat = overall_risk.get("category", "NEEDS REVIEW")

        # PAGE 1: COVER & EXECUTIVE SUMMARY
        # Header Band
        p.setFillColor(navy)
        p.rect(0, height - 90, width, 90, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 18)
        p.drawString(45, height - 42, "VERITAS AI  |  LEGAL INTELLIGENCE DOSSIER")
        p.setFont("Helvetica", 10)
        p.setFillColor(brass)
        p.drawString(45, height - 60, "FORENSIC CONTRACT ANALYSIS & COUNTERPARTY AUDIT")

        p.setFont("Helvetica", 8)
        p.setFillColor(colors.HexColor("#D0D5DD"))
        gen_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        p.drawRightString(width - 45, height - 42, f"Brief Ref: VERITAS-{int(datetime.datetime.now().timestamp())}")
        p.drawRightString(width - 45, height - 58, f"Generated: {gen_time}")

        # Meta bar
        y = height - 120
        p.setFillColor(light_bg)
        p.rect(45, y - 55, width - 90, 60, fill=True, stroke=True)
        p.setStrokeColor(colors.HexColor("#D0D5DD"))
        p.setLineWidth(0.5)

        p.setFillColor(charcoal)
        p.setFont("Helvetica-Bold", 9)
        p.drawString(55, y - 16, "DOCUMENT TYPE:")
        p.setFont("Helvetica", 9)
        p.drawString(160, y - 16, str(doc_summary.get("document_type", "Commercial Agreement"))[:45])

        p.setFont("Helvetica-Bold", 9)
        p.drawString(55, y - 32, "COUNTERPARTIES:")
        parties_str = ", ".join([p.get("name", "") for p in doc_summary.get("parties", [])]) or "Stated Signatories"
        p.setFont("Helvetica", 9)
        p.drawString(160, y - 32, parties_str[:55])

        p.setFont("Helvetica-Bold", 9)
        p.drawString(55, y - 48, "OVERALL RISK:")
        p.setFont("Helvetica-Bold", 10)
        p.setFillColor(danger_red if score >= 65 else amber if score >= 40 else verified_green)
        p.drawString(160, y - 48, f"{score}/100 — {risk_cat}")

        # Executive Summary Section
        y -= 85
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 13)
        p.drawString(45, y, "1. Executive Intelligence Brief")
        p.setStrokeColor(brass)
        p.setLineWidth(1)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 22
        p.setFillColor(charcoal)
        p.setFont("Helvetica", 9)
        takeaway = doc_summary.get("executive_takeaway", "Contract review complete.")
        p.drawString(45, y, takeaway[:110])
        if len(takeaway) > 110:
            y -= 14
            p.drawString(45, y, takeaway[110:220])

        y -= 20
        p.setFont("Helvetica-Bold", 9)
        p.drawString(45, y, "Scoring Methodology:")
        p.setFont("Helvetica", 8.5)
        method_text = overall_risk.get("methodology_explanation", "Weighted risk factors.")
        y -= 13
        p.drawString(45, y, method_text[:115])
        if len(method_text) > 115:
            y -= 13
            p.drawString(45, y, method_text[115:230])

        # Risk Factors Matrix
        y -= 30
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 13)
        p.drawString(45, y, "2. Key Contributing Risk Factors")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 20
        factors = overall_risk.get("contributing_factors", [])[:4]
        for f in factors:
            p.setFillColor(danger_red if f.get("impact") == "HIGH" else amber)
            p.rect(45, y - 2, 6, 6, fill=True, stroke=False)
            p.setFillColor(charcoal)
            p.setFont("Helvetica-Bold", 9)
            p.drawString(58, y - 2, f.get("factor", "")[:60])
            p.setFont("Helvetica", 8.5)
            y -= 13
            p.drawString(58, y - 2, f.get("detail", "")[:105])
            y -= 16

        # Counterparty section preview
        y -= 15
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 13)
        p.drawString(45, y, "3. Counterparty Investigation (TinyFish / Registry)")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 22
        c_status = tinyfish.get("investigation_status", "Not Evaluated")
        p.setFont("Helvetica-Bold", 9)
        p.setFillColor(charcoal)
        p.drawString(45, y, f"Target Entity: {tinyfish.get('entity_searched', 'N/A')}")
        p.drawRightString(width - 45, y, f"Status: {c_status}")

        y -= 16
        for ev in tinyfish.get("evidence_items", [])[:2]:
            p.setFont("Helvetica-Bold", 8.5)
            p.setFillColor(navy)
            p.drawString(50, y, f"• {ev.get('source_name', 'Registry Source')}:")
            p.setFont("Helvetica", 8)
            p.setFillColor(charcoal)
            y -= 12
            p.drawString(58, y, ev.get("information_retrieved", "")[:105])
            y -= 16

        # Footer page 1
        p.setFont("Helvetica", 8)
        p.setFillColor(slate)
        p.drawString(45, 30, "CONFIDENTIAL  |  VERITAS AI  |  DECISION-SUPPORT SYSTEM ONLY")
        p.drawRightString(width - 45, 30, "Page 1 of 2")
        p.showPage()

        # PAGE 2: CLAUSE BREAKDOWN & PRIVACY AUDIT
        # Header
        p.setFillColor(navy)
        p.rect(0, height - 50, width, 50, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, height - 32, "CLAUSE AUDIT, INTEGRITY & PRIVACY EXPOSURE FINDINGS")
        p.drawRightString(width - 45, height - 32, "VERITAS AI REPORT")

        y = height - 75
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "4. Clause-Level Risk Analysis")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 20
        for idx, cl in enumerate(clauses[:4]):
            cid = cl.get("clause_id", f"Clause {idx+1}")
            cat = cl.get("category", "")
            r_level = cl.get("risk_level", "MODERATE")
            pg = cl.get("page_number", 1)

            # Box per clause
            p.setFillColor(light_bg)
            p.rect(45, y - 65, width - 90, 65, fill=True, stroke=True)
            p.setStrokeColor(colors.HexColor("#D0D5DD"))

            # Header row
            p.setFillColor(navy)
            p.setFont("Helvetica-Bold", 9)
            p.drawString(55, y - 14, f"{cid} — {cat} (Page {pg})")

            p.setFillColor(danger_red if r_level == "HIGH RISK" else amber if r_level == "MODERATE RISK" else verified_green)
            p.drawRightString(width - 55, y - 14, r_level)

            p.setFillColor(charcoal)
            p.setFont("Helvetica-Oblique", 7.5)
            exc = cl.get("original_excerpt", "")[:100] + ("..." if len(cl.get("original_excerpt", "")) > 100 else "")
            p.drawString(55, y - 26, f'"{exc}"')

            p.setFont("Helvetica", 8)
            p.drawString(55, y - 38, f"Explanation: {cl.get('plain_english_explanation', '')[:95]}")
            p.drawString(55, y - 50, f"Suggested Step: {cl.get('suggested_next_step', '')[:95]}")

            y -= 75

        # Privacy Audit Section
        y -= 10
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "5. Privacy Exposure & Data Security Audit")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 18
        p.setFont("Helvetica-Bold", 9)
        p.setFillColor(charcoal)
        p.drawString(45, y, f"Overall Data Exposure Rating: {privacy.get('overall_exposure', 'LOW')}")
        p.drawString(250, y, f"Total Detected PII Items: {privacy.get('total_detections', 0)}")

        y -= 16
        for pf in privacy.get("findings", [])[:3]:
            p.setFont("Helvetica", 8)
            samples = ", ".join(pf.get("masked_samples", []))
            p.drawString(50, y, f"• {pf.get('info_type')}: {pf.get('count')} instances (Pages: {pf.get('pages')}). Masked: {samples}")
            y -= 13

        # Integrity indicators
        y -= 10
        p.setFillColor(navy)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(45, y, "6. Document Integrity Indicators")
        p.setStrokeColor(brass)
        p.line(45, y - 4, width - 45, y - 4)

        y -= 16
        for ind in integrity.get("indicators", [])[:2]:
            p.setFont("Helvetica", 8)
            p.drawString(50, y, f"• {ind.get('finding')}: {ind.get('observed_evidence', '')[:95]}")
            y -= 12

        # Legal Disclaimer
        y -= 15
        p.setFillColor(colors.HexColor("#EAECF0"))
        p.rect(45, y - 35, width - 90, 35, fill=True, stroke=False)
        p.setFillColor(slate)
        p.setFont("Helvetica-Bold", 7.5)
        p.drawString(55, y - 12, "IMPORTANT STATUTORY DISCLAIMER:")
        p.setFont("Helvetica", 7)
        p.drawString(55, y - 22, "Veritas AI is an automated decision-support utility. It does not establish legal enforceability, signer authenticity,")
        p.drawString(55, y - 30, "or company solvency. All findings and drafted amendments require verification by qualified legal counsel.")

        # Footer page 2
        p.setFont("Helvetica", 8)
        p.setFillColor(slate)
        p.drawString(45, 25, "CONFIDENTIAL  |  VERITAS AI  |  DECISION-SUPPORT SYSTEM ONLY")
        p.drawRightString(width - 45, 25, "Page 2 of 2")
        p.showPage()

        p.save()
        buffer.seek(0)
        return buffer.getvalue()
