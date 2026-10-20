# VERITAS AI

**Legal Document Intelligence and Forensic Investigation Platform**

> Tagline: "Don't Just Read the Contract. Investigate It."  
> Event: Kritical Hacks 2026  
> Category: Agentic AI / LegalTech / Document Intelligence  

---

## 1. Executive Summary

Veritas AI is an autonomous legal intelligence and contract investigation workstation designed to evaluate legal agreements beyond surface-level textual summarization. Standard legal AI tools often produce generic platitudes (e.g., "standard terms governing termination"), fail to cross-reference conflicting covenants, and hallucinate missing protections.

Veritas AI replaces heuristic generalizations with an evidence-grounded, multi-dimensional investigative pipeline:

1. **Evidence-Grounded Clause Audit:** Extracts and audits individual contractual covenants across 13 structured parameters, validating all quotations verbatim against raw document byte streams.
2. **Cross-Clause Interaction Reasoning:** Programmatically correlates coupled provisions (such as liability caps paired with uncapped indemnification or automatic renewals paired with short notice windows) to expose compounding financial exposure.
3. **Deterministic Financial & Date Arithmetic:** Dynamically extracts fee schedules, computes trailing liability recovery ceilings under contract formulas, annualizes late interest without compounding assumptions, and computes exact calendar non-renewal notice deadlines.
4. **Four-Tier Missing Protections Matrix:** Categorizes essential standard protections into four distinct operational states (`PRESENT`, `PARTIALLY PRESENT`, `ABSENT`, `UNCERTAIN`), avoiding false negatives on unilateral waivers.
5. **Document Integrity & Forensic ELA:** Inspects PDF dictionary structures, timestamp deltas, authoring software footprints, and renders 15x amplified Error Level Analysis (ELA) compression maps to expose potential post-hoc tampering.
6. **Statutory Privacy Audit & Binary Redaction:** Detects sensitive identifiers (PAN, Aadhaar, telephone numbers, emails, banking credentials) and permanently sanitizes PDF binary byte streams using PyMuPDF.
7. **Autonomous Counterparty Investigation (TinyFish):** Deploys autonomous web agents via the TinyFish SDK to investigate stated counterparties, corporate identification numbers (CIN), GSTIN registrations, and web domain footprints across public registries.
8. **Contextual Legal Copilot & Bilateral Redrafter:** Executes document-grounded legal question answering with strict clause citations and produces balanced, bilateral negotiation redrafts.
9. **Publication-Grade Intelligence Dossier:** Generates multi-page, publication-quality PDF executive briefs formatted with ReportLab for commercial stakeholders.

---

## 2. Design Philosophy and Visual Identity

Veritas AI departs from generic artificial intelligence templates (such as purple-blue gradients, floating orbs, glassmorphism, or repetitive rounded cards). It is styled as a professional legal research workstation with an editorial typography hierarchy:

- **Color Palette:**
  - Deep Ink Navy: `#15202B` (Structural primary)
  - Dark Charcoal: `#263238` (Secondary headers)
  - Warm Legal Paper: `#F5F3ED` (Background canvas)
  - Pure White: `#FFFFFF` (Card surfaces)
  - Muted Brass: `#AD925B` (Accents, highlights, and metadata tags)
  - Muted Slate: `#667085` (Secondary typography and borders)
  - High-Risk Red: `#B42318` (Critical severity alerts)
  - Amber Warning: `#B54708` (Moderate risk warnings)
  - Verified Green: `#067647` (Verbatim verification and low risk)

- **Layout Structure:**
  - Compact header with document metrics, processing telemetry, and action controls.
  - Sticky contractual overview bar presenting the 5-dimension risk score, renewal countdown, and liability cap calculations.
  - Multi-tab investigative navigation separating Clause Findings, Cross-Clause Reasoning, Missing Protections, Counterparty Intelligence, Integrity Forensics, Privacy Audit, and Document Stream.
  - Slide-out Legal Copilot drawer for contextual inquiries without disrupting active review.

---

## 3. System Architecture

```text
+-------------------------------------------------------------------------------+
|                       Next.js 16 + React 19 Client UI                         |
|                    (Bespoke Legal Analyst Workstation)                        |
+---------------------------------------+---------------------------------------+
                                        | HTTP / JSON / Binary Streams
                                        v
+-------------------------------------------------------------------------------+
|                        FastAPI Python Backend Engine                          |
|                             (Port 8000 / Uvicorn)                             |
+-------+--------------------+-------------------+--------------------+---------+
        |                    |                   |                    |
        v                    v                   v                    v
+---------------+    +---------------+   +---------------+    +---------------+
|   Document    |    |  Clause Risk  |   | Cross-Clause  |    |  Financial &  |
|  Extractor    |    |   Analyzer    |   |  Interaction  |    |     Date      |
| (PyMuPDF/PIL) |    |  (13 Fields)  |   |    Engine     |    |  Calculators  |
+---------------+    +---------------+   +---------------+    +---------------+
        |                    |                   |                    |
        v                    v                   v                    v
+---------------+    +---------------+   +---------------+    +---------------+
|  Integrity &  |    |   Evidence    |   |   Privacy &   |    |   TinyFish    |
|   ELA Maps    |    |   Verifier    |   | True Redactor |    | Agentic Web   |
|  (Difference) |    |  (Verbatim)   |   | (PyMuPDF Core)|    | Investigation |
+---------------+    +---------------+   +---------------+    +---------------+
        |                                                             |
        v                                                             v
+---------------+                                             +---------------+
|   ReportLab   |                                             | Contextual    |
|  Multi-Page   |                                             | Legal Copilot |
|  PDF Dossier  |                                             | (Grounded QA) |
+---------------+                                             +---------------+
```

---

## 4. Repository Structure

```text
Veritas/
|-- backend/
|   |-- __init__.py
|   |-- config.py                     # Environment variables, CORS, and upload limits
|   |-- main.py                       # FastAPI application routes and session management
|   |-- test_backend.py               # Comprehensive verification test suite (Tests A-L)
|   |-- services/
|       |-- __init__.py
|       |-- clause_analyzer.py        # 13-field clause extraction, 4-state protections, 5D score
|       |-- copilot_service.py        # Grounded contractual Q&A and bilateral clause redrafter
|       |-- cross_clause_engine.py    # Cross-clause conflict evaluation and compounding risk
|       |-- date_calculator.py        # Term expiration and 90-day renewal deadline arithmetic
|       |-- document_extractor.py     # PDF and image ingestion with metadata extraction
|       |-- evidence_verifier.py      # Normalized verbatim quotation matching and page locator
|       |-- financial_calculator.py   # Dynamic liability cap and simple interest calculations
|       |-- fixtures.py               # Multi-page synthetic SaaS and NDA contract generators
|       |-- integrity_analyzer.py     # PDF structural dictionary forensics and Error Level Analysis
|       |-- privacy_scanner.py        # Statutory PII detection and permanent binary PDF redaction
|       |-- report_generator.py       # Publication-grade ReportLab PDF brief compiler
|       |-- tinyfish_client.py        # TinyFish web agent integration with graceful fallbacks
|-- frontend/
|   |-- src/
|       |-- app/
|           |-- globals.css           # Workspace color variables, serif typography, scrollbars
|           |-- layout.tsx            # Root application layout and HTML metadata
|           |-- page.tsx              # Primary state orchestration and tab rendering
|       |-- components/
|           |-- ClauseFindingsTab.tsx    # Filterable clause audit, cross-clause reasoning, protections
|           |-- ContractOverviewBar.tsx  # Dynamic metrics, 5D risk score bar, renewal countdown
|           |-- CopilotDrawer.tsx        # Slide-out grounded legal assistant drawer
|           |-- DocumentReaderTab.tsx    # Full-text stream and page rendering
|           |-- Header.tsx               # Primary toolbar, session reset, and PDF export actions
|           |-- IntegrityTab.tsx         # Metadata forensic audit and interactive ELA viewer
|           |-- PrivacyTab.tsx           # PII disclosures table and redacted PDF download
|           |-- RedraftModal.tsx         # Interactive alternative clause wording modal
|           |-- TinyFishTab.tsx          # Autonomous web investigation agent terminal
|           |-- UploadWorkspace.tsx      # Ingestion zone with drag-and-drop and demo loader
|   |-- package.json
|   |-- tsconfig.json
|-- .env.example                      # Template configuration with non-sensitive placeholders
|-- .gitignore                        # Comprehensive ignore rules for Python, Node, and secrets
|-- requirements.txt                  # Python dependencies
|-- README.md                         # Project documentation
```

---

## 5. Analytical Framework & Technical Capabilities

### 5.1 Evidence-Grounded Clause Analysis
Every identified provision is extracted and structured into 13 required analytical parameters:
- **Clause Identifier & Title:** (e.g., "Section 4.1 - Service Provider Discretionary Exit")
- **Category:** Termination, Liability Limitations, Indemnification, Renewal, Payment, IP, Amendments, Dispute Resolution.
- **Section & Page Number:** Explicit location derived from document stream.
- **Exact Quotation:** Raw contractual excerpt.
- **Quotation Verification Status:** `VERIFIED_VERBATIM` or `VERIFIED_SUBSTRING` confirmed by the Evidence Verifier.
- **Plain-English Explanation:** Operational explanation of the clause mechanics.
- **Primary Benefiting Party:** Clear identification of contractual asymmetry.
- **Potential Business Consequence:** Tangible operational or financial impact.
- **Risk Severity:** `HIGH RISK`, `MODERATE RISK`, `LOW APPARENT RISK`, or `NEEDS REVIEW`.
- **Severity Justification:** Evidence-grounded rationale for the assigned severity.
- **Recommended Action:** Tactical next step for commercial negotiation.
- **Suggested Alternative Wording:** Bilateral contractual drafting ready for counter-proposals.
- **Confidence Level:** Numerical rating with transparent reasoning.
- **Related Clause IDs:** Explicit cross-references to linked provisions.

### 5.2 Dynamic Financial & Liability Cap Arithmetic
- **Trailing Liability Cap Extraction:** Rather than using static placeholders, the system evaluates trailing formulas (e.g., "fees received in the 1-month period immediately preceding the event").
- **Dynamic Fee Allocation:** Locates the Annual Subscription Fee (INR 180,000) from Section 2.1, derives the monthly allocation ($\text{INR } 180,000 / 12 = \text{INR } 15,000$), evaluates alternative fixed ceilings (INR 10,000), and outputs:
  $$\text{Effective Cap} = \min(\text{INR } 15,000, \text{INR } 10,000) = \text{INR } 10,000$$
- **Payment Interest Calculation:** Converts monthly interest (2% per month) to simple annual interest ($2\% \times 12 = 24.0\%$ per annum), noting that compounding is not specified. Captures short invoice dispute windows (10 calendar days).

### 5.3 Deterministic Renewal Timeline Arithmetic
- **Execution Date & Term:** Extracts effective date (01 October 2026) and 12-month term to establish initial expiration (30 September 2027).
- **Notice Window Arithmetic:**
  $$\text{Non-Renewal Notice Deadline} = \text{30 September 2027} - 90 \text{ calendar days} = \text{02 July 2027}$$
- **Formal Delivery Constraint:** Highlights that notice must be delivered via registered postal mail, precluding email notification.

### 5.4 Cross-Clause Interaction Engine
Identifies compounding risk interactions across separate clauses:
1. *Liability Cap vs Uncapped Indemnity (Section 6.2 vs Section 5.1/5.2):* Provider liability is capped at nominal sums while Customer indemnity is uncapped.
2. *Liability Cap vs Data Incidents (Section 6.1/6.2 vs Data Covenants):* Complete exclusion of indirect damages and lost data without a cybersecurity super-cap.
3. *Committed Term vs Convenience Asymmetry (Section 3.1 vs Section 4.1/4.3):* Provider exits freely on 45 days; Customer faces 100% early termination fee.
4. *Automatic Renewal vs 90-Day Notice (Section 3.2 vs Section 3.3):* Missed July deadline triggers 12-month rollover with automatic 15% rate escalation.
5. *Unilateral Website Amendments (Section 7.1):* Provider changes terms via online posting with deemed acceptance.

### 5.5 Four-Tier Missing Protections Matrix
Audits standard protections using 4 operational states:
- `PRESENT`: Mutual and balanced covenants confirmed in text.
- `PARTIALLY PRESENT`: One-sided or unilateral protection detected. For example, Section 6.1 waives consequential damages for the Provider only; Veritas AI correctly flags this as `PARTIALLY PRESENT` rather than falsely reporting it as `ABSENT`.
- `ABSENT`: Vital protection missing entirely (e.g., Source Code Escrow, Data Breach Notification SLA, Uptime Availability Credit Remedies).
- `UNCERTAIN`: Ambiguous drafting requiring external annexures or schedules.

### 5.6 Transparent 5-Dimension Risk Scoring
Computes an overall 0-100 risk score using a weighted model:
$$\text{Overall Score} = (0.30 \times F) + (0.25 \times I) + (0.20 \times D) + (0.15 \times O) + (0.10 \times A)$$
Where:
- $F$: Financial Exposure (30%)
- $I$: Contractual Imbalance (25%)
- $D$: Data & Privacy Exposure (20%)
- $O$: Operational Continuity (15%)
- $A$: Drafting Ambiguity (10%)

---

## 6. Autonomous Counterparty Investigation (TinyFish)

Veritas AI integrates autonomous web browsing agents via the **TinyFish Agent API** (`tinyfish` Python SDK) to verify entity standing directly against authoritative public databases.

### Investigation Workflow
1. **Entity Extraction:** Extracts corporate entity names and identification credentials (CIN, GSTIN, PAN, and domain addresses) from contract recitals.
2. **Autonomous Query Construction:** Formulates targeted registry queries:
   `"<Entity Name> corporate registration status MCA CIN <CIN Number>"`
3. **Live Web Agent Execution:** Dispatches queries via `TinyFish.search.query()` to autonomous browser agents that inspect the Ministry of Corporate Affairs (MCA), regulatory filings, and domain footprints.
4. **Structured Evidence Attribution:** Returns structured evidence items containing:
   - Source Title
   - URL Citation
   - Extraction Timestamp
   - Registration Standing (e.g., Active vs Inactive)
   - Stated vs Observed Incorporators
5. **Graceful Degradation:** If `TINYFISH_API_KEY` is unconfigured, Veritas AI automatically transitions to a labeled demonstration mode, presenting structured verification data without throwing unhandled exceptions.

---

## 7. Installation and Quickstart

### 7.1 Prerequisites
- **Python:** Version 3.11 or later
- **Node.js:** Version 18 or later (with npm)
- **Git**

### 7.2 Backend Setup

```bash
# Clone the repository
git clone https://github.com/Aarushyadav-994/Veritas.git
cd Veritas

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI backend daemon
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The backend API will be live at `http://localhost:8000`.  
Interactive Swagger documentation is available at `http://localhost:8000/docs`.

### 7.3 Frontend Setup

```bash
# In a new terminal, navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Build production bundle or launch dev server
npm run dev -- --port 3000
```

Open `http://localhost:3000` in your browser to access the Veritas AI analyst workstation.

---

## 8. Configuration & Environment Variables

Copy `.env.example` to `.env` in the project root:

```bash
cp .env.example .env
```

Edit `.env` to configure optional API credentials:

```bash
# Google Gemini API Key (Optional)
# If omitted, Veritas AI runs on its deterministic, local legal intelligence engine
GEMINI_API_KEY=""
GEMINI_MODEL="gemini-2.5-flash"

# TinyFish Agent API Key (Optional)
# If omitted, Veritas AI operates in transparent, labeled demonstration mode
TINYFISH_API_KEY=""

# Maximum upload file size in Megabytes (Default: 25)
MAX_UPLOAD_SIZE_MB=25
```

---

## 9. Verification & Test Suite

Veritas AI includes an automated test suite verifying all 12 analytical requirements (Tests A through L).

### Running the Test Suite

```bash
source venv/bin/activate
python backend/test_backend.py
```

### Test Coverage Summary

| Test | Objective | Status |
|---|---|---|
| **Test A** | Document Extraction: Identifies contract type, parties, effective date, initial term, and annual subscription fee. | Pass |
| **Test B** | Liability Cap Calculation: Formulates trailing 1-month fee, calculates monthly INR 15,000 estimate, compares with INR 10,000 ceiling, and lists assumptions. | Pass |
| **Test C** | Termination Asymmetry: Exposes Provider 45-day convenience exit versus Customer lock-in and 100% early termination fee. | Pass |
| **Test D** | Automatic Renewal Timeline: Calculates initial term end (30 Sep 2027), 90-day window, non-renewal deadline (02 July 2027), and postal mail delivery method. | Pass |
| **Test E** | Existing Damages Waiver Detection: Verifies Section 6.1 is classified as `PARTIALLY PRESENT` (not `ABSENT`) and documents the unilateral asymmetry. | Pass |
| **Test F** | Cross-Clause Interaction Reasoning: Correlates Section 6.2 liability cap with Section 5.1/5.2 uncapped indemnification (`HIGH RISK`). | Pass |
| **Test G** | Quotation Verification: Validates that all analyzed clauses match source text verbatim via `EvidenceVerifier`. | Pass |
| **Test H** | Payment Terms & Interest: Verifies 2% monthly rate, calculates 24% simple annual rate, and captures the 10-day invoice dispute window. | Pass |
| **Test I** | Uncertainty & Absent Protections: Verifies truly absent covenants (Source Code Escrow, SLA Credits) are reported as `ABSENT`. | Pass |
| **Test J** | Contract Generalization: Executes analysis on an independent Mutual NDA fixture, validating that scores, parties, and clauses differ dynamically. | Pass |
| **Test K** | PDF Report Generation: Validates ReportLab generation of multi-page dossiers without localhost URLs. | Pass |
| **Test L** | External Service Failure Handling: Simulates unconfigured and invalid TinyFish credentials, validating graceful fallback without backend crashes. | Pass |

---

## 10. API Specification

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check, active session count, and service configuration status |
| `POST` | `/api/upload` | Multipart file upload for PDF, PNG, and JPEG documents |
| `POST` | `/api/demo` | Instantly loads and audits the prepared synthetic enterprise agreement fixture |
| `GET` | `/api/session/{session_id}` | Retrieves parsed audit data, timeline calculations, and findings for a session |
| `POST` | `/api/investigate` | Triggers a live or demonstration TinyFish counterparty investigation |
| `POST` | `/api/copilot/ask` | Contextual question answering grounded strictly in document text |
| `POST` | `/api/copilot/redraft` | Generates balanced alternative clause language and tactical negotiation advice |
| `GET` | `/api/redact/{session_id}` | Streams a permanently redacted PDF with sanitized binary streams |
| `GET` | `/api/export/pdf/{session_id}` | Streams a compiled multi-page ReportLab legal intelligence dossier |
| `POST` | `/api/session/{session_id}/reset` | Clears active session state and document bytes from server memory |

---

## 11. Security and Responsible Data Practices

- **In-Memory Volatile Processing:** Uploaded documents are stored only in volatile memory during the active session. No document text or metadata is persisted to unencrypted disk caches or external databases.
- **Permanent Redaction:** Redactions applied via `PrivacyScanner` modify underlying PDF stream objects using PyMuPDF's `apply_redactions()` method, removing characters from the PDF byte stream rather than overlaying visual boxes.
- **Information Minimization:** Only stated entity names and registration numbers are transmitted to the TinyFish agent API; contract body text is never transmitted to external web investigation agents.
- **Session Purge:** Executing a session reset immediately releases raw PDF bytes and extracted text structures from memory.

---

## 12. Statutory Disclaimer

Veritas AI is an automated investigative utility designed for decision-support and issue identification. It does not provide legal advice, establish definitive enforceability, certify signer authenticity, or guarantee corporate solvency. All findings, risk indexes, and redrafted clauses must be verified by qualified legal counsel prior to formal execution or litigation.
