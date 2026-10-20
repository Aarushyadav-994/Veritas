import uuid
import os
import io
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.config import settings
from backend.services.document_extractor import DocumentExtractor, DocumentExtractionError
from backend.services.clause_analyzer import ClauseAnalyzer
from backend.services.integrity_analyzer import IntegrityAnalyzer
from backend.services.privacy_scanner import PrivacyScanner
from backend.services.tinyfish_client import TinyFishInvestigator
from backend.services.copilot_service import CopilotService
from backend.services.report_generator import ReportGenerator
from backend.services.fixtures import generate_synthetic_contract_pdf, SYNTHETIC_CONTRACT_TEXT

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Legal Document Intelligence & Forensic Investigation API"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session-scoped store
# Keeps processing in memory and avoids unnecessary permanent persistence
sessions: Dict[str, Dict[str, Any]] = {}
session_raw_bytes: Dict[str, bytes] = {}

class InvestigateRequest(BaseModel):
    session_id: str
    entity_name: str
    registration_id: Optional[str] = None
    jurisdiction: Optional[str] = None

class CopilotAskRequest(BaseModel):
    session_id: str
    question: str

class RedraftRequest(BaseModel):
    session_id: str
    clause_id: str
    category: str
    original_excerpt: str
    negotiation_goal: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key.strip()),
        "tinyfish_configured": bool(settings.tinyfish_api_key.strip()),
        "active_sessions": len(sessions)
    }

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_contract.pdf"
    content = await file.read()

    try:
        extraction = DocumentExtractor.extract_document(content, filename)
    except DocumentExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected document parsing failure: {str(e)}")

    session_id = str(uuid.uuid4())
    session_raw_bytes[session_id] = content

    # 1. Clause Analysis
    clause_analysis = ClauseAnalyzer.analyze_document(extraction["full_text"], extraction["pages"])

    # 2. Integrity Analysis
    integrity_analysis = IntegrityAnalyzer.analyze_pdf_integrity(extraction["metadata"], content)

    # 3. Privacy Scan
    privacy_analysis = PrivacyScanner.scan_document(extraction["pages"])

    # 4. Initial Counterparty Extraction
    counterparty_profile = clause_analysis.get("counterparty_profile", {})
    primary_entity = counterparty_profile.get("primary_counterparty", "Identified Signatory")
    stated_cin = counterparty_profile.get("stated_registration_or_cin", "")

    # Pre-run or prepare TinyFish investigation profile
    tinyfish_result = TinyFishInvestigator.investigate_entity(
        entity_name=primary_entity,
        registration_id=stated_cin
    )

    session_data = {
        "session_id": session_id,
        "filename": filename,
        "document_type": extraction["document_type"],
        "page_count": extraction["page_count"],
        "metadata": extraction["metadata"],
        "pages": extraction["pages"],
        "full_text": extraction["full_text"],
        "preview_images": extraction.get("preview_images", []),
        "document_summary": clause_analysis.get("document_summary", {}),
        "overall_risk": clause_analysis.get("overall_risk", {}),
        "clauses": clause_analysis.get("clauses", []),
        "missing_protections": clause_analysis.get("missing_protections", []),
        "counterparty_profile": counterparty_profile,
        "integrity": integrity_analysis,
        "privacy": privacy_analysis,
        "tinyfish": tinyfish_result,
        "analysis_engine": clause_analysis.get("engine", "Heuristic")
    }

    sessions[session_id] = session_data

    return session_data

@app.post("/api/demo")
def load_demo():
    """
    Instantly loads the prepared synthetic enterprise agreement fixture with
    real unfavorable provisions, personal details, and integrity indicators.
    """
    pdf_bytes = generate_synthetic_contract_pdf()
    filename = "Veritas_Sample_Cloud_Services_Agreement.pdf"

    extraction = DocumentExtractor.extract_document(pdf_bytes, filename)
    session_id = str(uuid.uuid4())
    session_raw_bytes[session_id] = pdf_bytes

    clause_analysis = ClauseAnalyzer.analyze_document(extraction["full_text"], extraction["pages"])
    integrity_analysis = IntegrityAnalyzer.analyze_pdf_integrity(extraction["metadata"], pdf_bytes)
    privacy_analysis = PrivacyScanner.scan_document(extraction["pages"])

    counterparty_profile = clause_analysis.get("counterparty_profile", {})
    primary_entity = "Vertex Dynamics Technologies Private Limited"
    stated_cin = "U72900DL2021PTC384910"

    tinyfish_result = TinyFishInvestigator.investigate_entity(
        entity_name=primary_entity,
        registration_id=stated_cin
    )

    session_data = {
        "session_id": session_id,
        "is_demo": True,
        "filename": filename,
        "document_type": extraction["document_type"],
        "page_count": extraction["page_count"],
        "metadata": extraction["metadata"],
        "pages": extraction["pages"],
        "full_text": extraction["full_text"],
        "preview_images": extraction.get("preview_images", []),
        "document_summary": clause_analysis.get("document_summary", {}),
        "overall_risk": clause_analysis.get("overall_risk", {}),
        "clauses": clause_analysis.get("clauses", []),
        "missing_protections": clause_analysis.get("missing_protections", []),
        "counterparty_profile": counterparty_profile,
        "integrity": integrity_analysis,
        "privacy": privacy_analysis,
        "tinyfish": tinyfish_result,
        "analysis_engine": clause_analysis.get("engine", "Veritas Deterministic Legal Engine")
    }

    sessions[session_id] = session_data
    return session_data

@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session expired or not found.")
    return sessions[session_id]

@app.post("/api/investigate")
def run_investigation(req: InvestigateRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session expired or not found.")

    res = TinyFishInvestigator.investigate_entity(
        entity_name=req.entity_name,
        registration_id=req.registration_id,
        jurisdiction=req.jurisdiction
    )

    sessions[req.session_id]["tinyfish"] = res
    return res

@app.post("/api/copilot/ask")
def copilot_ask(req: CopilotAskRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session expired or not found.")

    session = sessions[req.session_id]
    ans = CopilotService.answer_question(
        question=req.question,
        full_text=session["full_text"],
        clauses=session["clauses"]
    )
    return ans

@app.post("/api/copilot/redraft")
def copilot_redraft(req: RedraftRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session expired or not found.")

    res = CopilotService.redraft_clause(
        clause_id=req.clause_id,
        category=req.category,
        original_excerpt=req.original_excerpt,
        negotiation_goal=req.negotiation_goal
    )
    return res

@app.get("/api/redact/{session_id}")
def download_redacted_pdf(session_id: str):
    if session_id not in sessions or session_id not in session_raw_bytes:
        raise HTTPException(status_code=404, detail="Session not found.")

    session = sessions[session_id]
    raw_bytes = session_raw_bytes[session_id]

    redacted_pdf = PrivacyScanner.generate_redacted_pdf(raw_bytes, session["pages"])
    return Response(
        content=redacted_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=REDACTED_{session['filename']}"}
    )

@app.get("/api/export/pdf/{session_id}")
def export_report_pdf(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")

    pdf_report = ReportGenerator.generate_pdf_report(sessions[session_id])
    return Response(
        content=pdf_report,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Veritas_Intelligence_Report_{session_id[:8]}.pdf"}
    )

@app.post("/api/session/{session_id}/reset")
def reset_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    if session_id in session_raw_bytes:
        del session_raw_bytes[session_id]
    return {"status": "success", "message": "Analysis session purged from server memory."}
