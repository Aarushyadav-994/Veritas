# VERITAS AI: HACKATHON SUBMISSION CHECKLIST

## 1. Project Information
- **Project Name:** Veritas AI
- **Tagline:** Don't Just Read the Contract. Investigate It.
- **Event:** Kritical Hacks 2026
- **Category:** Agentic AI / LegalTech / Document Intelligence
- **Repository:** https://github.com/Aarushyadav-994/Veritas.git
- **Primary Branch:** `main`

---

## 2. Core Technical Architecture
- **Frontend:** Next.js 16.4.2 (Turbopack, React 19, Tailwind CSS) running on `http://localhost:3000`
- **Backend:** FastAPI (Python 3.11+, Uvicorn daemon) running on `http://localhost:8000`
- **Document Analysis Engine:** Deterministic evidence-grounded parser with 13-field clause segmentation
- **Forensics & Redaction:** PyMuPDF (`fitz`), Pillow, Error Level Analysis (ELA)
- **External Web Investigation:** Official TinyFish SDK (`tinyfish.TinyFish.search.query`)
- **Dossier Compilation:** ReportLab multi-page publication-ready PDF generator

---

## 3. Automated Test Verification Results
- **Command:** `source venv/bin/activate && python backend/test_backend.py`
- **Result:** 12 passed, 0 failed, 0 errors (Exit code 0)
- **Verified Requirements:**
  - Test A: Document Extraction (Master Cloud Services Agreement, Parties, Dates, Fees) - Pass
  - Test B: Liability Cap Calculation (Trailing 1-month fee, INR 15k estimate vs INR 10k cap) - Pass
  - Test C: Termination Asymmetry (45-day vendor exit vs 100% early termination fee lock-in) - Pass
  - Test D: Automatic Renewal Timeline (Initial term end 30 Sep 2027, notice deadline 02 July 2027) - Pass
  - Test E: Existing Damages Waiver (Section 6.1 classified as PARTIALLY PRESENT, not absent) - Pass
  - Test F: Cross-Clause Reasoning (Liability cap paired with uncapped indemnity flagged as HIGH RISK) - Pass
  - Test G: Quotation Verification (EvidenceVerifier confirms verbatim match against text stream) - Pass
  - Test H: Payment Interest Calculation (2% monthly annualized to 24% simple rate, 10-day invoice dispute window) - Pass
  - Test I: Absent Protections (Source code escrow and SLA credits classified as ABSENT) - Pass
  - Test J: Contract Generalization (Mutual NDA fixture dynamically yields 18/100 risk score) - Pass
  - Test K: PDF Report Generation (ReportLab dossier verified with zero localhost URLs) - Pass
  - Test L: External Service Degradation (Unconfigured and invalid key fallback modes verified) - Pass

---

## 4. TinyFish Integration Verification
- **SDK Implementation:** [`backend/services/tinyfish_client.py`](file:///Users/aarushyadav/Desktop/Law_Hack/backend/services/tinyfish_client.py)
- **Endpoint:** `client.search.query(query=reg_query)`
- **Query Structure:** Target legal entity name + corporate identification number (CIN)
- **Execution Evidence:** Real queries executed against corporate registries; returns active registration standing, incorporator data, and citation URLs.
- **Fallback Transparency:** When `TINYFISH_API_KEY` is not present, the UI clearly displays "Transparent Demo Preset" with explicit notification, avoiding deceptive mock presentation.

---

## 5. Security & Data Integrity Audit
- **Credentials:** Zero secrets or API keys are committed to Git. `.env` is ignored by `.gitignore`.
- **Environment Template:** `.env.example` contains only non-sensitive empty placeholders.
- **Permanent Redaction:** Verified via PyMuPDF binary text stream removal (`page.apply_redactions()`). Redacted values (PAN, Aadhaar, phone, email, bank details) cannot be recovered through text extraction.
- **Volatile Processing:** Document bytes exist in memory during active session only; no persistent database storage of uploaded contracts.

---

## 6. Known Limitations
- **Optical Character Recognition (OCR):** Image files and scanned PDFs rely on text layer presence; for purely rasterized scans without embedded OCR text, full OCR requires an installed Tesseract / Google Vision pipeline.
- **External Network Dependency:** Live TinyFish investigation requires internet access to `agent.tinyfish.ai`. If the network is unavailable or credentials expire, the application automatically uses the transparent demo mode.
- **Legal Disclaimer:** The platform is an automated decision-support utility and does not constitute formal legal counsel.

---

## 7. Pre-Submission Verification Steps for User
1. Verify both servers are running:
   - Backend: `curl -s http://localhost:8000/api/health`
   - Frontend: Visit `http://localhost:3000` in browser
2. Run test suite: `source venv/bin/activate && python backend/test_backend.py`
3. Click "Load Sample Contract" and confirm the 81/100 risk score and 02 July 2027 renewal deadline appear.
4. Test "Download Redacted PDF" from the Privacy tab.
5. Test "Export PDF Dossier" from the top header.
6. Record demo video following `DEMO_SCRIPT.md`.
7. Review `SOCIAL_POST_DRAFT.md` before publishing.
