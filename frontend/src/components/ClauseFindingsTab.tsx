"use client";

import React, { useState } from "react";
import { AlertTriangle, CheckCircle, HelpCircle, FileEdit, ArrowRight, ShieldAlert, Filter, CheckCircle2, Link2, Scale, ExternalLink } from "lucide-react";

interface ClauseItem {
  clause_id: string;
  clause_title?: string;
  category: string;
  risk_level: string;
  section_number?: string;
  page_number: number;
  exact_quotation?: string;
  original_excerpt: string;
  quotation_verified?: boolean;
  verification_status?: string;
  plain_english_explanation: string;
  benefiting_party?: string;
  potential_consequence: string;
  severity_justification?: string;
  suggested_next_step: string;
  suggested_alternative_wording?: string;
  confidence_level?: string;
  confidence_explanation?: string;
  related_clause_ids?: string[];
  evidence?: string;
}

interface CrossClauseItem {
  interaction_id: string;
  relationship_type: string;
  clauses_involved: string[];
  nature: string;
  risk_severity: string;
  analysis: string;
  negotiation_action: string;
}

interface MissingProtection {
  protection_name: string;
  status: "PRESENT" | "PARTIALLY PRESENT" | "ABSENT" | "UNCERTAIN";
  importance: string;
  existing_language_cited?: string;
  why_it_matters: string;
  residual_gap?: string;
  recommended_addition: string;
}

interface ClauseFindingsTabProps {
  clauses: ClauseItem[];
  crossClauseAnalysis?: CrossClauseItem[];
  missingProtections: MissingProtection[];
  onDraftAlternative: (clause: ClauseItem) => void;
}

export const ClauseFindingsTab: React.FC<ClauseFindingsTabProps> = ({
  clauses,
  crossClauseAnalysis,
  missingProtections,
  onDraftAlternative,
}) => {
  const [filter, setFilter] = useState<string>("ALL");
  const [subTab, setSubTab] = useState<"clauses" | "cross" | "protections">("clauses");

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

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "PRESENT":
        return "bg-[#ECFDF3] text-[#067647] border-[#A6F4C5]";
      case "PARTIALLY PRESENT":
        return "bg-[#FFFAEB] text-[#B54708] border-[#FEDF89]";
      case "ABSENT":
        return "bg-[#FEF3F2] text-[#B42318] border-[#FDA29B]";
      default:
        return "bg-[#F5F3ED] text-[#667085] border-[#D0D5DD]";
    }
  };

  const highRiskCount = clauses.filter((c) => c.risk_level === "HIGH RISK").length;
  const modRiskCount = clauses.filter((c) => c.risk_level === "MODERATE RISK").length;

  return (
    <div className="space-y-6">
      {/* Sub-navigation Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#D0D5DD]">
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setSubTab("clauses")}
            className={`px-3 py-1.5 rounded text-xs font-medium border transition-colors cursor-pointer ${
              subTab === "clauses"
                ? "bg-[#15202B] text-[#FFFFFF] border-[#15202B]"
                : "bg-[#FFFFFF] text-[#667085] border-[#D0D5DD] hover:border-[#15202B]"
            }`}
          >
            Clause Risk Audit ({clauses.length})
          </button>

          <button
            onClick={() => setSubTab("cross")}
            className={`px-3 py-1.5 rounded text-xs font-medium border transition-colors cursor-pointer flex items-center space-x-1.5 ${
              subTab === "cross"
                ? "bg-[#15202B] text-[#FFFFFF] border-[#15202B]"
                : "bg-[#FFFFFF] text-[#667085] border-[#D0D5DD] hover:border-[#15202B]"
            }`}
          >
            <Link2 className="w-3.5 h-3.5" />
            <span>Cross-Clause Reasoning ({crossClauseAnalysis?.length || 0})</span>
          </button>

          <button
            onClick={() => setSubTab("protections")}
            className={`px-3 py-1.5 rounded text-xs font-medium border transition-colors cursor-pointer ${
              subTab === "protections"
                ? "bg-[#15202B] text-[#FFFFFF] border-[#15202B]"
                : "bg-[#FFFFFF] text-[#667085] border-[#D0D5DD] hover:border-[#15202B]"
            }`}
          >
            Protections Matrix ({missingProtections.length})
          </button>
        </div>

        {subTab === "clauses" && (
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
                {btn === "ALL" ? "All" : btn.replace(" RISK", "")}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* VIEW 1: CLAUSE RISK AUDIT TABLE */}
      {subTab === "clauses" && (
        <div className="space-y-4">
          {filteredClauses.map((clause, idx) => {
            const quotationText = clause.exact_quotation || clause.original_excerpt;

            return (
              <div
                key={clause.clause_id || idx}
                className="bg-[#FFFFFF] border border-[#D0D5DD] rounded overflow-hidden shadow-xs"
              >
                {/* Header Strip */}
                <div className="p-4 bg-[#FAFAF8] border-b border-[#EFECE4] flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono font-bold text-xs text-[#15202B]">
                      {clause.clause_id}
                    </span>
                    <span className="text-xs text-[#667085]">•</span>
                    <span className="text-xs font-bold text-[#15202B]">
                      {clause.clause_title || clause.category}
                    </span>
                    <span className="text-[11px] text-[#667085] font-mono">
                      (Page {clause.page_number})
                    </span>

                    {clause.benefiting_party && (
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#EFECE4] text-[#263238]">
                        Benefiting: <strong>{clause.benefiting_party}</strong>
                      </span>
                    )}
                  </div>

                  <div className="flex items-center space-x-2 shrink-0">
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
                    >
                      <FileEdit className="w-3 h-3" />
                      <span>Draft Alternative</span>
                    </button>
                  </div>
                </div>

                {/* Body Content */}
                <div className="p-5 space-y-4 text-xs">
                  {/* Verbatim Excerpt Block with Verification Badge */}
                  <div className="bg-[#F5F3ED] border-l-2 border-[#AD925B] p-3.5 rounded-r space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono uppercase text-[#667085]">
                        Supporting Quotation (Verified Against Source Text)
                      </span>
                      {clause.quotation_verified ? (
                        <span className="inline-flex items-center space-x-1 text-[10px] font-mono text-[#067647] bg-[#ECFDF3] px-2 py-0.5 rounded border border-[#A6F4C5]">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>Verified Verbatim (Page {clause.page_number})</span>
                        </span>
                      ) : (
                        <span className="text-[10px] font-mono text-[#B54708] bg-[#FFFAEB] px-2 py-0.5 rounded border border-[#FEDF89]">
                          Unverified Paraphrase
                        </span>
                      )}
                    </div>
                    <p className="font-serif italic text-xs text-[#263238] leading-relaxed">
                      &ldquo;{quotationText}&rdquo;
                    </p>
                  </div>

                  {/* 2-Column Structured Analysis */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="font-bold text-[#15202B] block mb-1">Plain-English Meaning:</span>
                      <p className="text-[#475467] leading-relaxed">{clause.plain_english_explanation}</p>
                    </div>

                    <div>
                      <span className="font-bold text-[#15202B] block mb-1">Severity Justification:</span>
                      <p className="text-[#475467] leading-relaxed">{clause.severity_justification || "Evaluated against commercial contract standards."}</p>
                    </div>
                  </div>

                  {/* Consequences & Recommended Action */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-[#EFECE4]">
                    <div>
                      <span className="font-bold text-[#B42318] block mb-1">Potential Consequences:</span>
                      <p className="text-[#475467] leading-relaxed">{clause.potential_consequence}</p>
                    </div>

                    <div>
                      <span className="font-bold text-[#067647] block mb-1">Recommended Negotiation Action:</span>
                      <p className="text-[#475467] leading-relaxed">{clause.suggested_next_step}</p>
                    </div>
                  </div>

                  {/* Related Clauses & Confidence Footer */}
                  <div className="pt-2 border-t border-[#EFECE4] flex flex-wrap items-center justify-between gap-2 text-[11px] text-[#667085]">
                    {clause.related_clause_ids && clause.related_clause_ids.length > 0 && (
                      <div className="flex items-center space-x-1.5">
                        <Link2 className="w-3 h-3 text-[#AD925B]" />
                        <span className="font-bold text-[#263238]">Interacting Clauses:</span>
                        <div className="flex flex-wrap gap-1">
                          {clause.related_clause_ids.map((rc, rIdx) => (
                            <span key={rIdx} className="font-mono bg-[#FAFAF8] px-1.5 py-0.2 rounded border border-[#EFECE4] text-[#15202B]">
                              {rc}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {clause.confidence_level && (
                      <div className="font-mono text-[10px] text-[#98A2B3]">
                        Confidence: {clause.confidence_level}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* VIEW 2: CROSS-CLAUSE REASONING */}
      {subTab === "cross" && (
        <div className="space-y-4">
          <div className="p-4 bg-[#FFFFFF] border border-[#D0D5DD] rounded">
            <h4 className="font-serif text-base font-bold text-[#15202B]">
              Cross-Clause Dependency & Compounding Exposure Analysis
            </h4>
            <p className="text-xs text-[#667085] mt-1 leading-relaxed">
              Contracts cannot be audited in isolation. This engine analyzes how separate provisions interact,
              evaluating whether liability caps carve out indemnity, whether committed terms restrict exit rights,
              and how renewal windows compound price adjustments.
            </p>
          </div>

          {crossClauseAnalysis && crossClauseAnalysis.length > 0 ? (
            crossClauseAnalysis.map((item, idx) => (
              <div key={idx} className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-5 space-y-3 shadow-xs text-xs">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#EFECE4]">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-sm text-[#15202B]">{item.relationship_type}</span>
                    <span className="text-[#667085]">•</span>
                    <div className="flex items-center space-x-1">
                      {item.clauses_involved.map((clName, cIdx) => (
                        <span key={cIdx} className="font-mono bg-[#F5F3ED] px-1.5 py-0.5 rounded border border-[#D0D5DD] text-[#263238]">
                          {clName}
                        </span>
                      ))}
                    </div>
                  </div>

                  <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-semibold ${getRiskBadge(item.risk_severity)}`}>
                    {item.risk_severity}
                  </span>
                </div>

                <div>
                  <span className="font-bold text-[#15202B] block mb-1">Compounding Risk Analysis:</span>
                  <p className="text-[#263238] leading-relaxed">{item.analysis}</p>
                </div>

                <div className="pt-2 border-t border-[#EFECE4] bg-[#FAFAF8] p-3 rounded border border-[#EFECE4]">
                  <span className="font-bold text-[#067647] block mb-1">Recommended Harmonization Action:</span>
                  <p className="text-[#475467] leading-relaxed">{item.negotiation_action}</p>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-10 bg-[#FFFFFF] border border-[#D0D5DD] rounded text-xs text-[#667085]">
              No adverse cross-clause conflicts detected in the extracted text.
            </div>
          )}
        </div>
      )}

      {/* VIEW 3: DEFENSIVE PROTECTIONS MATRIX (4-STATE) */}
      {subTab === "protections" && (
        <div className="space-y-4">
          <div className="p-4 bg-[#FFFFFF] border border-[#D0D5DD] rounded">
            <h4 className="font-serif text-base font-bold text-[#15202B]">
              Defensive Protections Matrix (4-Tier Audit)
            </h4>
            <p className="text-xs text-[#667085] mt-1 leading-relaxed">
              Audits standard contractual protections using an evidence-grounded 4-state classifier:
              <strong className="text-[#067647]"> PRESENT</strong> (substantially exists and balanced),
              <strong className="text-[#B54708]"> PARTIALLY PRESENT</strong> (exists but one-sided or has residual gaps),
              <strong className="text-[#B42318]"> ABSENT</strong> (omitted completely), or
              <strong className="text-[#667085]"> UNCERTAIN</strong> (insufficient extraction context).
            </p>
          </div>

          <div className="space-y-3">
            {missingProtections.map((mp, i) => (
              <div key={i} className="p-5 bg-[#FFFFFF] border border-[#D0D5DD] rounded text-xs space-y-3 shadow-xs">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#EFECE4]">
                  <div>
                    <span className="font-bold text-sm text-[#15202B]">{mp.protection_name}</span>
                    <span className="text-[11px] text-[#667085] font-mono ml-2">
                      Priority: {mp.importance}
                    </span>
                  </div>

                  <span className={`text-[10px] font-mono uppercase px-2.5 py-1 rounded border font-bold ${getStatusBadge(mp.status)}`}>
                    Status: {mp.status}
                  </span>
                </div>

                {mp.existing_language_cited && (
                  <div className="p-3 bg-[#FAFAF8] border border-[#EFECE4] rounded">
                    <span className="text-[10px] font-mono uppercase text-[#667085] block mb-1">
                      Existing Language Identified in Document:
                    </span>
                    <p className="font-serif italic text-xs text-[#263238] leading-relaxed">
                      {mp.existing_language_cited}
                    </p>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <span className="font-bold text-[#15202B] block mb-1">Why It Matters:</span>
                    <p className="text-[#475467] leading-relaxed">{mp.why_it_matters}</p>
                  </div>

                  <div>
                    <span className="font-bold text-[#B42318] block mb-1">Residual Gap:</span>
                    <p className="text-[#475467] leading-relaxed">{mp.residual_gap || "None."}</p>
                  </div>
                </div>

                <div className="bg-[#ECFDF3] p-3 rounded border border-[#A6F4C5] text-[11px] font-mono text-[#15202B]">
                  <span className="text-[#067647] font-bold">Suggested Wording Addition / Harmonization: </span>
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
