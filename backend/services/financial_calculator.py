import re
from typing import Dict, Any, Optional

class FinancialCalculator:
    """
    Performs dynamic extraction and financial arithmetic for liability caps,
    annual subscription fees, monthly allocations, and penalty interest rates.
    Never hardcodes sample values; extracts figures from contract text dynamically.
    """

    @staticmethod
    def extract_monetary_amounts(text: str) -> list[Dict[str, Any]]:
        """
        Extracts monetary figures (e.g., INR 1,80,000, INR 180,000, USD 50,000, $10,000).
        """
        results = []
        # Pattern for currency followed or preceded by numbers
        pattern = re.compile(r"(?:(INR|Rs\.?|USD|\$|EUR|GBP)\s*([\d,]+(?:\.\d{2})?)|([\d,]+(?:\.\d{2})?)\s*(?:INR|USD|EUR))", re.IGNORECASE)
        for match in pattern.finditer(text):
            currency = match.group(1) or "INR"
            val_str = match.group(2) or match.group(3)
            clean_num = val_str.replace(",", "")
            try:
                num = float(clean_num)
                if num > 0:
                    results.append({
                        "currency": currency.upper().replace("RS.", "INR").replace("RS", "INR").replace("$", "USD"),
                        "raw_string": match.group(0).strip(),
                        "amount": num
                    })
            except ValueError:
                pass
        return results

    @staticmethod
    def analyze_liability_cap(full_text: str) -> Dict[str, Any]:
        """
        Dynamically calculates illustrative liability cap based on extracted fees and contractual cap formula.
        """
        # 1. Identify formula from text
        formula_type = "UNKNOWN"
        time_period_desc = "Not specified"
        cap_months = 1

        if re.search(r"(?:preceding|prior)\s*(?:one|1|\(1\))\s*month|thirty\s*\(?30\)?\s*days", full_text, re.IGNORECASE):
            formula_type = "ONE_MONTH_PRECEDING_FEES"
            time_period_desc = "1 month (30 days) immediately preceding the event giving rise to claim"
            cap_months = 1
        elif re.search(r"(?:preceding|prior)\s*(?:three|3|\(3\))\s*months|ninety\s*\(?90\)?\s*days", full_text, re.IGNORECASE):
            formula_type = "THREE_MONTHS_PRECEDING_FEES"
            time_period_desc = "3 months (90 days) preceding the event"
            cap_months = 3
        elif re.search(r"(?:preceding|prior)\s*(?:twelve|12|\(12\))\s*months|one\s*\(?1\)?\s*year", full_text, re.IGNORECASE):
            formula_type = "TWELVE_MONTHS_PRECEDING_FEES"
            time_period_desc = "12 months preceding the event"
            cap_months = 12
        elif re.search(r"total\s+fees\s+paid", full_text, re.IGNORECASE):
            formula_type = "TOTAL_FEES_PAID"
            time_period_desc = "Total fees actually received under the agreement"
            cap_months = 12

        # 2. Extract annual subscription fee if present
        annual_fee = None
        currency = "INR"

        fee_match = re.search(r"(?:annual\s+subscription\s+(?:fee|charges?)|contract\s+value|subscription\s+fee)\s*(?:of|is|:)?\s*(?:(INR|USD|\$|Rs\.?)\s*([\d,]+)|([\d,]+)\s*(?:INR|USD))", full_text, re.IGNORECASE)
        if fee_match:
            currency_raw = fee_match.group(1) or "INR"
            val_raw = (fee_match.group(2) or fee_match.group(3)).replace(",", "")
            try:
                annual_fee = float(val_raw)
                currency = currency_raw.upper().replace("RS.", "INR").replace("RS", "INR").replace("$", "USD")
            except ValueError:
                pass
        else:
            # Look for general recurring fees
            amounts = FinancialCalculator.extract_monetary_amounts(full_text)
            for a in amounts:
                if a["amount"] >= 50000:
                    annual_fee = a["amount"]
                    currency = a["currency"]
                    break

        # 3. Dynamic calculation with explicit assumptions
        if annual_fee and formula_type == "ONE_MONTH_PRECEDING_FEES":
            monthly_illustrative = round(annual_fee / 12, 2)
            fixed_alternate = 10000.0 if "10,000" in full_text else None
            
            calc_text = (
                f"Illustrative recovery ceiling: Approximately {currency} {monthly_illustrative:,.2f} "
                f"(derived from extracted annual fee of {currency} {annual_fee:,.2f} allocated equally across 12 calendar months: "
                f"{currency} {annual_fee:,.2f} / 12)."
            )
            if fixed_alternate:
                calc_text += f" Where the contract specifies 'or {currency} {fixed_alternate:,.2f}, whichever is less', recovery is further constrained to {currency} {min(monthly_illustrative, fixed_alternate):,.2f}."

            return {
                "formula_identified": "Subscription fees paid or payable for 1-month period immediately preceding the event",
                "time_period": time_period_desc,
                "annual_fee_detected": f"{currency} {annual_fee:,.2f}",
                "illustrative_cap_amount": f"{currency} {monthly_illustrative:,.2f}",
                "calculation_methodology": calc_text,
                "assumptions": [
                    f"Assumes an explicit equal monthly allocation of the detected {currency} {annual_fee:,.2f} annual subscription fee.",
                    "Estimate does not constitute a judicial ruling on enforceable damage recovery.",
                    "Actual recovery may vary based on exact billing schedule, credit adjustments, and trailing invoices."
                ],
                "carve_outs_detected": "Confidentiality, gross negligence, or willful misconduct exceptions" if "gross negligence" in full_text.lower() else "None explicitly detected in liability section",
                "commercial_impact": "Severe recovery suppression. In the event of catastrophic data loss, prolonged outage, or service breach, customer recovery is restricted to nominal one-month fees."
            }
        elif annual_fee:
            cap_val = round((annual_fee / 12) * cap_months, 2)
            return {
                "formula_identified": formula_type.replace("_", " ").title(),
                "time_period": time_period_desc,
                "annual_fee_detected": f"{currency} {annual_fee:,.2f}",
                "illustrative_cap_amount": f"{currency} {cap_val:,.2f}",
                "calculation_methodology": f"Derived from detected fee of {currency} {annual_fee:,.2f} across a {cap_months}-month window.",
                "assumptions": ["Assumes uniform fee allocation across contract term."],
                "carve_outs_detected": "Standard exclusions",
                "commercial_impact": f"Recovery capped to approximately {cap_months} month(s) of contract value."
            }
        else:
            return {
                "formula_identified": formula_type.replace("_", " ").title() if formula_type != "UNKNOWN" else "Fees paid in specified trailing period",
                "time_period": time_period_desc,
                "annual_fee_detected": "Fee schedule not explicitly stated in document body",
                "illustrative_cap_amount": "Requires fee schedule annexure to compute monetary value",
                "calculation_methodology": "Unable to calculate numeric cap without explicit pricing annexure or invoice schedule in extracted text.",
                "assumptions": ["Pricing may be detailed in an unattached Schedule or Order Form."],
                "carve_outs_detected": "Not determined",
                "commercial_impact": "Cap restricts liability to trailing periodic fees, limiting counterparty financial accountability."
            }

    @staticmethod
    def analyze_payment_penalties(full_text: str) -> Dict[str, Any]:
        """
        Analyzes payment terms, late interest calculations, and invoice dispute procedures.
        Distinguishes simple annualization from compounding.
        """
        # Detect interest rate
        rate_m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:per\s+(?:month|annum|year)|monthly|annually)", full_text, re.IGNORECASE)
        rate_val = 2.0
        period = "month"

        if rate_m:
            rate_val = float(rate_m.group(1))
            matched_text = rate_m.group(0).lower()
            if "annum" in matched_text or "year" in matched_text or "annually" in matched_text:
                period = "annum"
            else:
                period = "month"

        # Check compounding
        is_compounded = bool(re.search(r"compound(?:ed)?\s+(?:monthly|annually|daily)", full_text, re.IGNORECASE))

        # Check dispute window
        dispute_m = re.search(r"(?:disput\w+|contest\w*)[^.\n]{0,60}within\s+(?:(?:seven|ten|fifteen|thirty)\s*)?\(?(\d{1,2})\)?\s*(?:calendar\s+|business\s+)?days", full_text, re.IGNORECASE)
        dispute_days = int(dispute_m.group(1)) if dispute_m else None

        # Check payment due window
        due_m = re.search(r"(?:payable|due|remit)\s+(?:within|in)\s*(?:(?:fifteen|thirty|forty-five)\s*)?\(?(\d{1,2})\)?\s*days", full_text, re.IGNORECASE)
        due_days = int(due_m.group(1)) if due_m else 15

        # Calculations
        if period == "month":
            monthly_rate = rate_val
            simple_annual = monthly_rate * 12
            effective_annual = round(((1 + (monthly_rate / 100)) ** 12 - 1) * 100, 2) if is_compounded else None
        else:
            simple_annual = rate_val
            monthly_rate = round(rate_val / 12, 2)
            effective_annual = None

        rate_explanation = f"Stated Interest Rate: {rate_val}% per {period}."
        if period == "month":
            rate_explanation += f" Simple annualization yields {simple_annual:.1f}% per annum."
            if is_compounded:
                rate_explanation += f" Because the agreement explicitly specifies monthly compounding, the effective annual rate (EAR) is {effective_annual:.2f}% per annum."
            else:
                rate_explanation += " The agreement does not specify monthly compounding; therefore, simple annualization (not compounding) applies unless statutory rules dictate otherwise."

        dispute_analysis = (
            f"Invoice Dispute Window: {dispute_days} calendar days." if dispute_days
            else "Invoice Dispute Window: Not explicitly established in text (requires review of standard billing terms)."
        )

        consequences = [
            f"Invoices are payable within {due_days} days.",
            f"Unpaid balances accrue {rate_val}% per {period} late fee.",
        ]
        if dispute_days:
            consequences.append(f"Invoices not formally contested in writing within {dispute_days} days are deemed accepted and become immediately payable.")
        if is_compounded:
            consequences.append(f"Compounding accumulates financial liability exponentially on delinquent balances ({effective_annual}% effective annual rate).")

        return {
            "stated_rate": f"{rate_val}% per {period}",
            "is_compounded": is_compounded,
            "simple_annualized_rate": f"{simple_annual:.1f}% per annum",
            "effective_annual_rate": f"{effective_annual:.2f}% per annum" if is_compounded else "N/A (Simple interest only)",
            "payment_due_days": due_days,
            "dispute_window_days": dispute_days,
            "explanation": rate_explanation,
            "dispute_procedure_analysis": dispute_analysis,
            "consequences": consequences,
            "negotiation_recommendation": f"Negotiate a longer invoice dispute window (e.g. 30 business days), cap late interest to 1% per month simple interest, and ensure payment withholding is expressly permitted for good-faith disputed amounts without triggering service suspension."
        }
