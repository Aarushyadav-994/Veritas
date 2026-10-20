"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { UploadWorkspace } from "@/components/UploadWorkspace";
import { ContractOverviewBar } from "@/components/ContractOverviewBar";
import { ClauseFindingsTab } from "@/components/ClauseFindingsTab";
import { TinyFishTab } from "@/components/TinyFishTab";
import { IntegrityTab } from "@/components/IntegrityTab";
import { PrivacyTab } from "@/components/PrivacyTab";
import { DocumentReaderTab } from "@/components/DocumentReaderTab";
import { CopilotDrawer } from "@/components/CopilotDrawer";
import { RedraftModal } from "@/components/RedraftModal";
import { FileText, ShieldAlert, Building2, Eye, Lock, MessageSquare } from "lucide-react";

type ActiveTab = "clauses" | "tinyfish" | "integrity" | "privacy" | "reader";

export default function Home() {
  const [sessionData, setSessionData] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLoadingDemo, setIsLoadingDemo] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

  const [activeTab, setActiveTab] = useState<ActiveTab>("clauses");
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [selectedClauseForRedraft, setSelectedClauseForRedraft] = useState<any>(null);
  const [isRedraftModalOpen, setIsRedraftModalOpen] = useState(false);
  const [isInvestigating, setIsInvestigating] = useState(false);

  // File Upload Handler
  const handleFileUpload = async (file: File) => {
    setIsProcessing(true);
    setErrorMessage(undefined);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Upload failed with status ${res.status}`);
      }

      const data = await res.json();
      setSessionData(data);
      setActiveTab("clauses");
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to process document");
    } finally {
      setIsProcessing(false);
    }
  };

  // Load Demo Fixture Handler
  const handleLoadDemo = async () => {
    setIsLoadingDemo(true);
    setErrorMessage(undefined);

    try {
      const res = await fetch("http://localhost:8000/api/demo", {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error("Failed to load demo contract fixture");
      }

      const data = await res.json();
      setSessionData(data);
      setActiveTab("clauses");
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to load demo preset");
    } finally {
      setIsLoadingDemo(false);
    }
  };

  // Reset Session Handler
  const handleResetSession = async () => {
    if (sessionData?.session_id) {
      try {
        await fetch(`http://localhost:8000/api/session/${sessionData.session_id}/reset`, {
          method: "POST",
        });
      } catch (e) {
        console.error(e);
      }
    }
    setSessionData(null);
    setActiveTab("clauses");
    setIsCopilotOpen(false);
    setErrorMessage(undefined);
  };

  // Export PDF Handler
  const handleExportPdf = () => {
    if (!sessionData?.session_id) return;
    window.open(`http://localhost:8000/api/export/pdf/${sessionData.session_id}`, "_blank");
  };

  // Rerun TinyFish Investigation Handler
  const handleRerunInvestigation = async (entityName: string, regId?: string) => {
    if (!sessionData?.session_id) return;
    setIsInvestigating(true);

    try {
      const res = await fetch("http://localhost:8000/api/investigate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionData.session_id,
          entity_name: entityName,
          registration_id: regId,
        }),
      });

      if (res.ok) {
        const updatedTf = await res.json();
        setSessionData((prev: any) => ({
          ...prev,
          tinyfish: updatedTf,
        }));
      }
    } catch (err) {
      console.error("TinyFish rerun failed:", err);
    } finally {
      setIsInvestigating(false);
    }
  };

  // Open Draft Alternative Modal
  const handleOpenDraftAlternative = (clause: any) => {
    setSelectedClauseForRedraft(clause);
    setIsRedraftModalOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F5F3ED]">
      <Header
        hasDocument={!!sessionData}
        filename={sessionData?.filename}
        isDemo={sessionData?.is_demo}
        onReset={handleResetSession}
        onExport={handleExportPdf}
        onLoadDemo={handleLoadDemo}
        isLoadingDemo={isLoadingDemo}
        engineName={sessionData?.analysis_engine}
        tinyfishStatus={sessionData?.tinyfish?.investigation_status}
      />

      <main className="flex-1 pb-16">
        {!sessionData ? (
          <UploadWorkspace
            onFileUpload={handleFileUpload}
            onLoadDemo={handleLoadDemo}
            isProcessing={isProcessing}
            isLoadingDemo={isLoadingDemo}
            errorMessage={errorMessage}
          />
        ) : (
          <div className="space-y-6">
            {/* Overview & Score Bar */}
            <ContractOverviewBar
              documentSummary={sessionData.document_summary}
              overallRisk={sessionData.overall_risk}
              pageCount={sessionData.page_count}
              engineName={sessionData.analysis_engine}
              renewalTimeline={sessionData.renewal_timeline}
              financialAnalytics={sessionData.financial_analytics}
            />

            {/* Main Tabs Container */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {/* Tab Navigation Toolbar */}
              <div className="border-b border-[#D0D5DD] flex items-center justify-between overflow-x-auto whitespace-nowrap mb-6">
                <nav className="flex space-x-2">
                  <button
                    onClick={() => setActiveTab("clauses")}
                    className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-colors flex items-center space-x-1.5 cursor-pointer ${
                      activeTab === "clauses"
                        ? "border-[#15202B] text-[#15202B] font-bold"
                        : "border-transparent text-[#667085] hover:text-[#15202B] hover:border-[#D0D5DD]"
                    }`}
                  >
                    <ShieldAlert className="w-3.5 h-3.5 text-[#B42318]" />
                    <span>Clause Risk Audit</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#FAFAF8] text-[#263238] border border-[#EFECE4]">
                      {sessionData.clauses?.length || 0}
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveTab("tinyfish")}
                    className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-colors flex items-center space-x-1.5 cursor-pointer ${
                      activeTab === "tinyfish"
                        ? "border-[#15202B] text-[#15202B] font-bold"
                        : "border-transparent text-[#667085] hover:text-[#15202B] hover:border-[#D0D5DD]"
                    }`}
                  >
                    <Building2 className="w-3.5 h-3.5 text-[#AD925B]" />
                    <span>Counterparty Investigation</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#15202B] text-[#AD925B]">
                      TinyFish
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveTab("integrity")}
                    className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-colors flex items-center space-x-1.5 cursor-pointer ${
                      activeTab === "integrity"
                        ? "border-[#15202B] text-[#15202B] font-bold"
                        : "border-transparent text-[#667085] hover:text-[#15202B] hover:border-[#D0D5DD]"
                    }`}
                  >
                    <Eye className="w-3.5 h-3.5 text-[#067647]" />
                    <span>Integrity & ELA Forensics</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#FAFAF8] text-[#263238] border border-[#EFECE4]">
                      {sessionData.integrity?.indicators?.length || 0}
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveTab("privacy")}
                    className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-colors flex items-center space-x-1.5 cursor-pointer ${
                      activeTab === "privacy"
                        ? "border-[#15202B] text-[#15202B] font-bold"
                        : "border-transparent text-[#667085] hover:text-[#15202B] hover:border-[#D0D5DD]"
                    }`}
                  >
                    <Lock className="w-3.5 h-3.5 text-[#B54708]" />
                    <span>Privacy & Redaction</span>
                    {sessionData.privacy?.total_detections > 0 && (
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#FEF3F2] text-[#B42318] border border-[#FDA29B]">
                        {sessionData.privacy.total_detections} PII
                      </span>
                    )}
                  </button>

                  <button
                    onClick={() => setActiveTab("reader")}
                    className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-colors flex items-center space-x-1.5 cursor-pointer ${
                      activeTab === "reader"
                        ? "border-[#15202B] text-[#15202B] font-bold"
                        : "border-transparent text-[#667085] hover:text-[#15202B] hover:border-[#D0D5DD]"
                    }`}
                  >
                    <FileText className="w-3.5 h-3.5 text-[#667085]" />
                    <span>Document Reader</span>
                  </button>
                </nav>

                {/* Copilot Toggle Button */}
                <button
                  onClick={() => setIsCopilotOpen(true)}
                  className="inline-flex items-center space-x-1.5 text-xs font-medium px-3 py-1.5 rounded bg-[#15202B] text-[#FFFFFF] hover:bg-[#263238] transition-colors cursor-pointer shrink-0 ml-4 mb-1"
                >
                  <MessageSquare className="w-3.5 h-3.5 text-[#AD925B]" />
                  <span>Legal Copilot</span>
                </button>
              </div>

              {/* Active Tab Panel */}
              <div>
                {activeTab === "clauses" && (
                  <ClauseFindingsTab
                    clauses={sessionData.clauses || []}
                    missingProtections={sessionData.missing_protections || []}
                    crossClauseAnalysis={sessionData.cross_clause_analysis}
                    onDraftAlternative={handleOpenDraftAlternative}
                  />
                )}

                {activeTab === "tinyfish" && (
                  <TinyFishTab
                    sessionId={sessionData.session_id}
                    tinyfishData={sessionData.tinyfish}
                    counterpartyProfile={sessionData.counterparty_profile}
                    onRerunInvestigation={handleRerunInvestigation}
                    isInvestigating={isInvestigating}
                  />
                )}

                {activeTab === "integrity" && (
                  <IntegrityTab
                    integrityData={sessionData.integrity}
                    metadata={sessionData.metadata}
                  />
                )}

                {activeTab === "privacy" && (
                  <PrivacyTab
                    sessionId={sessionData.session_id}
                    privacyData={sessionData.privacy}
                  />
                )}

                {activeTab === "reader" && (
                  <DocumentReaderTab
                    pages={sessionData.pages || []}
                    fullText={sessionData.full_text || ""}
                  />
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Slide-out Contextual Legal Copilot Drawer */}
      {sessionData && (
        <CopilotDrawer
          sessionId={sessionData.session_id}
          isOpen={isCopilotOpen}
          onClose={() => setIsCopilotOpen(false)}
          documentTitle={sessionData.filename}
        />
      )}

      {/* Alternative Clause Redrafting Modal */}
      {sessionData && (
        <RedraftModal
          sessionId={sessionData.session_id}
          clause={selectedClauseForRedraft}
          isOpen={isRedraftModalOpen}
          onClose={() => {
            setIsRedraftModalOpen(false);
            setSelectedClauseForRedraft(null);
          }}
        />
      )}
    </div>
  );
}
