import io
import re
import textwrap
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

SYNTHETIC_CONTRACT_TEXT = """
MASTER CLOUD SERVICES & ENTERPRISE SOFTWARE LICENSE AGREEMENT

This Master Cloud Services Agreement ("Agreement") is executed as of 1 October 2026 ("Effective Date"), by and between:

VERTEX DYNAMICS TECHNOLOGIES PRIVATE LIMITED, a corporation organized under the laws of India, having its principal registered office at Plot 42, Okhla Industrial Area, Phase-III, New Delhi 110020, CIN: U72900DL2021PTC384910, PAN: AABCV1234F, GSTIN: 07AABCV1234F1Z5, represented by authorized signatory Rajiv Malhotra, Aadhaar: 9823 4102 8841 (hereinafter referred to as the "Service Provider");

AND

APEX LOGIC CORPORATION, having its corporate office at Tech Park Horizon, Whitefield, Bangalore 560066 (hereinafter referred to as the "Client" or "Customer").

Contact Email: legal-notices@vertexdynamics.example.com | Direct Billing Tel: +91 98765 43210
Settlement Wire Account: HDFC Bank, A/C No: 502000392817294, IFSC Code: HDFC0001234

RECITALS
WHEREAS, Service Provider operates proprietary cloud-hosted enterprise infrastructure; and
WHEREAS, Client desires to subscribe to said services subject to the terms and covenants herein.

OPERATIONAL TERMS & COVENANTS

1. SCOPE AND LICENSE GRANT
1.1 Service Provider grants Client a limited, revocable, non-exclusive license to access the enterprise platform.
1.2 All underlying source code, database architectures, derivative algorithms, and modifications created shall vest exclusively in Service Provider.

2. FEES, BILLING & FINANCIAL PENALTIES
2.1 Client shall pay an Annual Subscription Fee of INR 180,000 (Indian Rupees One Lakh Eighty Thousand only), billed in equal monthly installments or upfront as set forth in the billing schedule.
2.2 Client shall remit all subscription invoices within fifteen (15) days of receipt. Client must notify Service Provider in writing of any good-faith disputed amount within ten (10) calendar days of invoice date, failing which such invoice shall be deemed undisputed and irrevocably approved.
2.3 Delinquent balances shall accrue late payment interest at the rate of two percent (2%) per month, or the maximum rate permitted by applicable law, whichever is lower, calculated on a simple basis from the due date until full payment.
2.4 In addition to interest, any late payment exceeding thirty (30) days shall incur an administrative liquidated fee of INR 1,50,000 to offset collection costs.

3. TERM AND AUTOMATIC RENEWAL
3.1 The Initial Term of this Agreement shall be twelve (12) months commencing on the Effective Date (1 October 2026).
3.2 This Agreement shall automatically renew for successive twelve (12) month terms unless Client serves written non-renewal notice via registered postal mail at least ninety (90) days prior to the expiration of the then-current term.
3.3 Upon any renewal, annual subscription charges shall increase automatically by fifteen percent (15%) over the preceding term rates without requiring Client's prior written approval.

4. TERMINATION
4.1 Service Provider may terminate this Agreement for convenience at any time, with or without cause, upon delivering forty-five (45) days' prior written email notice to Client.
4.2 Client may terminate this Agreement only in the event of an uncured material breach by Service Provider that remains uncured thirty (30) days following written notice. Client possesses no general right of termination for convenience during the committed Initial Term.
4.3 If Client seeks early cancellation or discontinues use prior to the expiration of the committed Initial Term, Client shall pay an Early Termination Fee equal to one hundred percent (100%) of all remaining fees due across the unexpired portion of the twelve (12) month term.
4.4 In no event shall any advance fees, onboarding charges, or prepaid infrastructure credits be refundable to Client upon termination for any reason whatsoever.

5. INDEMNIFICATION AND UNLIMITED EXPOSURE
5.1 Client shall defend, indemnify, and hold harmless Service Provider, its affiliates, directors, and licensors from and against any and all third-party claims, damages, liabilities, losses, judgments, and reasonable legal fees arising out of Client's use of the service or breach of this Agreement.
5.2 Client's indemnification obligations under this Section 5 are unconditional, uncapped, and shall survive the termination or expiration of this Agreement indefinitely.

6. LIMITATION OF PROVIDER LIABILITY
6.1 Consequential Damages Waiver: In no event shall Service Provider, its officers, or employees be liable to Client for any indirect, incidental, special, exemplary, punitive, or consequential damages, or any loss of profits, revenue, data, or business interruption, regardless of the theory of liability.
6.2 Aggregate Liability Ceiling: Service Provider's total aggregate liability arising out of or related to this Agreement, whether in contract, tort (including negligence), warranty, or otherwise, shall strictly not exceed the total subscription fees actually received by Service Provider from Client in the one (1) month period immediately preceding the event giving rise to the claim, or INR 10,000, whichever is lower.
6.3 The limitations set forth in this Section 6 shall apply even if an essential purpose fails and regardless of whether Service Provider was advised of the possibility of such damages.

7. UNILATERAL AMENDMENT RIGHTS
7.1 Service Provider reserves the unconstrained right to modify, amend, or supplement these terms, service level commitments, and feature availability at any time by posting updated terms to its website at vertexdynamics.example.com/legal.
7.2 Client's continued access or payment after such posting shall constitute irrevocable acceptance of all revised terms.

8. GOVERNING LAW AND EXCLUSIVE DISPUTE VENUE
8.1 This Agreement shall be governed by the laws of India.
8.2 Any dispute, controversy, or claim arising hereunder shall be referred to binding arbitration conducted by a sole arbitrator appointed solely and exclusively by Service Provider's Managing Director. The seat and venue of arbitration shall be New Delhi.

IN WITNESS WHEREOF, the authorized representatives have executed this Agreement as of the Effective Date.

For VERTEX DYNAMICS TECHNOLOGIES PVT LTD:
Authorized Signatory: Rajiv Malhotra (Director)
Tax ID / PAN: AABCV1234F

For APEX LOGIC CORPORATION:
Authorized Signatory: Authorized Officer
"""

# SECOND INDEPENDENT FIXTURE FOR TEST J: Bilateral Mutual Non-Disclosure Agreement
SYNTHETIC_MUTUAL_NDA_TEXT = """
MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of 15 January 2026 ("Effective Date"), by and between:

SOLARIA BIOTECH INCORPORATED, having its principal place of business at 100 Innovation Way, Cambridge, MA 02142 ("Party A");

AND

NOVAGEN DYNAMICS LLC, having its principal place of business at 450 Research Parkway, Austin, TX 78759 ("Party B").

1. PURPOSE
The parties wish to explore a potential business partnership regarding proprietary analytical algorithms (the "Purpose").

2. CONFIDENTIAL INFORMATION
"Confidential Information" means any non-public technical, commercial, or financial information disclosed by either party ("Disclosing Party") to the other party ("Receiving Party").

3. MUTUAL NON-DISCLOSURE OBLIGATIONS
Each party agrees: (a) to protect the other party's Confidential Information with the same degree of care it uses for its own confidential information, but not less than reasonable care; (b) not to disclose such Confidential Information to any third party without prior written consent; and (c) to use Confidential Information solely for the Purpose.

4. TERM AND TERMINATION
This Agreement shall remain in effect for an Initial Term of two (2) years from the Effective Date. Either party may terminate this Agreement for convenience at any time upon thirty (30) days' prior written notice to the other party. The confidentiality obligations herein shall survive for three (3) years following termination.

5. MUTUAL LIMITATION OF LIABILITY
Neither party shall be liable to the other for any indirect, special, incidental, or consequential damages. Each party's total aggregate liability under this Agreement shall not exceed direct damages up to a maximum ceiling of USD 100,000.

6. GOVERNING LAW
This Agreement shall be governed by the laws of the State of Delaware, without regard to conflict of laws principles.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

For SOLARIA BIOTECH INC: Authorized Signatory
For NOVAGEN DYNAMICS LLC: Authorized Signatory
"""

def generate_synthetic_contract_pdf() -> bytes:
    """
    Generates a realistic multi-page PDF of the primary synthetic test contract with
    ReportLab, complete with authentic layout and legal headers.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Page 1
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, "MASTER CLOUD SERVICES & ENTERPRISE AGREEMENT")
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColor(colors.HexColor("#475467"))
    p.drawString(50, height - 65, "Execution Copy - Strictly Confidential Commercial Contract")
    p.setStrokeColor(colors.HexColor("#AD925B"))
    p.setLineWidth(1.5)
    p.line(50, height - 72, width - 50, height - 72)

    p.setFillColor(colors.black)
    p.setFont("Helvetica", 9)

    lines = SYNTHETIC_CONTRACT_TEXT.strip().split("\n")
    y = height - 95
    line_height = 13

    for line in lines:
        if y < 60:
            p.setFont("Helvetica", 8)
            p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 9)

        if line.startswith("MASTER") or line.startswith("OPERATIONAL") or line.startswith("RECITALS"):
            p.setFont("Helvetica-Bold", 11)
            y -= 6
            p.drawString(50, y, line)
            p.setFont("Helvetica", 9)
        elif re.match(r"^\d+\.\s+[A-Z\s,&]+$", line):
            p.setFont("Helvetica-Bold", 10)
            y -= 4
            p.drawString(50, y, line)
            p.setFont("Helvetica", 9)
        else:
            wrapped = textwrap.wrap(line, width=90) if len(line) > 90 else [line]
            indent = 50
            for wline in wrapped:
                if y < 60:
                    p.setFont("Helvetica", 8)
                    p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 9)
                p.drawString(indent, y, wline)
                indent = 60
                y -= line_height
            continue

    p.setFont("Helvetica", 8)
    p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
    p.save()

    buffer.seek(0)
    return buffer.getvalue()

def generate_nda_contract_pdf() -> bytes:
    """
    Generates the secondary independent test fixture PDF (Mutual NDA) for cross-contract validation.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, height - 50, "MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT")
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColor(colors.HexColor("#475467"))
    p.drawString(50, height - 65, "Standard Bilateral Commercial Protective Agreement")
    p.setStrokeColor(colors.HexColor("#067647"))
    p.setLineWidth(1.5)
    p.line(50, height - 72, width - 50, height - 72)

    p.setFillColor(colors.black)
    p.setFont("Helvetica", 9)

    lines = SYNTHETIC_MUTUAL_NDA_TEXT.strip().split("\n")
    y = height - 95
    line_height = 13

    for line in lines:
        if y < 60:
            p.setFont("Helvetica", 8)
            p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 9)

        if line.startswith("MUTUAL") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6."):
            p.setFont("Helvetica-Bold", 10)
            y -= 4
            p.drawString(50, y, line)
            p.setFont("Helvetica", 9)
        else:
            wrapped = textwrap.wrap(line, width=90) if len(line) > 90 else [line]
            indent = 50
            for wline in wrapped:
                if y < 60:
                    p.setFont("Helvetica", 8)
                    p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 9)
                p.drawString(indent, y, wline)
                indent = 60
                y -= line_height
            continue

    p.setFont("Helvetica", 8)
    p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
    p.save()

    buffer.seek(0)
    return buffer.getvalue()
