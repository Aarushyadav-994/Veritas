import sys
import os

sys.path.insert(0, os.path.abspath("."))

from backend.services.fixtures import generate_synthetic_contract_pdf
from backend.services.document_extractor import DocumentExtractor
from backend.services.clause_analyzer import ClauseAnalyzer
from backend.services.integrity_analyzer import IntegrityAnalyzer
from backend.services.privacy_scanner import PrivacyScanner
from backend.services.tinyfish_client import TinyFishInvestigator
from backend.services.copilot_service import CopilotService
from backend.services.report_generator import ReportGenerator

def test_pipeline():
    print("1. Generating synthetic test contract PDF...")
    pdf_bytes = generate_synthetic_contract_pdf()
    assert len(pdf_bytes) > 1000, "Synthetic PDF generation failed"
    print(f"   Generated PDF size: {len(pdf_bytes)} bytes")

    print("2. Testing DocumentExtractor...")
    doc_data = DocumentExtractor.extract_document(pdf_bytes, "test_contract.pdf")
    assert doc_data["page_count"] >= 1, "Page count must be >= 1"
    assert len(doc_data["full_text"]) > 200, "Text extraction must have content"
    print(f"   Extracted {doc_data['page_count']} pages, {len(doc_data['full_text'])} characters")

    print("3. Testing ClauseAnalyzer...")
    analysis = ClauseAnalyzer.analyze_document(doc_data["full_text"], doc_data["pages"])
    assert "clauses" in analysis and len(analysis["clauses"]) > 0, "Clauses must be extracted"
    assert "overall_risk" in analysis, "Overall risk must be calculated"
    print(f"   Extracted {len(analysis['clauses'])} clauses. Overall Risk: {analysis['overall_risk']['score']}/100 ({analysis['overall_risk']['category']})")

    print("4. Testing IntegrityAnalyzer...")
    integrity = IntegrityAnalyzer.analyze_pdf_integrity(doc_data["metadata"], pdf_bytes)
    assert "indicators" in integrity, "Indicators must be present"
    assert "ela" in integrity, "ELA must be present"
    print(f"   Integrity status: {integrity['overall_integrity_status']}, {len(integrity['indicators'])} indicators")

    print("5. Testing PrivacyScanner...")
    privacy = PrivacyScanner.scan_document(doc_data["pages"])
    assert "findings" in privacy, "Privacy findings must be present"
    print(f"   Privacy exposure: {privacy['overall_exposure']}, {privacy['total_detections']} detections")

    print("6. Testing Redaction...")
    redacted = PrivacyScanner.generate_redacted_pdf(pdf_bytes, doc_data["pages"])
    assert len(redacted) > 500, "Redacted PDF failed"
    print(f"   Redacted PDF size: {len(redacted)} bytes")

    print("7. Testing TinyFishInvestigator...")
    tf = TinyFishInvestigator.investigate_entity("Vertex Dynamics Technologies Private Limited")
    assert "investigation_status" in tf, "TinyFish response missing status"
    print(f"   TinyFish status: {tf['investigation_status']}, {len(tf['evidence_items'])} evidence records")

    print("8. Testing CopilotService Q&A & Redraft...")
    q_res = CopilotService.answer_question("How can I terminate this agreement?", doc_data["full_text"], analysis["clauses"])
    assert len(q_res["answer"]) > 50, "Copilot answer failed"
    print(f"   Copilot answered with {len(q_res['answer'])} chars, cited: {q_res['cited_clauses']}")

    redraft = CopilotService.redraft_clause(
        clause_id="Clause 4.1",
        category="Termination",
        original_excerpt="Service Provider may terminate this Agreement at any time, with or without cause, immediately upon delivering written email notice to Client."
    )
    assert len(redraft["proposed_alternative"]) > 50, "Redraft clause failed"
    print(f"   Redrafted clause alternative: {len(redraft['proposed_alternative'])} chars")

    print("9. Testing ReportGenerator PDF output...")
    session_payload = {
        "document_summary": analysis["document_summary"],
        "overall_risk": analysis["overall_risk"],
        "clauses": analysis["clauses"],
        "privacy": privacy,
        "integrity": integrity,
        "tinyfish": tf
    }
    report_pdf = ReportGenerator.generate_pdf_report(session_payload)
    assert len(report_pdf) > 2000, "Report PDF generation failed"
    print(f"   Report PDF generated successfully: {len(report_pdf)} bytes")

    print("\nALL BACKEND SERVICES TESTED AND PASSING!")

if __name__ == "__main__":
    test_pipeline()
