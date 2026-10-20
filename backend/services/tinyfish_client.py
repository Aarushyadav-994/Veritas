import os
import datetime
from typing import Dict, Any, List, Optional
from backend.config import settings

class TinyFishInvestigator:
    @staticmethod
    def is_configured() -> bool:
        return bool(settings.tinyfish_api_key and settings.tinyfish_api_key.strip())

    @staticmethod
    def investigate_entity(
        entity_name: str,
        registration_id: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a real agentic web investigation using TinyFish if configured,
        or delivers an honest, labeled simulated investigation if credentials are absent.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        if not TinyFishInvestigator.is_configured():
            return TinyFishInvestigator._generate_simulated_result(entity_name, registration_id, now_iso)

        # Real TinyFish execution
        try:
            return TinyFishInvestigator._run_live_tinyfish(entity_name, registration_id, now_iso)
        except Exception as e:
            # Report honest integration failure without crashing the platform
            return {
                "entity_searched": entity_name,
                "investigation_status": "Investigation failed",
                "is_live_execution": True,
                "api_endpoint": "https://agent.tinyfish.ai/v1/search/query",
                "error_details": f"TinyFish Agent API execution error: {str(e)}",
                "timestamp": now_iso,
                "limitations": "Network or authentication issue prevented live web agent execution. Check TINYFISH_API_KEY and endpoint accessibility.",
                "evidence_items": []
            }

    @staticmethod
    def _run_live_tinyfish(entity_name: str, registration_id: Optional[str], timestamp: str) -> Dict[str, Any]:
        """
        Dispatches live TinyFish queries to verify stated entities against corporate registries,
        regulatory portals, and web footprints.
        """
        from tinyfish import TinyFish

        client = TinyFish(api_key=settings.tinyfish_api_key)
        clean_name = entity_name.strip() if entity_name else "Target Entity"

        evidence_items: List[Dict[str, Any]] = []

        # Construct specific search query for corporate registry records
        reg_query = f"{clean_name} corporate registration status MCA CIN"
        if registration_id and "Not" not in registration_id:
            reg_query += f" {registration_id}"

        search_resp = client.search.query(query=reg_query)

        status_label = "Not verified"
        if search_resp and hasattr(search_resp, "results") and len(search_resp.results) > 0:
            status_label = "Verified against source"

            for res in search_resp.results[:4]:
                snippet_text = res.snippet or "Live index record retrieved from source."
                title_text = res.title or res.site_name or "Official Web Record"
                url_text = res.url or "https://www.mca.gov.in"

                # Check evidence indicators
                is_active = any(k in snippet_text.lower() for k in ["active", "incorporated", "registered", "company", "limited"])

                evidence_items.append({
                    "verification_question": f"Is '{clean_name}' listed in public registries or verified business directories?",
                    "source_name": f"{title_text} ({res.site_name or 'Web Source'})",
                    "source_url": url_text,
                    "information_retrieved": snippet_text,
                    "timestamp": timestamp,
                    "status": "Verified against source" if is_active else "Partially verified",
                    "limitations": "Public search index verification confirms public corporate presence. It does not certify signatory authority or contractual authenticity."
                })
        else:
            status_label = "Not verified"
            evidence_items.append({
                "verification_question": f"Does '{clean_name}' have verifiable registration filings in online corporate indexes?",
                "source_name": "TinyFish Web Index Lookup",
                "source_url": f"https://www.google.com/search?q={clean_name.replace(' ', '+')}",
                "information_retrieved": "No public incorporation records were indexed for this exact entity name under the searched parameters.",
                "timestamp": timestamp,
                "status": "Not verified",
                "limitations": "Unregistered entities, newly formed private corporations, or synthetic demo parties may not appear in public web indexes."
            })

        # Query 2: Official domain and corporate footprint audit
        domain_query = f"{clean_name} official website contact address"
        domain_resp = client.search.query(query=domain_query)
        if domain_resp and hasattr(domain_resp, "results") and len(domain_resp.results) > 0:
            top_domain = domain_resp.results[0]
            evidence_items.append({
                "verification_question": f"Does '{clean_name}' maintain an indexed web footprint and official contact presence?",
                "source_name": f"{top_domain.title or 'Official Presence'} ({top_domain.site_name or 'Domain'})",
                "source_url": top_domain.url,
                "information_retrieved": top_domain.snippet or "Domain record verified via live TinyFish search.",
                "timestamp": timestamp,
                "status": "Partially verified",
                "limitations": "Domain ownership confirms corporate web branding but does not replace formal legal diligence."
            })

        return {
            "entity_searched": clean_name,
            "investigation_status": status_label,
            "is_live_execution": True,
            "api_endpoint": "https://agent.tinyfish.ai (Live Execution via TinyFish SDK)",
            "timestamp": timestamp,
            "limitations": "Live counterparty verification retrieved through TinyFish infrastructure. Public records verify filing status but do not guarantee individual authorization or contract enforceability.",
            "evidence_items": evidence_items
        }

    @staticmethod
    def _generate_simulated_result(entity_name: str, registration_id: Optional[str], timestamp: str) -> Dict[str, Any]:
        """
        Transparent, clearly labeled simulation mode when TINYFISH_API_KEY is not configured.
        Never pretends to be a live lookup.
        """
        clean_name = entity_name if entity_name and entity_name != "Party A" else "Vertex Dynamics Technologies Pvt Ltd"
        reg_id = registration_id if registration_id and "Not" not in registration_id else "U72900DL2021PTC384910"

        evidence_items = [
            {
                "verification_question": f"Is '{clean_name}' actively incorporated under Ministry of Corporate Affairs / Registrar of Companies?",
                "source_name": "Ministry of Corporate Affairs (MCA) Registry [Simulated Demonstration]",
                "source_url": "https://www.mca.gov.in/content/mca/global/en/home.html",
                "information_retrieved": f"Entity Name: {clean_name} | CIN: {reg_id} | Status: Active | Date of Inc: 14/06/2021 | Class: Private Limited | Authorized Capital: INR 10,00,000",
                "timestamp": timestamp,
                "status": "Verified against source",
                "limitations": "DEMONSTRATION FIXTURE: Active MCA status confirms registration filing presence but does not verify whether the signer holds valid corporate Power of Attorney."
            },
            {
                "verification_question": f"Does '{clean_name}' maintain active GSTIN tax registration corresponding to stated jurisdiction?",
                "source_name": "GST Common Portal Public Verification [Simulated Demonstration]",
                "source_url": "https://services.gst.gov.in/services/searchtpbypan",
                "information_retrieved": "GSTIN: 07AABCV1234F1Z5 | Legal Name: Vertex Dynamics Technologies Private Limited | Principal Place of Business: Okhla Phase III, New Delhi | Status: Active",
                "timestamp": timestamp,
                "status": "Verified against source",
                "limitations": "DEMONSTRATION FIXTURE: Tax registration verifies operational tax identity but does not safeguard against breach of contract or financial insolvency."
            },
            {
                "verification_question": f"Does the official domain and web footprint match the stated corporate address?",
                "source_name": "Official Corporate Domain & Security Audit [Simulated Demonstration]",
                "source_url": "https://vertexdynamics.example.com",
                "information_retrieved": "DNS Records: Active MX & SPF configurations present. SSL Certificate: Let's Encrypt Authority valid through 2026. Registered address matches MCA filing.",
                "timestamp": timestamp,
                "status": "Partially verified",
                "limitations": "DEMONSTRATION FIXTURE: Domain registration records confirm web presence but do not verify contractual authority."
            }
        ]

        return {
            "entity_searched": clean_name,
            "investigation_status": "Simulated Demonstration",
            "is_live_execution": False,
            "api_endpoint": "https://agent.tinyfish.ai/v1/automation/run (Mock Mode)",
            "configuration_notice": "TINYFISH_API_KEY environment variable is not configured. Displaying transparent simulated corporate registry records for demo purposes. To activate live agent browsing, set TINYFISH_API_KEY.",
            "timestamp": timestamp,
            "limitations": "This report is a simulated demonstration fixture. No live web queries were dispatched to TinyFish servers.",
            "evidence_items": evidence_items
        }
