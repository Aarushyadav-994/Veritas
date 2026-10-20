import io
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

SYNTHETIC_CONTRACT_TEXT = """
MASTER CLOUD SERVICES & ENTERPRISE SOFTWARE LICENSE AGREEMENT

This Master Cloud Services Agreement ("Agreement") is executed as of October 15, 2025 ("Effective Date"), by and between:

VERTEX DYNAMICS TECHNOLOGIES PRIVATE LIMITED, a corporation organized under the laws of India, having its principal registered office at Plot 42, Okhla Industrial Area, Phase-III, New Delhi 110020, CIN: U72900DL2021PTC384910, PAN: AABCV1234F, GSTIN: 07AABCV1234F1Z5, represented by authorized signatory Rajiv Malhotra, Aadhaar: 9823 4102 8841 (hereinafter referred to as the "Service Provider");

AND

APEX LOGIC CORPORATION, having its corporate office at Tech Park Horizon, Whitefield, Bangalore 560066 (hereinafter referred to as the "Client").

Contact Email: legal-notices@vertexdynamics.example.com | Direct Billing Tel: +91 98765 43210
Settlement Wire Account: HDFC Bank, A/C No: 502000392817294, IFSC Code: HDFC0001234

RECITALS
WHEREAS, Service Provider operates proprietary cloud-hosted enterprise infrastructure; and
WHEREAS, Client desires to subscribe to said services subject to the terms and covenants herein.

OPERATIONAL TERMS & COVENANTS

1. SCOPE AND LICENSE GRANT
1.1 Service Provider grants Client a limited, revocable, non-exclusive license to access the platform.
1.2 All underlying source code, database architectures, derivative algorithms, and modifications created shall vest exclusively in Service Provider.

2. FEES, BILLING & FINANCIAL PENALTIES
2.1 Client shall remit all subscription invoices within fifteen (15) days of receipt.
2.2 Delinquent balances shall accrue late payment interest at the rate of twenty-four percent (24%) per annum, compounded monthly from the due date until full satisfaction.
2.3 In addition to interest, any late payment exceeding thirty (30) days shall incur a mandatory liquidated damages fee of INR 1,50,000 to offset administrative collection costs.

3. TERM AND AUTOMATIC RENEWAL
3.1 The Initial Term shall be thirty-six (36) months from the Effective Date.
3.2 This Agreement shall automatically renew for successive twenty-four (24) month terms unless Client serves written non-renewal notice via registered postal mail at least ninety (90) days prior to the expiration of the current term.
3.3 Upon any renewal, annual subscription charges shall increase automatically by fifteen percent (15%) over the preceding term rates without requiring Client's prior approval.

4. TERMINATION
4.1 Service Provider may terminate this Agreement at any time, with or without cause, immediately upon delivering written email notice to Client.
4.2 Client may terminate this Agreement only upon sixty (60) days' written notice, subject to payment of an Early Termination Fee equal to one hundred percent (100%) of all remaining fees due across the unexpired portion of the thirty-six (36) month term.
4.3 In no event shall any advance fees, onboarding charges, or prepaid infrastructure credits be refundable to Client upon termination for any reason whatsoever.

5. INDEMNIFICATION AND UNLIMITED EXPOSURE
5.1 Client shall defend, indemnify, and hold harmless Service Provider, its affiliates, directors, and licensors from and against any and all claims, damages, liabilities, losses, judgments, and legal fees arising out of Client's use of the service or any third-party claims.
5.2 Client's indemnification obligations under this Section 5 are unconditional, uncapped, and shall survive the termination or expiration of this Agreement indefinitely.

6. LIMITATION OF PROVIDER LIABILITY
6.1 In no event shall Service Provider, its officers, or employees be liable for any indirect, special, incidental, punitive, or consequential damages, or any lost profits, lost data, or business interruption.
6.2 Service Provider's total aggregate liability arising out of or related to this Agreement, whether in contract, tort, or warranty, shall strictly not exceed the total fees actually received by Service Provider from Client in the thirty (30) days immediately preceding the event giving rise to claim, or INR 10,000, whichever is less.

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

def generate_synthetic_contract_pdf() -> bytes:
    """
    Generates a realistic multi-page PDF of the synthetic test contract with
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
        elif line and line[0].isdigit() and "." in line[:3] and not line.startswith("1.1") and not line.startswith("2.1") and not line.startswith("3.1") and not line.startswith("4.1") and not line.startswith("5.1") and not line.startswith("6.1") and not line.startswith("7.1") and not line.startswith("8.1"):
            p.setFont("Helvetica-Bold", 10)
            y -= 4
            p.drawString(50, y, line)
            p.setFont("Helvetica", 9)
        else:
            p.drawString(50, y, line[:95])
            if len(line) > 95:
                y -= line_height
                p.drawString(65, y, line[95:190])
        y -= line_height

    p.setFont("Helvetica", 8)
    p.drawString(width / 2 - 20, 30, f"Page {p.getPageNumber()}")
    p.save()

    buffer.seek(0)
    return buffer.getvalue()
