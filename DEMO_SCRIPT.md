# VERITAS AI: LIVE DEMONSTRATION RUNBOOK

**Target Duration:** 2 minutes 30 seconds to 3 minutes  
**Format:** Live Screen Walkthrough for Hackathon Judges  
**Prerequisites:** Backend running on `http://localhost:8000`, Frontend running on `http://localhost:3000`

---

## Part 1: Introduction and Ingestion (0:00 - 0:30)

### What to Click
1. Open your browser to `http://localhost:3000`.
2. On the main ingestion workstation, point to the upload dropzone, then click the **"Load Sample Contract"** button.

### Key Talking Points
- "Most legal AI tools stop at summarizing contracts. Veritas AI is an investigative workstation built to uncover what contracts hide: asymmetric liability, predatory renewal traps, conflicting covenants, and counterparty registry standing."
- "We are loading an authentic enterprise Master Cloud Services Agreement between Vertex Dynamics Technologies and Apex Logic Corporation."
- "Notice the rapid ingestion: in under two seconds, the platform parses internal PDF structures, verifies quotations against the document byte stream, and computes cross-clause dependencies."

---

## Part 2: Multidimensional Risk and Timeline Arithmetic (0:30 - 1:00)

### What to Point Out
1. Highlight the **Overall Risk Index: 81 / 100 (HIGH RISK)** in the top bar.
2. Direct the judges' attention to the five scoring dimensions:
   - Financial Exposure: 85/100 (30% weight)
   - Contractual Imbalance: 90/100 (25% weight)
   - Data & Privacy Exposure: 70/100 (20% weight)
   - Operational Continuity: 75/100 (15% weight)
   - Drafting Ambiguity: 60/100 (10% weight)
3. Point to the **Renewal Timeline arithmetic block**:
   - Initial Term Expiration: 30 September 2027
   - Non-Renewal Notice Deadline: 02 July 2027 (90 calendar days prior)
   - Formal Delivery Rule: Registered postal mail strictly required (email notices are excluded)
4. Point to the **Liability Cap calculation**:
   - Derived monthly allocation: INR 15,000 (INR 180,000 annual fee / 12 months)
   - Alternative fixed ceiling: INR 10,000
   - Effective recovery ceiling: INR 10,000

### Key Talking Points
- "Rather than producing subjective grades, Veritas AI computes risk deterministically across five weighted operational dimensions."
- "Look at the timeline arithmetic: the agreement commenced on 01 October 2026. Because Section 3.2 mandates 90 days prior written notice by registered postal mail, the non-renewal deadline is 02 July 2027. Missing this date automatically triggers another full year with an automatic 15% price hike."
- "On liability: Section 6.2 restricts recovery to one month of trailing fees or INR 10,000. Based on the extracted INR 180,000 annual fee, recovery is capped to a nominal INR 10,000 even in catastrophic service failures."

---

## Part 3: Cross-Clause Reasoning and Missing Protections (1:00 - 1:40)

### What to Click
1. In the Clause Risk Audit tab, click the **"Cross-Clause Reasoning"** sub-tab.
2. Select the first interaction: **"Liability Cap vs Uncapped Indemnification"**.
3. Next, click the **"Protections Matrix"** sub-tab and point out **Section 6.1 (Mutual Consequential Damages Waiver)** classified as `PARTIALLY PRESENT`.

### Key Talking Points
- "Standard legal tools evaluate clauses in isolation. Veritas AI evaluates cross-clause coupling."
- "Look at this interaction: Section 6.2 caps Provider liability to one month of fees, while Section 5.2 imposes unconditional, uncapped indemnity on the Customer. The Customer faces infinite third-party liability exposure while the Provider's risk is capped at nominal sums."
- "In the Protections Matrix, look at Consequential Damages: traditional regex-based checkers flag this as 'Absent'. Veritas AI detects that Section 6.1 already waives consequential damages, but correctly diagnoses it as 'Partially Present' because the waiver protects only the Service Provider, leaving the Customer exposed."

---

## Part 4: Counterparty Investigation via TinyFish (1:40 - 2:10)

### What to Click
1. Click the **"Counterparty Investigation"** tab in the main navigation.
2. Point to the **Execution Mode** indicator in the top right.
   - If online: "Live TinyFish Web Agent" (verified against MCA and registry records).
   - If offline: "Transparent Demo Preset" with clear attribution.
3. Scroll through the retrieved evidence records showing entity standing, CIN `U72900DL2021PTC384910`, and source citations.

### Key Talking Points
- "A contract is only as good as the counterparty behind it. Veritas AI integrates TinyFish autonomous browser agents to investigate the other party."
- "The agent takes the corporate registration number and name from the recitals and queries public corporate registries (MCA, CIN, GSTIN)."
- "It returns verifiable evidence records with timestamps, registration standing, and exact source citations so analysts know who they are contracting with before signing."

---

## Part 5: Alternative Drafting, Redaction, and PDF Export (2:10 - 2:45)

### What to Click
1. Return to the **"Clause Findings"** sub-tab. Find Section 4.1 (Termination for Convenience) and click **"Draft Alternative"**.
2. Show the modal with the proposed bilateral wording and tactical negotiation rationale. Click **"Copy Alternative"**. Close the modal.
3. Click the **"Privacy & Redaction"** tab. Point out the detected PAN and Aadhaar instances. Click **"Download Redacted PDF"**.
4. Click **"Export PDF Dossier"** in the top header. Open the generated 3-page brief.

### Key Talking Points
- "When an unfair clause is detected, Veritas AI generates balanced, bilateral redrafts ready for counter-proposals."
- "Under Privacy, sensitive identifiers like PAN cards and Aadhaar numbers are detected. When we download the redacted PDF, PyMuPDF removes the characters from the PDF byte stream permanently, rather than drawing black boxes over them."
- "Finally, the entire investigation compiles into a 3-page, publication-grade executive dossier ready for executive leadership and counsel."

---

## Part 6: Closing Statement (2:45 - 3:00)

### Key Talking Points
- "Veritas AI combines contract risk auditing, cross-clause reasoning, forensic integrity checks, statutory privacy redaction, and autonomous web investigations into one coherent workspace."
- "Don't just read the contract. Investigate it."
- "Thank you, and we welcome your questions."
