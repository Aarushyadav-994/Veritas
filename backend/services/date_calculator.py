import re
import datetime
from typing import Dict, Any, Optional, Tuple

class DateCalculator:
    """
    Performs deterministic contract term and non-renewal deadline arithmetic.
    Extracts dates, durations, and notice intervals from contract text and calculates
    exact deadlines with transparent assumptions.
    """

    MONTH_MAP = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }

    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime.date]:
        """
        Attempts to parse date strings in formats:
        - '1 October 2026'
        - 'October 1, 2026'
        - '15 October 2025'
        - '2026-10-01'
        - '01/10/2026'
        """
        if not date_str:
            return None

        clean = date_str.strip().lower()

        # Format 1: '1 october 2026' or '1st october 2026'
        m1 = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)[,\s]+(\d{4})", clean)
        if m1:
            day = int(m1.group(1))
            month_name = m1.group(2)
            year = int(m1.group(3))
            if month_name in DateCalculator.MONTH_MAP:
                month = DateCalculator.MONTH_MAP[month_name]
                try:
                    return datetime.date(year, month, day)
                except ValueError:
                    pass

        # Format 2: 'october 1, 2026' or 'october 1 2026'
        m2 = re.search(r"([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?[,\s]+(\d{4})", clean)
        if m2:
            month_name = m2.group(1)
            day = int(m2.group(2))
            year = int(m2.group(3))
            if month_name in DateCalculator.MONTH_MAP:
                month = DateCalculator.MONTH_MAP[month_name]
                try:
                    return datetime.date(year, month, day)
                except ValueError:
                    pass

        # Format 3: YYYY-MM-DD
        m3 = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", clean)
        if m3:
            try:
                return datetime.date(int(m3.group(1)), int(m3.group(2)), int(m3.group(3)))
            except ValueError:
                pass

        return None

    @staticmethod
    def extract_term_months(text: str) -> Optional[int]:
        """
        Extracts duration in months from text like 'twelve (12) months', '12 months', '1 year', '36 months'.
        """
        # Look for months explicitly
        m = re.search(r"(?:initial\s+term|term\s+of|duration\s+of|period\s+of)?\s*(?:(?:one|two|three|four|five|six|twelve|twenty-four|thirty-six)\s*)?\(?(\d{1,3})\)?\s*months?", text, re.IGNORECASE)
        if m:
            return int(m.group(1))

        # Look for years
        y = re.search(r"(?:initial\s+term|term\s+of|period\s+of)?\s*\(?(\d{1,2})\)?\s*years?", text, re.IGNORECASE)
        if y:
            return int(y.group(1)) * 12

        return None

    @staticmethod
    def extract_notice_days(text: str) -> Optional[int]:
        """
        Extracts notice period in days (e.g. 'ninety (90) days', '90 days', '30 days').
        """
        m = re.search(r"(?:at\s+least|not\s+less\s+than|prior\s+notice\s+of)?\s*(?:(?:thirty|forty-five|sixty|ninety|one\s+hundred\s+twenty)\s*)?\(?(\d{1,3})\)?\s*days?", text, re.IGNORECASE)
        if m:
            return int(m.group(1))
        return None

    @staticmethod
    def add_months(sourcedate: datetime.date, months: int) -> datetime.date:
        """
        Deterministically adds months to a date handling calendar month lengths.
        """
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, [31,
            29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return datetime.date(year, month, day)

    @staticmethod
    def analyze_renewal_timeline(
        full_text: str,
        effective_date_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Performs full renewal timeline calculation and date arithmetic based on extracted agreement text.
        """
        # 1. Detect effective date if not explicitly passed
        parsed_eff_date = None
        if effective_date_str:
            parsed_eff_date = DateCalculator.parse_date(effective_date_str)

        if not parsed_eff_date:
            date_m = re.search(r"(?:effective\s+as\s+of|dated|executed\s+as\s+of|entered\s+into\s+on)\s+([A-Za-z0-9\s,]{4,30}\d{4})", full_text[:2500], re.IGNORECASE)
            if date_m:
                parsed_eff_date = DateCalculator.parse_date(date_m.group(1))

        # 2. Extract initial term duration
        term_months = DateCalculator.extract_term_months(full_text) or 12

        # 3. Extract non-renewal notice period
        # Look specifically in renewal sections
        renewal_snippet_m = re.search(r"(\b(?:renew|renewal|non-renewal)\b[\s\S]{10,400}?(?:\.|\n\n))", full_text, re.IGNORECASE)
        notice_days = 90
        if renewal_snippet_m:
            detected_notice = DateCalculator.extract_notice_days(renewal_snippet_m.group(1))
            if detected_notice:
                notice_days = detected_notice

        # 4. Perform deterministic arithmetic if effective date is available
        if parsed_eff_date:
            # End of initial term: Effective date + term_months (e.g. 1 Oct 2026 + 12 months = 30 Sep 2027 or 1 Oct 2027)
            term_end_date = DateCalculator.add_months(parsed_eff_date, term_months)
            # Subtract 1 day for standard inclusive period (e.g. 1 Oct 2026 to 30 Sep 2027)
            inclusive_end_date = term_end_date - datetime.timedelta(days=1)

            # Deadline: Notice period before term end date
            notice_deadline_date = inclusive_end_date - datetime.timedelta(days=notice_days)

            return {
                "calculation_status": "DETERMINED",
                "effective_date": parsed_eff_date.strftime("%d %B %Y"),
                "initial_term_months": term_months,
                "initial_term_end_date": inclusive_end_date.strftime("%d %B %Y"),
                "notice_period_days": notice_days,
                "notice_deadline_date": notice_deadline_date.strftime("%d %B %Y"),
                "arithmetic_formula": f"Notice Deadline = ({inclusive_end_date.strftime('%d %B %Y')} [Initial Term End]) minus {notice_days} calendar days",
                "assumptions": [
                    "Calculation assumes calendar day counting rather than business days unless explicitly defined otherwise.",
                    "Notice is assumed to be required on or before 11:59 PM on the calculated deadline date.",
                    "Consecutive renewal terms will shift subsequent non-renewal deadlines forward by the agreed renewal interval."
                ],
                "consequences_of_missed_deadline": f"Failure to serve written notice by {notice_deadline_date.strftime('%d %B %Y')} triggers automatic renewal for the subsequent term without opportunity for discretionary cancellation.",
                "uncertainties": []
            }
        else:
            return {
                "calculation_status": "APPROXIMATE_OR_UNCERTAIN",
                "effective_date": "Execution Date (Not explicitly fixed in text)",
                "initial_term_months": term_months,
                "initial_term_end_date": "Effective Date + 12 Months",
                "notice_period_days": notice_days,
                "notice_deadline_date": f"{notice_days} days prior to initial term anniversary",
                "arithmetic_formula": f"Notice Deadline = (Anniversary Date) minus {notice_days} calendar days",
                "assumptions": [
                    "Effective date was not parsed with certainty from text; timeline is expressed as relative offset."
                ],
                "consequences_of_missed_deadline": f"Automatic rollover occurs if notice is not provided at least {notice_days} days before term expiration.",
                "uncertainties": [
                    "Missing absolute calendar execution date in contract recitals."
                ]
            }
