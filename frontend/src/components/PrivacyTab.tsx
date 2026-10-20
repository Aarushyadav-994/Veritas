"use client";

import React, { useState } from "react";
import { ShieldAlert, Download, Lock, CheckCircle2, EyeOff, AlertTriangle } from "lucide-react";

interface PrivacyFinding {
  info_type: string;
  count: number;
  pages: number[];
  risk_level: string;
  disclosure_risk: string;
  mitigation: string;
  masked_samples: string[];
}

interface PrivacyTabProps {
  sessionId: string;
  privacyData?: {
    overall_exposure: string;
    total_detections: number;
    findings: PrivacyFinding[];
    can_redact: boolean;
    redaction_targets_count: number;
  };
}

export const PrivacyTab: React.FC<PrivacyTabProps> = ({
  sessionId,
  privacyData,
}) => {
  const [isRedacting, setIsRedacting] = useState(false);

  const getExposureBadge = (exposure: string) => {
    switch (exposure) {
      case "CRITICAL":
      case "HIGH":
        return "bg-[#FEF3F2] text-[#B42318] border-[#FDA29B]";
      case "MODERATE":
        return "bg-[#FFFAEB] text-[#B54708] border-[#FEDF89]";
      case "LOW":
        return "bg-[#ECFDF3] text-[#067647] border-[#A6F4C5]";
      default:
        return "bg-[#F5F3ED] text-[#667085] border-[#D0D5DD]";
    }
  };

  const handleDownloadRedacted = () => {
    setIsRedacting(true);
    // Trigger download from backend
    window.open(`http://localhost:8000/api/redact/${sessionId}`, "_blank");
    setTimeout(() => setIsRedacting(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Privacy Overview Banner */}
      <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#EFECE4]">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[#15202B] text-[#AD925B]">
                Statutory Data Privacy Audit
              </span>
              <span
                className={`text-xs font-mono px-2 py-0.5 rounded border font-semibold ${getExposureBadge(
                  privacyData?.overall_exposure || "MINIMAL"
                )}`}
              >
                {privacyData?.overall_exposure || "LOW"} EXPOSURE
              </span>
            </div>
            <h3 className="font-serif text-lg font-bold text-[#15202B] mt-2">
              Personally Identifiable Information (PII) Audit & Redaction Terminal
            </h3>
            <p className="text-xs text-[#667085] mt-0.5">
              Identifies direct tax credentials, national identity numbers, banking coordinates, and communication channels.
            </p>
          </div>

          {/* Genuine Redaction Trigger Button */}
          {privacyData?.can_redact && (
            <button
              onClick={handleDownloadRedacted}
              disabled={isRedacting}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-[#15202B] hover:bg-[#263238] text-[#FFFFFF] text-xs font-medium border border-[#15202B] transition-colors cursor-pointer shrink-0 disabled:opacity-50"
            >
              <EyeOff className="w-3.5 h-3.5 text-[#AD925B]" />
              <span>{isRedacting ? "Generating Scrubbed Copy..." : "Download Redacted PDF"}</span>
            </button>
          )}
        </div>

        {/* Stats Strip */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4 pt-2 text-xs">
          <div className="p-3 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Total Identified Items</span>
            <span className="font-mono text-base font-bold text-[#15202B]">
              {privacyData?.total_detections || 0} sensitive fields
            </span>
          </div>

          <div className="p-3 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Redaction Technology</span>
            <span className="font-mono text-xs font-medium text-[#067647]">
              PyMuPDF True Byte Scrubbing
            </span>
          </div>

          <div className="p-3 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Statutory Compliance Scope</span>
            <span className="font-mono text-xs text-[#15202B]">
              DPDP Act 2023 / UIDAI / GDPR
            </span>
          </div>
        </div>
      </div>

      {/* Findings Table */}
      <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded overflow-hidden shadow-xs">
        <div className="p-4 bg-[#FAFAF8] border-b border-[#EFECE4] flex items-center justify-between">
          <h4 className="font-mono text-xs font-bold uppercase text-[#15202B]">
            Identified Sensitive Data Entities ({privacyData?.findings?.length || 0})
          </h4>
          <span className="text-[11px] text-[#667085]">
            Values below are displayed with safe masking
          </span>
        </div>

        <div className="divide-y divide-[#EFECE4]">
          {privacyData?.findings?.map((f, idx) => (
            <div key={idx} className="p-5 space-y-3 text-xs">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-[#15202B] text-sm">{f.info_type}</span>
                  <span className="text-[11px] text-[#667085] font-mono">
                    ({f.count} {f.count === 1 ? "match" : "matches"} on {f.pages.length === 1 ? "page" : "pages"} {f.pages.join(", ")})
                  </span>
                </div>

                <span
                  className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-semibold ${getExposureBadge(
                    f.risk_level
                  )}`}
                >
                  {f.risk_level} Exposure
                </span>
              </div>

              {/* Masked Samples */}
              <div className="flex items-center space-x-2 text-[11px]">
                <span className="font-mono text-[#667085]">Masked Evidence:</span>
                <div className="flex flex-wrap gap-1.5">
                  {f.masked_samples.map((sample, sIdx) => (
                    <span
                      key={sIdx}
                      className="font-mono bg-[#F5F3ED] text-[#263238] px-2 py-0.5 rounded border border-[#D0D5DD]"
                    >
                      {sample}
                    </span>
                  ))}
                </div>
              </div>

              {/* Risk & Mitigation */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                <div>
                  <span className="font-bold text-[#B42318] block mb-1">Disclosure Risk:</span>
                  <p className="text-[#475467] leading-relaxed">{f.disclosure_risk}</p>
                </div>

                <div>
                  <span className="font-bold text-[#067647] block mb-1">Prescribed Mitigation:</span>
                  <p className="text-[#475467] leading-relaxed">{f.mitigation}</p>
                </div>
              </div>
            </div>
          ))}

          {(!privacyData?.findings || privacyData.findings.length === 0) && (
            <div className="text-center py-10 text-xs text-[#667085]">
              No sensitive personal identifiers or banking coordinates identified in the document text stream.
            </div>
          )}
        </div>
      </div>

      {/* True Redaction Guarantee Notice */}
      <div className="bg-[#FAFAF8] border border-[#D0D5DD] rounded p-4 text-xs text-[#667085] flex items-start space-x-2.5">
        <Lock className="w-4 h-4 text-[#AD925B] mt-0.5 shrink-0" />
        <div>
          <span className="font-bold text-[#15202B]">Cryptographic & Binary Redaction Integrity: </span>
          <span>
            Veritas AI executes true PDF stream redaction via PyMuPDF&apos;s native <code className="font-mono text-[11px] bg-[#EFECE4] px-1 py-0.5 rounded">apply_redactions()</code> pipeline.
            The underlying text glyphs and coordinates are permanently stripped from the binary stream, preventing reverse extraction or copy-paste retrieval.
          </span>
        </div>
      </div>
    </div>
  );
};
