import os
import datetime
from typing import Dict, Any, List, Optional
import httpx
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
                "api_endpoint": "https://agent.tinyfish.ai/v1/automation/run",
                "error_details": f"TinyFish Agent API execution error: {str(e)}",
                "timestamp": now_iso,
                "limitations": "Network or authentication issue prevented live web agent execution. Check TINYFISH_API_KEY and endpoint accessibility.",
                "evidence_items": []
            }

    @staticmethod
    def _run_live_tinyfish(entity_name: str, registration_id: Optional[str], timestamp: str) -> Dict[str, Any]:
        """
        Calls TinyFish Web Agent API with targeted verification goals.
        """
        from tinyfish import TinyFish, RunStatus

        client = TinyFish(api_key=settings.tinyfish_api_key)

        evidence_items: List[Dict[str, Any]] = []

        # Target 1: Public registry verification (e.g. OpenCorporates / Zauba / MCA lookup)
        search_target_url = "https://opencorporates.com"
        goal = f"Search for company '{entity_name}'. Find incorporation status, company number, and registered address. Return summary."

        run_response = client.agent.run(
            url=search_target_url,
            goal=goal
        )

        status_label = "Not verified"
        retrieved_data = "No records located."

        if run_response.status == RunStatus.COMPLETED and run_response.result:
            retrieved_data = str(run_response.result)
            if "active" in retrieved_data.lower() or "incorporated" in retrieved_data.lower():
                status_label = "Verified against source"
            else:
                status_label = "Partially verified"
        else:
            status_label = "Investigation failed"
            retrieved_data = f"TinyFish run status: {run_response.status}"

        evidence_items.append({
            "verification_question": f"Is '{entity_name}' legally incorporated in official corporate registries?",
            "source_name": "OpenCorporates Global Registry",
            "source_url": f"https://opencorporates.com/companies?q={entity_name.replace(' ', '+')}",
            "information_retrieved": retrieved_data,
            "timestamp": timestamp,
            "status": status_label,
            "limitations": "Corporate registry verification confirms entity registration history but does not authenticate the individual counterparty representative or the specific contract document."
        })

        return {
            "entity_searched": entity_name,
            "investigation_status": status_label,
            "is_live_execution": True,
            "api_endpoint": "https://agent.tinyfish.ai/v1/automation/run",
            "timestamp": timestamp,
            "limitations": "Independent verification reflects publicly indexable corporate records retrieved via live TinyFish web agents. Does not constitute guarantee of commercial solvency or signature authenticity.",
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
