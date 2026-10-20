"use client";

import React, { useState } from "react";
import { AlertTriangle, CheckCircle, HelpCircle, FileEdit, ArrowRight, ShieldAlert, Sparkles, Filter } from "lucide-react";

interface ClauseItem {
  clause_id: string;
  category: string;
  risk_level: string;
  original_excerpt: string;
  page_number: number;
  plain_english_explanation: string;
  why_it_matters: string;
  potential_consequence: string;
  suggested_next_step: string;
  evidence?: string;
}

interface MissingProtection {
  protection_name: string;
  importance: string;
  why_it_matters: string;
  recommended_addition: string;
}

interface ClauseFindingsTabProps {
  clauses: ClauseItem[];
  missingProtections: MissingProtection[];
  onDraftAlternative: (clause: ClauseItem) => void;
}

export const ClauseFindingsTab: React.FC<ClauseFindingsTabProps> = ({
  clauses,
  missingProtections,
  onDraftAlternative,
}) => {
  const [filter, setFilter] = useState<string>("ALL");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const filteredClauses = clauses.filter((c) => {
    if (filter === "ALL") return true;
    return c.risk_level === filter;
  });

  const getRiskBadge = (level: string) => {
    switch (level) {
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

  const highRiskCount = clauses.filter((c) => c.risk_level === "HIGH RISK").length;
  const modRiskCount = clauses.filter((c) => c.risk_level === "MODERATE RISK").length;

  return (
    <div className="space-y-8">
      {/* Filter and Overview Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#D0D5DD]">
        <div>
          <h3 className="font-serif text-lg font-bold text-[#15202B]">
            Clause-Level Risk Audit ({clauses.length} evaluated)
          </h3>
          <p className="text-xs text-[#667085]">
            {highRiskCount} high-risk exposure provisions and {modRiskCount} moderate terms requiring negotiation.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center space-x-1.5 text-xs">
          <span className="text-[#667085] font-mono mr-1 flex items-center">
            <Filter className="w-3 h-3 mr-1" />
            Filter:
          </span>
          {["ALL", "HIGH RISK", "MODERATE RISK", "LOW APPARENT RISK"].map((btn) => (
            <button
              key={btn}
              onClick={() => setFilter(btn)}
              className={`px-2.5 py-1 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                filter === btn
                  ? "bg-[#15202B] text-[#FFFFFF]"
                  : "bg-[#FFFFFF] text-[#667085] border border-[#D0D5DD] hover:border-[#15202B]"
              }`}
            >
              {btn === "ALL" ? "All Clauses" : btn.replace(" RISK", "")}
            </button>
          ))}
        </div>
      </div>

      {/* Clause Cards List */}
      <div className="space-y-4">
        {filteredClauses.map((clause, idx) => {
          const isExpanded = expandedId === clause.clause_id;

          return (
            <div
              key={clause.clause_id || idx}
              className="bg-[#FFFFFF] border border-[#D0D5DD] rounded overflow-hidden shadow-xs"
            >
              {/* Clause Header Bar */}
              <div className="p-4 bg-[#FAFAF8] border-b border-[#EFECE4] flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center space-x-2.5">
                  <span className="font-mono font-bold text-xs text-[#15202B]">
                    {clause.clause_id}
                  </span>
                  <span className="text-xs text-[#667085]">•</span>
                  <span className="text-xs font-semibold text-[#263238]">
                    {clause.category}
                  </span>
                  <span className="text-[11px] text-[#667085] font-mono">
                    (Page {clause.page_number})
                  </span>
                </div>

                <div className="flex items-center space-x-2.5">
                  <span
                    className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-semibold ${getRiskBadge(
                      clause.risk_level
                    )}`}
                  >
                    {clause.risk_level}
                  </span>

                  <button
                    onClick={() => onDraftAlternative(clause)}
                    className="inline-flex items-center space-x-1 text-xs font-medium px-2.5 py-1 rounded bg-[#FFFFFF] text-[#AD925B] border border-[#AD925B] hover:bg-[#F5F3ED] transition-colors cursor-pointer"
                    title="Generate balanced negotiation draft for this clause"
                  >
                    <FileEdit className="w-3 h-3" />
                    <span>Draft Alternative</span>
                  </button>
                </div>
              </div>

              {/* Clause Body Content */}
              <div className="p-5 space-y-4 text-xs">
                {/* Verbatim Excerpt */}
                <div className="bg-[#F5F3ED] border-l-2 border-[#AD925B] p-3.5 rounded-r">
                  <div className="text-[10px] font-mono uppercase text-[#667085] mb-1">
                    Verbatim Document Excerpt
                  </div>
                  <p className="font-serif italic text-xs text-[#263238] leading-relaxed">
                    &ldquo;{clause.original_excerpt}&rdquo;
                  </p>
                </div>

                {/* Structured Analysis Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                  <div>
                    <span className="font-bold text-[#15202B] block mb-1">Plain-English Meaning:</span>
                    <p className="text-[#475467] leading-relaxed">{clause.plain_english_explanation}</p>
                  </div>

                  <div>
                    <span className="font-bold text-[#15202B] block mb-1">Why It Matters:</span>
                    <p className="text-[#475467] leading-relaxed">{clause.why_it_matters}</p>
                  </div>
                </div>

                {/* Consequences & Next Step */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-[#EFECE4]">
                  <div>
                    <span className="font-bold text-[#B42318] block mb-1">Potential Consequence:</span>
                    <p className="text-[#475467] leading-relaxed">{clause.potential_consequence}</p>
                  </div>

                  <div>
                    <span className="font-bold text-[#067647] block mb-1">Recommended Next Step:</span>
                    <p className="text-[#475467] leading-relaxed">{clause.suggested_next_step}</p>
                  </div>
                </div>

                {clause.evidence && (
                  <div className="text-[11px] font-mono text-[#667085] pt-1">
                    <span className="font-bold">Text Evidence: </span>
                    <span className="bg-[#FAFAF8] px-1.5 py-0.5 rounded border border-[#EFECE4]">
                      {clause.evidence}
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {filteredClauses.length === 0 && (
          <div className="text-center py-10 bg-[#FFFFFF] border border-[#D0D5DD] rounded text-xs text-[#667085]">
            No clauses found under filter &quot;{filter}&quot;.
          </div>
        )}
      </div>

      {/* Relevant Omissions & Missing Protections Subsection */}
      {missingProtections && missingProtections.length > 0 && (
        <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6">
          <div className="flex items-center space-x-2 mb-2">
            <ShieldAlert className="w-4 h-4 text-[#B54708]" />
            <h4 className="font-serif text-base font-bold text-[#15202B]">
              Omitted Protections & Missing Covenants
            </h4>
          </div>
          <p className="text-xs text-[#667085] mb-4">
            The following standard defensive clauses are absent from the agreement, creating potential legal blindspots:
          </p>

          <div className="space-y-3">
            {missingProtections.map((mp, i) => (
              <div key={i} className="p-3.5 bg-[#FFFAEB] border border-[#FEDF89] rounded text-xs">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-[#B54708]">{mp.protection_name}</span>
                  <span className="text-[10px] font-mono uppercase bg-[#FEDF89] text-[#7A271A] px-2 py-0.5 rounded">
                    {mp.importance} Priority
                  </span>
                </div>
                <p className="text-[#263238] leading-relaxed mb-2">{mp.why_it_matters}</p>
                <div className="bg-[#FFFFFF] p-2.5 rounded border border-[#FEDF89] text-[11px] font-mono text-[#263238]">
                  <span className="text-[#AD925B] font-bold">Suggested Insertion: </span>
                  {mp.recommended_addition}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
