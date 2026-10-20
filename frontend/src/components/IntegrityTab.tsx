"use client";

import React, { useState } from "react";
import { ShieldCheck, AlertCircle, Eye, Sliders, Info, FileCode, CheckCircle2 } from "lucide-react";

interface Indicator {
  finding: string;
  page_or_region: string;
  detection_method: string;
  observed_evidence: string;
  severity: string;
  interpretation: string;
  limitations: string;
  recommended_manual_check: string;
}

interface IntegrityTabProps {
  integrityData?: {
    section_title: string;
    overall_integrity_status: string;
    disclaimer: string;
    indicators: Indicator[];
    ela?: {
      enabled: boolean;
      original_preview?: string;
      ela_preview?: string;
      explanation?: string;
      limitations?: string;
      manual_check?: string;
      reason?: string;
    };
  };
  metadata?: Record<string, any>;
}

export const IntegrityTab: React.FC<IntegrityTabProps> = ({
  integrityData,
  metadata,
}) => {
  const [elaViewMode, setElaViewMode] = useState<"side-by-side" | "ela-only" | "original-only">("side-by-side");

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
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

  return (
    <div className="space-y-8">
      {/* Overview & Metadata Summary Banner */}
      <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#EFECE4]">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[#15202B] text-[#AD925B]">
                Forensic File Auditing
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#ECFDF3] text-[#067647] border border-[#A6F4C5] font-semibold">
                {integrityData?.overall_integrity_status || "Qualified Verification"}
              </span>
            </div>
            <h3 className="font-serif text-lg font-bold text-[#15202B] mt-2">
              {integrityData?.section_title || "Document Integrity Indicators"}
            </h3>
            <p className="text-xs text-[#667085] mt-0.5">
              Structural analysis of PDF stream dictionaries, generation timestamps, and compression levels.
            </p>
          </div>

          <div className="text-xs text-right">
            <span className="text-[11px] font-mono text-[#667085]">Audit Scope</span>
            <div className="font-semibold text-[#15202B]">Metadata & Error Level Analysis</div>
          </div>
        </div>

        {/* Metadata Matrix Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 pt-2 text-xs">
          <div className="p-2.5 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Creation Date</span>
            <span className="font-mono text-[#15202B] truncate block">
              {metadata?.creation_date || "Not explicitly recorded"}
            </span>
          </div>

          <div className="p-2.5 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Modification Date</span>
            <span className="font-mono text-[#15202B] truncate block">
              {metadata?.modification_date || "Not explicitly recorded"}
            </span>
          </div>

          <div className="p-2.5 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Producer Software</span>
            <span className="font-mono text-[#15202B] truncate block">
              {metadata?.producer || "Enterprise Document Pipeline"}
            </span>
          </div>

          <div className="p-2.5 bg-[#FAFAF8] rounded border border-[#EFECE4]">
            <span className="text-[#667085] text-[10px] uppercase font-mono block">Encryption / Security</span>
            <span className="font-mono text-[#067647] font-semibold block">
              {metadata?.encryption || "None (Standard Open)"}
            </span>
          </div>
        </div>
      </div>

      {/* Error Level Analysis (ELA) Interactive Forensic Viewer */}
      {integrityData?.ela?.enabled && (
        <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6 shadow-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#EFECE4]">
            <div>
              <span className="text-xs font-mono uppercase text-[#AD925B] font-bold">
                Image Compression Forensic Visualizer
              </span>
              <h4 className="font-serif text-base font-bold text-[#15202B]">
                Error Level Analysis (ELA) — Primary Surface
              </h4>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center space-x-1 bg-[#F5F3ED] p-1 rounded border border-[#D0D5DD] text-xs">
              <button
                onClick={() => setElaViewMode("side-by-side")}
                className={`px-2.5 py-1 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                  elaViewMode === "side-by-side" ? "bg-[#15202B] text-[#FFFFFF]" : "text-[#667085]"
                }`}
              >
                Side-by-Side
              </button>
              <button
                onClick={() => setElaViewMode("ela-only")}
                className={`px-2.5 py-1 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                  elaViewMode === "ela-only" ? "bg-[#15202B] text-[#FFFFFF]" : "text-[#667085]"
                }`}
              >
                ELA Map Only
              </button>
              <button
                onClick={() => setElaViewMode("original-only")}
                className={`px-2.5 py-1 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                  elaViewMode === "original-only" ? "bg-[#15202B] text-[#FFFFFF]" : "text-[#667085]"
                }`}
              >
                Original Only
              </button>
            </div>
          </div>

          {/* Interactive Image Render */}
          <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
            {(elaViewMode === "side-by-side" || elaViewMode === "original-only") && (
              <div className="space-y-2">
                <span className="text-[11px] font-mono font-semibold text-[#263238]">
                  Original Document Surface (Page 1)
                </span>
                <div className="border border-[#D0D5DD] rounded overflow-hidden bg-[#FAFAF8] p-2 flex items-center justify-center max-h-96">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={integrityData.ela.original_preview}
                    alt="Original document surface"
                    className="max-h-88 object-contain"
                  />
                </div>
              </div>
            )}

            {(elaViewMode === "side-by-side" || elaViewMode === "ela-only") && (
              <div className="space-y-2">
                <span className="text-[11px] font-mono font-semibold text-[#AD925B]">
                  ELA Compression Variance Map (15x Difference Scale)
                </span>
                <div className="border border-[#15202B] rounded overflow-hidden bg-[#15202B] p-2 flex items-center justify-center max-h-96">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={integrityData.ela.ela_preview}
                    alt="Error Level Analysis map"
                    className="max-h-88 object-contain"
                  />
                </div>
              </div>
            )}
          </div>

          {/* ELA Forensic Commentary */}
          <div className="mt-4 pt-4 border-t border-[#EFECE4] space-y-2 text-xs">
            <p className="text-[#263238] leading-relaxed">
              <strong>Technical Mechanism: </strong>
              {integrityData.ela.explanation}
            </p>
            <div className="p-3 bg-[#FAFAF8] border border-[#EFECE4] rounded text-[11px] text-[#667085]">
              <strong className="text-[#B54708]">Analytical Safeguard: </strong>
              {integrityData.ela.limitations}
            </div>
          </div>
        </div>
      )}

      {/* Forensic Indicators List */}
      <div className="space-y-4">
        <h4 className="font-mono text-xs font-bold uppercase text-[#15202B]">
          Observed Structural Indicators ({integrityData?.indicators?.length || 0})
        </h4>

        {integrityData?.indicators?.map((ind, idx) => (
          <div
            key={idx}
            className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-5 space-y-3 shadow-xs text-xs"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#EFECE4]">
              <div className="flex items-center space-x-2">
                <span className="font-bold text-[#15202B]">{ind.finding}</span>
                <span className="text-[#667085]">•</span>
                <span className="font-mono text-[#667085]">{ind.page_or_region}</span>
              </div>
              <span
                className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-semibold ${getSeverityBadge(
                  ind.severity
                )}`}
              >
                {ind.severity} Severity
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="font-bold text-[#667085] block mb-1">Observed Evidence:</span>
                <p className="font-mono text-[11px] bg-[#FAFAF8] p-2 rounded border border-[#EFECE4] text-[#15202B]">
                  {ind.observed_evidence}
                </p>
              </div>

              <div>
                <span className="font-bold text-[#667085] block mb-1">Analytical Interpretation:</span>
                <p className="text-[#263238] leading-relaxed">{ind.interpretation}</p>
              </div>
            </div>

            <div className="pt-2 border-t border-[#EFECE4] grid grid-cols-1 md:grid-cols-2 gap-4 text-[11px] text-[#667085]">
              <div>
                <span className="font-bold text-[#B54708]">Limitations: </span>
                <span>{ind.limitations}</span>
              </div>
              <div>
                <span className="font-bold text-[#067647]">Recommended Action: </span>
                <span>{ind.recommended_manual_check}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
