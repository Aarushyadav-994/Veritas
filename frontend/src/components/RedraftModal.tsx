"use client";

import React, { useState } from "react";
import { Copy, Check, X, FileEdit, ArrowRight, Sparkles, Scale, Info } from "lucide-react";

interface RedraftResult {
  clause_id: string;
  category: string;
  original_wording: string;
  why_unfavorable: string;
  proposed_alternative: string;
  explanation_of_changes: string;
  negotiation_notes: string;
}

interface RedraftModalProps {
  sessionId: string;
  clause: {
    clause_id: string;
    category: string;
    original_excerpt: string;
  } | null;
  isOpen: boolean;
  onClose: () => void;
}

export const RedraftModal: React.FC<RedraftModalProps> = ({
  sessionId,
  clause,
  isOpen,
  onClose,
}) => {
  const [goal, setGoal] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<RedraftResult | null>(null);
  const [copied, setCopied] = useState(false);

  if (!isOpen || !clause) return null;

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch("http://localhost:8000/api/copilot/redraft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          clause_id: clause.clause_id,
          category: clause.category,
          original_excerpt: clause.original_excerpt,
          negotiation_goal: goal || undefined,
        }),
      });

      if (!res.ok) throw new Error("Failed to generate redraft");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    if (!result?.proposed_alternative) return;
    navigator.clipboard.writeText(result.proposed_alternative);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 bg-[#15202B]/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col">
        {/* Modal Header */}
        <div className="p-5 bg-[#FAFAF8] border-b border-[#EFECE4] flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[#15202B] text-[#AD925B]">
                Bilateral Negotiation Redrafter
              </span>
              <span className="font-mono text-xs text-[#263238] font-bold">
                {clause.clause_id} ({clause.category})
              </span>
            </div>
            <h3 className="font-serif text-base font-bold text-[#15202B] mt-1">
              Draft Balanced Counter-Proposal
            </h3>
          </div>

          <button
            onClick={onClose}
            className="text-[#667085] hover:text-[#15202B] p-1 rounded hover:bg-[#EFECE4] cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 text-xs flex-1">
          {/* Original Unfavorable Excerpt */}
          <div className="space-y-1.5">
            <span className="font-mono font-bold uppercase text-[10px] text-[#667085]">
              Current Document Language (Unfavorable)
            </span>
            <div className="p-3 bg-[#FEF3F2] border border-[#FDA29B] rounded font-serif italic text-xs text-[#263238]">
              &ldquo;{clause.original_excerpt}&rdquo;
            </div>
          </div>

          {/* Goal Input & Generate Action */}
          {!result && (
            <div className="space-y-3 pt-2">
              <label className="font-bold text-[#15202B] block">
                Negotiation Stance / Target Balance (Optional):
              </label>
              <input
                type="text"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="e.g. Mutual 30-day notice, cap liability to 12 months fees, include cure period"
                className="w-full px-3 py-2 text-xs border border-[#D0D5DD] rounded bg-[#FAFAF8] focus:bg-[#FFFFFF] focus:outline-none focus:border-[#15202B]"
              />

              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full py-2.5 px-4 rounded bg-[#15202B] hover:bg-[#263238] text-[#FFFFFF] font-medium text-xs flex items-center justify-center space-x-2 transition-colors cursor-pointer disabled:opacity-50"
              >
                <Scale className="w-3.5 h-3.5 text-[#AD925B]" />
                <span>{isGenerating ? "Synthesizing Balanced Legal Language..." : "Generate Counter-Proposal"}</span>
              </button>
            </div>
          )}

          {/* Redraft Results View */}
          {result && (
            <div className="space-y-4 pt-2">
              {/* Proposed Alternative */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold uppercase text-[10px] text-[#067647]">
                    Proposed Bilateral Alternative
                  </span>
                  <button
                    onClick={handleCopy}
                    className="inline-flex items-center space-x-1 text-xs font-medium px-2 py-1 rounded bg-[#F5F3ED] text-[#15202B] hover:bg-[#E8E1D3] border border-[#D0D5DD] transition-colors cursor-pointer"
                  >
                    {copied ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-[#067647]" />
                        <span className="text-[#067647]">Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5 text-[#AD925B]" />
                        <span>Copy Clause</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="p-4 bg-[#ECFDF3] border border-[#A6F4C5] rounded font-serif text-xs text-[#15202B] leading-relaxed">
                  {result.proposed_alternative}
                </div>
              </div>

              {/* Rationale & Changes */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                <div className="p-3 bg-[#FAFAF8] border border-[#EFECE4] rounded">
                  <span className="font-bold text-[#15202B] block mb-1">Specific Modifications Made:</span>
                  <p className="text-[#475467] leading-relaxed">{result.explanation_of_changes}</p>
                </div>

                <div className="p-3 bg-[#FAFAF8] border border-[#EFECE4] rounded">
                  <span className="font-bold text-[#15202B] block mb-1">Negotiation Tactical Notes:</span>
                  <p className="text-[#475467] leading-relaxed">{result.negotiation_notes}</p>
                </div>
              </div>

              {/* Reset draft button */}
              <button
                onClick={() => setResult(null)}
                className="text-xs text-[#667085] hover:text-[#15202B] underline pt-1 cursor-pointer"
              >
                Adjust negotiation goal & regenerate
              </button>
            </div>
          )}
        </div>

        {/* Modal Footer / Disclaimer */}
        <div className="p-4 bg-[#FAFAF8] border-t border-[#EFECE4] flex items-center justify-between text-[11px] text-[#667085]">
          <span className="flex items-center space-x-1.5">
            <Info className="w-3.5 h-3.5 text-[#AD925B]" />
            <span>Negotiation draft for legal review. Not a warranty of enforceability.</span>
          </span>
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded bg-[#FFFFFF] border border-[#D0D5DD] text-[#263238] hover:bg-[#F5F3ED] cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
