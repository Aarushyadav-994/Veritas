# VERITAS AI

> **"Don't Just Read the Contract. Investigate It."**  
> *Category:* Agentic AI / LegalTech / Document Intelligence  
> *Event:* Kritical Hacks 2026

---

## 1. Executive Overview

**Veritas AI** is a legal document intelligence and investigation workstation designed for founders, legal researchers, students, and businesses. Traditional contract readers summarize text; Veritas AI investigates agreements from multiple forensic angles:
- **Clause-Level Risk Intelligence:** Pinpoints one-sided termination lock-ins, automatic renewals, uncapped liabilities, and missing statutory protections.
- **Autonomous Counterparty Investigation:** Leverages **TinyFish** AI web agents to audit corporate registries, tax filings, and corporate domains.
- **Document Integrity & Error Level Analysis (ELA):** Inspects PDF metadata streams, revision histories, producer traces, and applies ELA pixel compression variance maps.
- **Privacy Exposure & Redaction:** Audits sensitive PII (Aadhaar, PAN, phone, email, bank details) and performs true binary-level PDF stream redaction.
- **Contextual Legal Copilot:** Provides document-grounded legal Q&A citing exact clauses and generates balanced, bilateral alternative contract wording ready to copy.

---

## 2. Visual Identity & Bespoke Design

Veritas AI departs from generic AI SaaS templates (no purple gradients, floating orbs, or glassmorphic decorative cards). The interface is styled as a restrained legal analyst workstation:
- **Palette:** Deep Ink Navy (`#15202B`), Charcoal (`#263238`), Warm Paper (`#F5F3ED`), Muted Brass (`#AD925B`), Slate (`#667085`), High-Risk Red (`#B42318`), Warning Amber (`#B54708`), Verified Green (`#067647`).
- **Typography:** Restrained serif headings paired with clean tabular monospace numerals and identifiers.
- **Information Architecture:** Compact navigation, prominent document workspace, filterable clause risk matrix, interactive ELA viewer, and contextual assistant drawer.

---

## 3. System Architecture

```
                       ┌────────────────────────────────────────┐
                       │  Next.js 16 + React 19 + Tailwind CSS  │
                       │     (Analyst Workstation Interface)    │
                       └──────────────────┬─────────────────────┘
                                          │ HTTP / JSON / Streams
                                          ▼
                       ┌────────────────────────────────────────┐
                       │     FastAPI Python Backend Engine      │
                       └──────────────────┬─────────────────────┘
                                          │
        ┌───────────────────┬─────────────┴───────┬───────────────────┐
        ▼                   ▼                     ▼                   ▼
┌───────────────┐   ┌───────────────┐     ┌───────────────┐   ┌───────────────┐
│ PyMuPDF & PIL │   │  Clause & PII │     │   TinyFish    │   │ Google Gemini │
│  Extraction   │   │  Heuristics   │     │   Web Agent   │   │  API Copilot  │
│  & ELA Maps   │   │  & Redaction  │     │ Investigation │   │  & Grounding  │
└───────────────┘   └───────────────┘     └───────────────┘   └───────────────┘
```

---

## 4. Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Backend Setup
```bash
# In the root repository directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the FastAPI server on port 8000
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Backend will be live at `http://localhost:8000`. API Docs available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
# In the frontend directory
cd frontend
npm install
npm run dev -- --port 3000
```
Frontend workstation will be live at `http://localhost:3000`.

---

## 5. Environment Variables & API Keys

Create a `.env` file in the root directory (refer to `.env.example`):
```bash
# Optional: Google Gemini API Key
GEMINI_API_KEY=""
GEMINI_MODEL="gemini-2.5-flash"

# Optional: TinyFish Web Agent API Key
TINYFISH_API_KEY=""
```

> **Transparent Demonstration Mode:**  
> Veritas AI functions **100% out of the box** without external API keys. If keys are omitted:
> - The **Deterministic Legal Heuristic Engine** extracts clauses, missing protections, and calculates transparent risk indices.
> - The **TinyFish Module** transparently labels evidence as "Simulated Demonstration" and audits sample registry records.
> - The **Copilot & Redrafter** executes grounded semantic retrieval over the document text.
> When `GEMINI_API_KEY` or `TINYFISH_API_KEY` are provided, the platform automatically activates live cloud models and web agents.

---

## 6. Verification & Test Suite

Run the end-to-end backend test suite:
```bash
source venv/bin/activate
python backend/test_backend.py
```
This tests:
1. Synthetic legal agreement generation.
2. PDF text extraction & metadata parsing (PyMuPDF).
3. Clause segmentation & risk grading.
4. Document integrity checks & Error Level Analysis (ELA).
5. Privacy exposure detection (Aadhaar, PAN, phone, email, bank details).
6. Binary-level permanent PDF text redaction.
7. TinyFish counterparty agent dispatcher.
8. Contextual Copilot Q&A and clause counter-proposal drafting.
9. Formal ReportLab PDF intelligence dossier generation.

---

## 7. Statutory Disclaimer

Veritas AI is an automated decision-support utility. It does not establish legal enforceability, signer authenticity, or company solvency. All findings and drafted amendments require verification by qualified legal counsel.
