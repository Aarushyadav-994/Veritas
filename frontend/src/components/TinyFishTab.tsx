"use client";

import React, { useState } from "react";
import { Search, ExternalLink, ShieldCheck, AlertTriangle, CheckCircle2, RefreshCw, Globe, Building2, Info } from "lucide-react";

interface EvidenceItem {
  verification_question: string;
  source_name: string;
  source_url: string;
  information_retrieved: string;
  timestamp: string;
  status: string;
  limitations: string;
}

interface TinyFishTabProps {
  sessionId: string;
  tinyfishData?: {
    entity_searched: string;
    investigation_status: string;
    is_live_execution: boolean;
    api_endpoint: string;
    configuration_notice?: string;
    timestamp: string;
    limitations: string;
    evidence_items: EvidenceItem[];
  };
  counterpartyProfile?: {
    primary_counterparty?: string;
    stated_registration_or_cin?: string;
    jurisdiction_state?: string;
    registered_address?: string;
    official_domain?: string;
  };
  onRerunInvestigation: (entityName: string, regId?: string) => void;
  isInvestigating?: boolean;
}

export const TinyFishTab: React.FC<TinyFishTabProps> = ({
  sessionId,
  tinyfishData,
  counterpartyProfile,
  onRerunInvestigation,
  isInvestigating,
}) => {
  const [entityNameInput, setEntityNameInput] = useState(
    counterpartyProfile?.primary_counterparty || tinyfishData?.entity_searched || "Vertex Dynamics Technologies Private Limited"
  );
  const [regIdInput, setRegIdInput] = useState(
    counterpartyProfile?.stated_registration_or_cin || "U72900DL2021PTC384910"
  );

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Verified against source":
        return "bg-[#ECFDF3] text-[#067647] border-[#A6F4C5]";
      case "Partially verified":
        return "bg-[#FFFAEB] text-[#B54708] border-[#FEDF89]";
      case "Conflicting evidence":
        return "bg-[#FEF3F2] text-[#B42318] border-[#FDA29B]";
      case "Simulated Demonstration":
        return "bg-[#F5F3ED] text-[#785E2F] border-[#D0D5DD]";
      default:
        return "bg-[#F5F3ED] text-[#667085] border-[#D0D5DD]";
    }
  };

  const isSimulated = !tinyfishData?.is_live_execution;

  return (
    <div className="space-y-6">
      {/* Title & Agentic Verification Summary */}
      <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[#EFECE4]">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[#15202B] text-[#AD925B]">
                TinyFish Agentic Web Intelligence
              </span>
              <span
                className={`text-[10px] font-mono px-2 py-0.5 rounded border font-semibold ${getStatusBadge(
                  tinyfishData?.investigation_status || "Pending"
                )}`}
              >
                {tinyfishData?.investigation_status || "Awaiting Query"}
              </span>
            </div>
            <h3 className="font-serif text-lg font-bold text-[#15202B] mt-2">
              Counterparty Entity & Public Registry Investigation
            </h3>
            <p className="text-xs text-[#667085] mt-0.5">
              Automated autonomous web agents verify stated corporate registrations against official government registries and corporate records.
            </p>
          </div>

          {/* Transparent Live vs Simulation indicator */}
          <div className="text-right text-xs">
            <div className="text-[11px] font-mono text-[#667085]">Execution Mode</div>
            <div className="font-bold text-[#15202B]">
              {tinyfishData?.is_live_execution ? (
                <span className="text-[#067647]">Live TinyFish Web Agent</span>
              ) : (
                <span className="text-[#B54708]">Transparent Demo Preset</span>
              )}
            </div>
            <div className="text-[10px] font-mono text-[#98A2B3] mt-0.5">
              {tinyfishData?.timestamp || "Latest Run"}
            </div>
          </div>
        </div>

        {/* Configuration Notice if API Key not set */}
        {tinyfishData?.configuration_notice && (
          <div className="mt-4 p-3.5 bg-[#FFFAEB] border border-[#FEDF89] rounded text-xs text-[#7A271A] flex items-start space-x-2">
            <Info className="w-4 h-4 mt-0.5 shrink-0 text-[#B54708]" />
            <div>
              <span className="font-bold">Credential Notice: </span>
              <span>{tinyfishData.configuration_notice}</span>
            </div>
          </div>
        )}

        {/* Counterparty Parameter Form */}
        <div className="mt-5 grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
          <div className="md:col-span-5 space-y-1">
            <label className="text-xs font-mono font-semibold text-[#263238]">
              Target Legal Entity Name
            </label>
            <input
              type="text"
              value={entityNameInput}
              onChange={(e) => setEntityNameInput(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#D0D5DD] rounded bg-[#FAFAF8] focus:bg-[#FFFFFF] focus:outline-none focus:border-[#15202B]"
              placeholder="e.g. Vertex Dynamics Technologies Pvt Ltd"
            />
          </div>

          <div className="md:col-span-4 space-y-1">
            <label className="text-xs font-mono font-semibold text-[#263238]">
              Stated Registration / CIN / Tax ID
            </label>
            <input
              type="text"
              value={regIdInput}
              onChange={(e) => setRegIdInput(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#D0D5DD] rounded bg-[#FAFAF8] focus:bg-[#FFFFFF] focus:outline-none focus:border-[#15202B]"
              placeholder="e.g. U72900DL2021PTC384910"
            />
          </div>

          <div className="md:col-span-3">
            <button
              onClick={() => onRerunInvestigation(entityNameInput, regIdInput)}
              disabled={isInvestigating}
              className="w-full py-2 px-3 text-xs font-medium rounded bg-[#15202B] hover:bg-[#263238] text-[#FFFFFF] flex items-center justify-center space-x-1.5 transition-colors cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-[#AD925B] ${isInvestigating ? "animate-spin" : ""}`} />
              <span>{isInvestigating ? "Investigating..." : "Dispatch TinyFish Agent"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Evidence Findings Grid */}
      <div className="space-y-4">
        <h4 className="font-mono text-xs font-bold uppercase text-[#15202B]">
          Retrieved Investigation Evidence ({tinyfishData?.evidence_items?.length || 0} Sources)
        </h4>

        {tinyfishData?.evidence_items?.map((ev, idx) => (
          <div
            key={idx}
            className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-5 space-y-3 shadow-xs"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#EFECE4]">
              <div className="flex items-center space-x-2">
                <Building2 className="w-4 h-4 text-[#AD925B]" />
                <span className="font-bold text-xs text-[#15202B]">{ev.source_name}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span
                  className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-semibold ${getStatusBadge(
                    ev.status
                  )}`}
                >
                  {ev.status}
                </span>
                <a
                  href={ev.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-[#AD925B] hover:text-[#8F7644] flex items-center space-x-0.5"
                >
                  <span className="text-[11px]">View Source</span>
                  <ExternalLink className="w-3 h-3 ml-0.5" />
                </a>
              </div>
            </div>

            <div className="text-xs">
              <span className="font-bold text-[#667085] block mb-1">Audit Verification Question:</span>
              <p className="text-[#15202B] font-medium">{ev.verification_question}</p>
            </div>

            <div className="bg-[#F5F3ED] p-3 rounded border border-[#EFECE4] text-xs font-mono">
              <span className="text-[10px] uppercase text-[#667085] block mb-1">Information Retrieved:</span>
              <p className="text-[#263238] whitespace-pre-wrap">{ev.information_retrieved}</p>
            </div>

            <div className="pt-2 border-t border-[#EFECE4] text-[11px] text-[#667085]">
              <span className="font-bold text-[#B54708]">Forensic Limitation: </span>
              <span>{ev.limitations}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Mandatory Statutory Disclaimer Card */}
      <div className="bg-[#FAFAF8] border border-[#D0D5DD] rounded p-4 text-xs text-[#667085]">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="w-4 h-4 text-[#B54708] mt-0.5 shrink-0" />
          <div className="space-y-1">
            <span className="font-bold text-[#15202B]">Scope Limitation & Objective Neutrality:</span>
            <p className="leading-relaxed">
              Public registry verification confirms official entity registration filings, tax identifiers, or web domain presence.
              It does NOT establish that an individual signatory possesses authorized Power of Attorney, that a particular contract is legally binding, or that the counterparty is commercially solvent.
              Failed lookups do not conclusively establish fraudulent intent.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
