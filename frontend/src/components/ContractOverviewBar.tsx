"use client";

import React, { useState } from "react";
import { AlertTriangle, Info, Calendar, Users, FileCheck, ChevronDown, ChevronUp } from "lucide-react";

interface ContractOverviewBarProps {
  documentSummary: {
    document_type?: string;
    parties?: Array<{ name: string; role: string; jurisdiction?: string }>;
    effective_date?: string;
    term_duration?: string;
    executive_takeaway?: string;
  };
  overallRisk: {
    score: number;
    category: string;
    methodology_explanation?: string;
    contributing_factors?: Array<{ factor: string; impact: string; detail: string }>;
  };
  pageCount: number;
  engineName?: string;
}

export const ContractOverviewBar: React.FC<ContractOverviewBarProps> = ({
  documentSummary,
  overallRisk,
  pageCount,
  engineName,
}) => {
  const [showMethodology, setShowMethodology] = useState(false);

  const score = overallRisk?.score || 0;
  const category = overallRisk?.category || "NEEDS REVIEW";

  const getBadgeStyle = (cat: string) => {
    switch (cat) {
      case "HIGH RISK":
        return "bg-[#FEF3F2] text-[#B42318] border-[#FDA29B]";
      case "MODERATE RISK":
        return "bg-[#FFFAEB] text-[#B54708] border-[#FEDF89]";
      case "LOW APPARENT RISK":
        return "bg-[#ECFDF3] text-[#067647] border-[#A6F4C5]";
      default:
        return "bg-[#F5F3ED] text-[#667085] border-[#D0D5DD]";
    }
  };

  return (
    <div className="bg-[#FFFFFF] border-b border-[#D0D5DD]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
        {/* Top Summary Row */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[#F5F3ED] text-[#263238] border border-[#D0D5DD]">
                {documentSummary?.document_type || "Commercial Contract"}
              </span>
              <span className="text-xs text-[#667085]">
                {pageCount} {pageCount === 1 ? "page" : "pages"} analyzed
              </span>
              {engineName && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#FAFAF8] text-[#667085] border border-[#EFECE4]">
                  {engineName}
                </span>
              )}
            </div>
            <h2 className="font-serif text-xl sm:text-2xl text-[#15202B] font-bold">
              {documentSummary?.executive_takeaway || "Contract Review & Forensic Risk Audit"}
            </h2>
          </div>

          {/* Transparent Risk Score Badge */}
          <div className="flex items-center space-x-3 shrink-0">
            <div className="text-right hidden sm:block">
              <div className="text-[11px] font-mono uppercase text-[#667085]">Calculated Risk Index</div>
              <button
                onClick={() => setShowMethodology(!showMethodology)}
                className="text-xs text-[#AD925B] hover:text-[#8F7644] underline flex items-center justify-end space-x-0.5 cursor-pointer ml-auto"
              >
                <span>Methodology & Factors</span>
                {showMethodology ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
              </button>
            </div>

            <div className={`px-4 py-2 rounded border flex items-center space-x-3 ${getBadgeStyle(category)}`}>
              <div className="text-center font-mono font-bold text-2xl leading-none">
                {score}
                <span className="text-xs font-normal text-opacity-70">/100</span>
              </div>
              <div className="border-l border-current pl-3 py-0.5">
                <div className="text-[10px] font-mono tracking-wider uppercase font-semibold">Assessment</div>
                <div className="font-bold text-xs uppercase tracking-tight">{category}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Contract Core Metadata Strip */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 mt-4 border-t border-[#EFECE4] text-xs">
          <div className="flex items-center space-x-2 text-[#263238]">
            <Users className="w-4 h-4 text-[#AD925B] shrink-0" />
            <div className="truncate">
              <span className="text-[#667085]">Signatories: </span>
              <span className="font-medium">
                {documentSummary?.parties?.map((p) => p.name).join(" vs ") || "Identified Parties"}
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-2 text-[#263238]">
            <Calendar className="w-4 h-4 text-[#AD925B] shrink-0" />
            <div>
              <span className="text-[#667085]">Effective Date: </span>
              <span className="font-medium">{documentSummary?.effective_date || "Stated in execution copy"}</span>
            </div>
          </div>

          <div className="flex items-center space-x-2 text-[#263238]">
            <FileCheck className="w-4 h-4 text-[#AD925B] shrink-0" />
            <div>
              <span className="text-[#667085]">Initial Term: </span>
              <span className="font-medium">{documentSummary?.term_duration || "Per contract terms"}</span>
            </div>
          </div>
        </div>

        {/* Expandable Scoring Methodology & Contributing Factors Drawer */}
        {showMethodology && (
          <div className="mt-4 pt-4 border-t border-[#EFECE4] bg-[#FAFAF8] p-4 rounded border border-[#D0D5DD]">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-xs font-mono uppercase font-bold text-[#15202B]">
                  Transparent Scoring Methodology
                </h4>
                <p className="text-xs text-[#667085] mt-1 leading-relaxed">
                  {overallRisk?.methodology_explanation ||
                    "Score reflects the presence of unilateral termination provisions, uncapped indemnities, automatic rollover terms, and omitted statutory protections."}
                </p>
              </div>
              <span className="text-[10px] font-mono text-[#667085] bg-[#FFFFFF] px-2 py-0.5 border border-[#D0D5DD] rounded">
                Non-Evaluative Decision Support
              </span>
            </div>

            {overallRisk?.contributing_factors && overallRisk.contributing_factors.length > 0 && (
              <div className="mt-3 pt-3 border-t border-[#EFECE4]">
                <div className="text-[11px] font-bold text-[#263238] mb-2">Contributing Factors:</div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                  {overallRisk.contributing_factors.map((f, i) => (
                    <div key={i} className="flex items-start space-x-2 p-2 bg-[#FFFFFF] border border-[#EFECE4] rounded">
                      <span
                        className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded uppercase mt-0.5 ${
                          f.impact === "HIGH"
                            ? "bg-[#FEF3F2] text-[#B42318]"
                            : "bg-[#FFFAEB] text-[#B54708]"
                        }`}
                      >
                        {f.impact}
                      </span>
                      <div>
                        <div className="font-semibold text-[#15202B]">{f.factor}</div>
                        <div className="text-[11px] text-[#667085]">{f.detail}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
