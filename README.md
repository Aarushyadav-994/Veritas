# VERITAS AI

**Legal Document Intelligence and Forensic Investigation Platform**

> Tagline: "Don't Just Read the Contract. Investigate It."  
> Event: Kritical Hacks 2026  
> Category: Agentic AI / LegalTech / Document Intelligence  

---

## 1. Executive Overview

Veritas AI is an end-to-end legal intelligence platform and investigative workstation. Traditional contract review tools restrict their scope to basic summarization. Veritas AI evaluates agreements from multiple investigative perspectives:

1. **Contract Intelligence Engine:** Extracts clause-level risks across critical categories including unilateral termination, automatic renewal roll-overs, uncapped indemnities, and liability suppressions.
2. **Document Integrity and Forensic Analysis:** Inspects internal PDF dictionary streams, generation timestamps, author signatures, consumer editing footprints, and applies Error Level Analysis (ELA) to expose image compression variance maps.
3. **Statutory Privacy Exposure Audit:** Identifies sensitive Personally Identifiable Information (PAN cards, Aadhaar numbers, phone numbers, email addresses, and banking credentials) and provides cryptographic, permanent byte-level PDF redaction.
4. **Autonomous Counterparty Investigation (TinyFish):** Integrates autonomous browser agents via the TinyFish Agent API to verify stated entities, corporate registration numbers (CIN), GSTIN records, and official domain registrations against public registries.
5. **Contextual Legal Copilot and Clause Redrafter:** Provides document-grounded legal question answering with explicit clause citations, along with an interactive negotiation redrafter that generates commercially balanced counter-proposals.
6. **Unified Legal Intelligence Report:** Compiles all findings into a structured interactive workstation and generates publication-grade PDF intelligence briefs via ReportLab.

---

## 2. Design Philosophy and Visual Identity

Veritas AI avoids generic artificial intelligence dashboard patterns (such as purple gradients, floating orbs, glassmorphism, or repetitive cards). The platform is constructed as a bespoke legal analyst workstation:

- **Palette:**
  - Deep Ink Navy: `#15202B`
  - Charcoal: `#263238`
  - Warm Paper: `#F5F3ED`
  - White: `#FFFFFF`
  - Muted Brass: `#AD925B`
  - Slate: `#667085`
  - High-Risk Red: `#B42318`
  - Warning Amber: `#B54708`
  - Verified Green: `#067647`

- **Typography and Structure:**
  - Editorial serif headers paired with clean tabular monospace numerals and clause references.
  - Subtle borders, clear separators, and purposeful contrast over heavy shadows.
  - Compact navigation, prominent document workspace, filterable clause risk matrix, and contextual action drawers placed adjacent to the data they affect.

---

## 3. System Architecture

```text
+-------------------------------------------------------------+
|            Next.js 16 + React 19 + Tailwind CSS             |
|              (Legal Analyst Workstation UI)                 |
+------------------------------+------------------------------+
                               | HTTP / JSON / Binary Streams
                               v
+-------------------------------------------------------------+
|                FastAPI Python Backend Engine                |
|                    (Port 8000 / Uvicorn)                    |
+-------+------------------+-------------------+--------------+
        |                  |                   |
        v                  v                   v
+---------------+  +---------------+   +---------------+
| PyMuPDF / PIL |  | Clause / PII  |   |   TinyFish    |
| Extraction &  |  | Heuristics &  |   |   Web Agent   |
|   ELA Maps    |  | True Redactor |   | Investigation |
+---------------+  +---------------+   +---------------+
        |                                      |
        v                                      v
+---------------+                      +---------------+
| ReportLab PDF |                      | Google Gemini |
| Intelligence  |                      | LLM Copilot & |
| Dossier Gen   |                      | Schema Parser |
+---------------+                      +---------------+
```

---

## 4. Repository Structure

```text
Law_Hack/
|-- backend/
|   |-- config.py                   # Environment settings and application configuration
|   |-- main.py                     # FastAPI application endpoints, routing, CORS, session state
|   |-- test_backend.py             # Comprehensive automated verification test suite
|   |-- services/
|       |-- clause_analyzer.py      # Clause segmentation, risk grading, and omitted covenants
|       |-- copilot_service.py      # Grounded question-answering and bilateral redrafting
|       |-- document_extractor.py   # Multi-format PDF and image text/metadata extraction
|       |-- fixtures.py             # Synthetic enterprise contract generator for instant demos
|       |-- integrity_analyzer.py   # PDF metadata forensics and Error Level Analysis (ELA)
|       |-- privacy_scanner.py      # PII detection and permanent binary PDF redaction
|       |-- report_generator.py     # Multi-page ReportLab PDF brief compilation
|       |-- tinyfish_client.py      # Real TinyFish agentic web investigation and mock fallbacks
|-- frontend/
|   |-- src/
|       |-- app/
|           |-- globals.css         # Bespoke color variables, scrollbar styling, typography
|           |-- layout.tsx          # Root layout and metadata configuration
|           |-- page.tsx            # Main application dashboard and state orchestration
|       |-- components/
|           |-- ClauseFindingsTab.tsx    # Filterable clause risk table with excerpt blocks
|           |-- ContractOverviewBar.tsx  # Document summary bar and transparent risk index
|           |-- CopilotDrawer.tsx        # Document-grounded Q&A assistant drawer
|           |-- DocumentReaderTab.tsx    # Page-by-page text stream and visual page viewer
|           |-- Header.tsx               # Top workstation toolbar and actions
|           |-- IntegrityTab.tsx         # Metadata forensic audit and interactive ELA viewer
|           |-- PrivacyTab.tsx           # PII disclosure audit and redacted PDF download
|           |-- RedraftModal.tsx         # Interactive alternative clause redrafting modal
|           |-- TinyFishTab.tsx          # Autonomous counterparty investigation terminal
|           |-- UploadWorkspace.tsx      # Drag-and-drop document ingestion terminal
|   |-- package.json
|   |-- tsconfig.json
|-- requirements.txt                # Python backend dependencies
|-- .env.example                    # Environment variable configuration template
|-- .gitignore                      # Git ignore patterns
|-- README.md                       # Comprehensive platform documentation
```

---

## 5. Detailed Component Specifications

### 5.1 Document Ingestion and Extraction (`document_extractor.py`)
- Accepts PDF, PNG, and JPEG documents up to 25 MB.
- Inspects document streams using PyMuPDF (`fitz`) and Pillow.
- Extracts page text, character counts, word counts, and structural metadata.
- Validates against empty files, unsupported extensions, and password-protected files with user-facing error reporting.

### 5.2 Contract Intelligence Engine (`clause_analyzer.py`)
- Segments agreements into standard commercial categories:
  - Termination
  - Automatic Renewal
  - Payment and Penalties
  - Indemnification
  - Liability Limitations
  - Intellectual Property
  - Dispute Resolution and Jurisdiction
  - Unilateral Amendment Rights
- Analyzes each provision for unfavorable asymmetric language.
- Classifies risk into four distinct tiers:
  - `HIGH RISK`: Significant financial or operational vulnerability.
  - `MODERATE RISK`: Restrictive or unbalanced commercial language.
  - `LOW APPARENT RISK`: Standard mutualized terms.
  - `NEEDS REVIEW`: Requires specific legal or factual clarification.
- Identifies missing protections (such as mutual consequential damages exclusions or mandatory cure periods).
- Computes an overall transparent risk index (0 to 100) with full mathematical attribution.

### 5.3 Document Integrity Analysis and ELA (`integrity_analyzer.py`)
- Audits PDF dictionaries for timestamp discrepancies between CreationDate and ModDate.
- Scans producer and creator tags for signatures of consumer-grade editors (Canva, Photoshop, iLovePDF).
- Detects font diversity anomalies that may suggest spliced sections or post-hoc alterations.
- Computes Error Level Analysis (ELA) on primary surfaces:
  - Re-encodes the surface at a fixed JPEG quality of 90.
  - Measures the pixel difference against the input image.
  - Amplifies differences by a factor of 15 to highlight compression variances.
  - Displays results via an interactive comparison viewer with forensic disclaimers.

### 5.4 Privacy Exposure Audit and True Redaction (`privacy_scanner.py`)
- Detects sensitive identifiers:
  - Permanent Account Numbers (PAN)
  - Aadhaar Identification Numbers (with UIDAI masking)
  - Telephone and mobile numbers
  - Email addresses
  - Bank account numbers (with contextual validation)
  - Indian Financial System Codes (IFSC)
- Rates exposure risk and suggests mitigations.
- Generates genuine redacted PDFs using PyMuPDF's `apply_redactions()` method, ensuring underlying characters and binary streams are scrubbed and unrecoverable.

### 5.5 Autonomous Counterparty Investigation (`tinyfish_client.py`)
- Extracts primary counterparty names and corporate registration identifiers.
- Implements the TinyFish Agent API (`https://agent.tinyfish.ai/v1/automation/run` via the `tinyfish` Python SDK).
- Directs autonomous web agents to verify legal entity standing across public registries and domain footprints.
- Returns evidence records with source titles, URLs, timestamps, verification statuses, and limitations.
- Automatically enables a transparent, explicitly labeled simulated mode if `TINYFISH_API_KEY` is not configured.

### 5.6 Contextual Legal Copilot (`copilot_service.py`)
- Contextual assistant operating strictly over the current contract text and segmented clauses.
- References exact clause identifiers and page numbers in its responses.
- Explicitly reports when a requested topic is absent from the agreement.
- Offers interactive clause redrafting: transforms one-sided clauses into balanced, bilateral drafts with tactical negotiation notes and a copy action.

### 5.7 Unified Report Generation (`report_generator.py`)
- Generates a publication-ready legal intelligence brief in PDF format using ReportLab.
- Formats the dossier with an executive summary, risk index breakdown, counterparty findings, clause analysis, integrity indicators, privacy audit, and statutory disclaimers.

---

## 6. Installation and Setup

### 6.1 Prerequisites
- Python 3.11 or later
- Node.js 18 or later, with npm

### 6.2 Backend Setup
```bash
# Clone the repository
git clone https://github.com/Aarushyadav-994/Veritas.git
cd Veritas

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start the FastAPI backend server
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
The backend API will be accessible at `http://localhost:8000`.  
Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### 6.3 Frontend Setup
```bash
# In a new terminal window, navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Next.js development server
npm run dev -- --port 3000
```
The Veritas AI workstation will be accessible at `http://localhost:3000`.

---

## 7. Configuration and Environment Variables

Copy `.env.example` to `.env` in the project root:

```bash
# Google Gemini API Key (Optional)
# If omitted, Veritas AI uses its local Deterministic Legal Heuristic Engine
GEMINI_API_KEY=""
GEMINI_MODEL="gemini-2.5-flash"

# TinyFish Web Agent API Key (Optional)
# If omitted, Veritas AI activates transparent simulated registry mode
TINYFISH_API_KEY=""

# Maximum upload file size in Megabytes (Default: 25)
MAX_UPLOAD_SIZE_MB=25
```

### Transparent Demonstration Mode
Veritas AI does not require external API credentials to run. When API keys are unset:
- The local deterministic heuristic engine segments clauses, calculates risk scores, and detects missing protections.
- The TinyFish module displays transparently labeled demonstration registry results.
- The legal copilot executes grounded contextual retrieval over the document text.
- Adding valid credentials automatically activates live cloud model calls and live TinyFish web agents.

---

## 8. API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check, active sessions count, and API key configuration status |
| `POST` | `/api/upload` | Multipart file upload for PDF, PNG, and JPEG documents |
| `POST` | `/api/demo` | Instant loading and auditing of the synthetic enterprise test contract |
| `GET` | `/api/session/{session_id}` | Retrieves session audit data |
| `POST` | `/api/investigate` | Dispatches TinyFish counterparty investigation |
| `POST` | `/api/copilot/ask` | Contextual question answering grounded in contract text |
| `POST` | `/api/copilot/redraft` | Generates balanced alternative clause wording |
| `GET` | `/api/redact/{session_id}` | Streams permanently redacted PDF document |
| `GET` | `/api/export/pdf/{session_id}` | Streams compiled ReportLab legal intelligence dossier |
| `POST` | `/api/session/{session_id}/reset` | Purges session state from active server memory |

---

## 9. Verification and Test Suite

To run the automated test suite covering all backend services:

```bash
source venv/bin/activate
python backend/test_backend.py
```

Test coverage includes:
1. Synthetic agreement generation via ReportLab.
2. PDF text and metadata extraction via PyMuPDF.
3. Clause risk segmentation and overall scoring.
4. Integrity inspection and Error Level Analysis difference map calculation.
5. Privacy detection for PAN, Aadhaar, phone numbers, and bank accounts.
6. Binary-level permanent PDF text redaction.
7. TinyFish investigator query handling.
8. Grounded legal copilot question answering and clause redrafting.
9. Formal PDF report compilation.

---

## 10. Security and Data Handling Practices

- **In-Memory Processing:** Document processing is scoped to active in-memory sessions; uploaded files are not written to persistent databases.
- **Session Purge:** Users can purge their session at any point, removing raw document bytes from memory.
- **Sanitized Outputs:** Masked strings are presented in the user interface and export briefs to prevent accidental PII leakage.
- **Information Minimization:** Only entity names and registration numbers are transmitted to external verification agents; complete contracts are never sent to external web agents.

---

## 11. Statutory Disclaimer

Veritas AI is an automated decision-support utility. It does not establish legal enforceability, signer authenticity, or company solvency. All findings, risk indicators, and redrafted clauses require verification by qualified legal counsel.
