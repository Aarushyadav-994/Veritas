"use client";

import React, { useState } from "react";
import { AlertTriangle, Info, Calendar, Users, FileCheck, ChevronDown, ChevronUp, Scale, Clock, DollarSign } from "lucide-react";

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
    dimension_scores?: {
      financial_exposure?: number;
      contractual_imbalance?: number;
      data_confidentiality?: number;
      operational_continuity?: number;
      drafting_ambiguity?: number;
    };
  };
  pageCount: number;
  engineName?: string;
  renewalTimeline?: {
    calculation_status?: string;
    effective_date?: string;
    initial_term_months?: number;
    initial_term_end_date?: string;
    notice_period_days?: number;
    notice_deadline_date?: string;
    arithmetic_formula?: string;
    consequences_of_missed_deadline?: string;
  };
  financialAnalytics?: {
    liability_cap?: {
      formula_identified?: string;
      illustrative_cap_amount?: string;
      calculation_methodology?: string;
      assumptions?: string[];
      carve_outs_detected?: string;
    };
    payment_penalties?: {
      stated_rate?: string;
      simple_annualized_rate?: string;
      effective_annual_rate?: string;
      is_compounded?: boolean;
      dispute_window_days?: number;
      payment_due_days?: number;
    };
  };
}

export const ContractOverviewBar: React.FC<ContractOverviewBarProps> = ({
  documentSummary,
  overallRisk,
  pageCount,
  engineName,
  renewalTimeline,
  financialAnalytics,
}) => {
  const [showMethodology, setShowMethodology] = useState(false);
  const [showCalculators, setShowCalculators] = useState(false);

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
                <span>Methodology & Dimensions</span>
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

        {/* Dynamic Contract Arithmetic Callout Strip */}
        <div className="mt-3 pt-3 border-t border-[#EFECE4] flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-4">
            {renewalTimeline?.notice_deadline_date && (
              <div className="flex items-center space-x-1.5 text-[#263238] bg-[#FAFAF8] px-2.5 py-1 rounded border border-[#EFECE4]">
                <Clock className="w-3.5 h-3.5 text-[#B54708]" />
                <span className="text-[#667085]">Non-Renewal Deadline:</span>
                <span className="font-mono font-bold text-[#15202B]">{renewalTimeline.notice_deadline_date}</span>
              </div>
            )}

            {financialAnalytics?.liability_cap?.illustrative_cap_amount && (
              <div className="flex items-center space-x-1.5 text-[#263238] bg-[#FAFAF8] px-2.5 py-1 rounded border border-[#EFECE4]">
                <DollarSign className="w-3.5 h-3.5 text-[#AD925B]" />
                <span className="text-[#667085]">Illustrative Liability Ceiling:</span>
                <span className="font-mono font-bold text-[#15202B]">{financialAnalytics.liability_cap.illustrative_cap_amount}</span>
              </div>
            )}
          </div>

          <button
            onClick={() => setShowCalculators(!showCalculators)}
            className="text-xs text-[#AD925B] hover:text-[#8F7644] underline flex items-center space-x-1 cursor-pointer ml-auto"
          >
            <span>View Calculation Arithmetic</span>
            {showCalculators ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>
        </div>

        {/* Expandable Calculation Assumptions Drawer */}
        {showCalculators && (
          <div className="mt-3 pt-3 border-t border-[#EFECE4] bg-[#FAFAF8] p-4 rounded border border-[#D0D5DD] text-xs space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-[#EFECE4]">
              <span className="font-mono font-bold uppercase text-[#15202B]">
                Dynamic Milestone & Financial Arithmetic
              </span>
              <span className="text-[10px] font-mono text-[#667085]">
                Extracted Deterministically from Contract Covenants
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3 bg-[#FFFFFF] rounded border border-[#EFECE4] space-y-1.5">
                <span className="font-bold text-[#15202B] block">Renewal Timeline Arithmetic:</span>
                <p className="font-mono text-[11px] text-[#263238]">{renewalTimeline?.arithmetic_formula}</p>
                <div className="text-[11px] text-[#667085]">
                  <span>Initial Term: {renewalTimeline?.initial_term_months} months. Notice Window: {renewalTimeline?.notice_period_days} days.</span>
                </div>
                <div className="text-[11px] text-[#B42318] pt-1 border-t border-[#EFECE4]">
                  {renewalTimeline?.consequences_of_missed_deadline}
                </div>
              </div>

              <div className="p-3 bg-[#FFFFFF] rounded border border-[#EFECE4] space-y-1.5">
                <span className="font-bold text-[#15202B] block">Liability Cap Calculation Methodology:</span>
                <p className="font-mono text-[11px] text-[#263238]">{financialAnalytics?.liability_cap?.calculation_methodology}</p>
                <div className="text-[11px] text-[#667085]">
                  <span>Carve-Outs Detected: {financialAnalytics?.liability_cap?.carve_outs_detected}</span>
                </div>
                <div className="text-[11px] text-[#B54708] pt-1 border-t border-[#EFECE4]">
                  {financialAnalytics?.liability_cap?.assumptions?.[0]}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Expandable Scoring Methodology & Contributing Factors Drawer */}
        {showMethodology && (
          <div className="mt-4 pt-4 border-t border-[#EFECE4] bg-[#FAFAF8] p-4 rounded border border-[#D0D5DD]">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-xs font-mono uppercase font-bold text-[#15202B]">
                  Deterministic Multi-Dimensional Scoring Model
                </h4>
                <p className="text-xs text-[#667085] mt-1 leading-relaxed">
                  {overallRisk?.methodology_explanation ||
                    "Score reflects weighted distribution across Financial (30%), Imbalance (25%), Data Security (20%), Operational (15%), and Ambiguity (10%)."}
                </p>
              </div>
              <span className="text-[10px] font-mono text-[#667085] bg-[#FFFFFF] px-2 py-0.5 border border-[#D0D5DD] rounded">
                Non-Evaluative Decision Support
              </span>
            </div>

            {/* Dimension Breakdown Gauges */}
            {overallRisk?.dimension_scores && (
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 mt-3 pt-3 border-t border-[#EFECE4] text-[11px]">
                <div className="p-2 bg-[#FFFFFF] rounded border border-[#EFECE4] text-center">
                  <div className="text-[#667085] font-mono text-[10px]">Financial (30%)</div>
                  <div className="font-bold font-mono text-sm text-[#B42318]">{overallRisk.dimension_scores.financial_exposure}/100</div>
                </div>
                <div className="p-2 bg-[#FFFFFF] rounded border border-[#EFECE4] text-center">
                  <div className="text-[#667085] font-mono text-[10px]">Imbalance (25%)</div>
                  <div className="font-bold font-mono text-sm text-[#B42318]">{overallRisk.dimension_scores.contractual_imbalance}/100</div>
                </div>
                <div className="p-2 bg-[#FFFFFF] rounded border border-[#EFECE4] text-center">
                  <div className="text-[#667085] font-mono text-[10px]">Data & Privacy (20%)</div>
                  <div className="font-bold font-mono text-sm text-[#B54708]">{overallRisk.dimension_scores.data_confidentiality}/100</div>
                </div>
                <div className="p-2 bg-[#FFFFFF] rounded border border-[#EFECE4] text-center">
                  <div className="text-[#667085] font-mono text-[10px]">Operational (15%)</div>
                  <div className="font-bold font-mono text-sm text-[#B42318]">{overallRisk.dimension_scores.operational_continuity}/100</div>
                </div>
                <div className="p-2 bg-[#FFFFFF] rounded border border-[#EFECE4] text-center">
                  <div className="text-[#667085] font-mono text-[10px]">Ambiguity (10%)</div>
                  <div className="font-bold font-mono text-sm text-[#667085]">{overallRisk.dimension_scores.drafting_ambiguity}/100</div>
                </div>
              </div>
            )}

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
