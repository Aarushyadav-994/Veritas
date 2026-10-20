"use client";

import React, { useState, useRef } from "react";
import { Upload, FileText, AlertCircle, ShieldCheck, Eye, Search, Lock, ArrowRight, CheckCircle2 } from "lucide-react";

interface UploadWorkspaceProps {
  onFileUpload: (file: File) => void;
  onLoadDemo: () => void;
  isProcessing: boolean;
  isLoadingDemo: boolean;
  errorMessage?: string;
}

export const UploadWorkspace: React.FC<UploadWorkspaceProps> = ({
  onFileUpload,
  onLoadDemo,
  isProcessing,
  isLoadingDemo,
  errorMessage,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [clientError, setClientError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const validateAndProcess = (file: File) => {
    setClientError(null);
    const validExtensions = [".pdf", ".png", ".jpg", ".jpeg"];
    const ext = "." + file.name.split(".").pop()?.toLowerCase();

    if (!validExtensions.includes(ext)) {
      setClientError(`Unsupported file format '${ext}'. Please upload a PDF, PNG, or JPEG agreement.`);
      return;
    }

    if (file.size > 25 * 1024 * 1024) {
      setClientError("File exceeds the maximum allowable 25 MB limit.");
      return;
    }

    if (file.size === 0) {
      setClientError("Uploaded document appears to be empty (0 bytes).");
      return;
    }

    onFileUpload(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndProcess(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndProcess(e.target.files[0]);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 sm:px-6">
      {/* Editorial Title Block */}
      <div className="text-center max-w-2xl mx-auto mb-10">
        <div className="inline-flex items-center space-x-2 text-xs font-mono uppercase px-3 py-1 bg-[#FFFFFF] border border-[#D0D5DD] rounded text-[#263238] mb-4">
          <ShieldCheck className="w-3.5 h-3.5 text-[#067647]" />
          <span>Forensic Document Investigation & Risk Intelligence</span>
        </div>
        <h1 className="font-serif text-3xl sm:text-4xl text-[#15202B] font-bold tracking-tight">
          Review the agreement before you sign.
        </h1>
        <p className="mt-3 text-sm sm:text-base text-[#667085] leading-relaxed">
          Veritas AI combines clause-level legal risk extraction, PDF metadata forensics,
          privacy exposure auditing, and TinyFish corporate counterparty investigation into one cohesive brief.
        </p>
      </div>

      {/* Error Notifications */}
      {(clientError || errorMessage) && (
        <div className="mb-6 p-4 rounded bg-[#FEF3F2] border border-[#FDA29B] text-[#B42318] text-xs flex items-start space-x-2.5">
          <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
          <div>
            <span className="font-bold">Ingestion Warning: </span>
            <span>{clientError || errorMessage}</span>
          </div>
        </div>
      )}

      {/* Primary Workstation Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Drag & Drop Ingestion Zone */}
        <div className="lg:col-span-7 bg-[#FFFFFF] border border-[#D0D5DD] rounded p-6 shadow-xs">
          <div className="flex items-center justify-between pb-4 border-b border-[#EFECE4] mb-4">
            <span className="text-xs font-mono font-bold uppercase text-[#15202B]">
              Document Ingestion Terminal
            </span>
            <span className="text-xs text-[#667085]">PDF, PNG, JPG (up to 25 MB)</span>
          </div>

          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => !isProcessing && fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded p-8 sm:p-10 text-center cursor-pointer transition-all ${
              isDragOver
                ? "border-[#AD925B] bg-[#F5F3ED]"
                : "border-[#D0D5DD] hover:border-[#15202B] bg-[#FAFAF8]"
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileInputChange}
              accept=".pdf,.png,.jpg,.jpeg"
              className="hidden"
            />

            <div className="w-12 h-12 rounded bg-[#FFFFFF] border border-[#D0D5DD] mx-auto flex items-center justify-center mb-4">
              <Upload className="w-5 h-5 text-[#15202B]" />
            </div>

            {isProcessing ? (
              <div className="space-y-2">
                <p className="font-serif font-bold text-sm text-[#15202B]">
                  Analyzing Contract Structure...
                </p>
                <p className="text-xs text-[#667085]">
                  Executing page extraction, clause segmentation, privacy scan, and metadata forensics.
                </p>
                <div className="w-48 h-1 bg-[#EFECE4] mx-auto rounded overflow-hidden mt-3">
                  <div className="w-full h-full bg-[#AD925B] animate-pulse" />
                </div>
              </div>
            ) : (
              <div className="space-y-1.5">
                <p className="font-serif font-bold text-sm text-[#15202B]">
                  Drag & drop your legal agreement here
                </p>
                <p className="text-xs text-[#667085]">
                  or click to select file from your workstation
                </p>
                <p className="text-[11px] text-[#98A2B3] pt-2">
                  Client agreements, Master Services Agreements, NDAs, SaaS terms, vendor contracts.
                </p>
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-[#EFECE4] flex items-center justify-between text-[11px] text-[#667085]">
            <span className="flex items-center space-x-1">
              <Lock className="w-3 h-3 text-[#AD925B]" />
              <span>In-memory session processing. Never stored permanently.</span>
            </span>
            <span>PyMuPDF Engine</span>
          </div>
        </div>

        {/* Right Column: Instant Evaluation / Demo & Capability Matrix */}
        <div className="lg:col-span-5 space-y-6">
          {/* Quick Demo Loader Card */}
          <div className="bg-[#15202B] text-[#FFFFFF] rounded p-6 border border-[#263238] shadow-xs">
            <div className="flex items-center space-x-2 text-xs font-mono text-[#AD925B] uppercase mb-2">
              <FileText className="w-3.5 h-3.5" />
              <span>Hackathon Evaluation Preset</span>
            </div>
            <h3 className="font-serif font-bold text-base text-[#FFFFFF] mb-2">
              Cloud Services Agreement (Sample)
            </h3>
            <p className="text-xs text-[#D0D5DD] leading-relaxed mb-4">
              Instantly test the full workflow with a prepared enterprise agreement featuring unfavorable
              unilateral termination, automatic 24-month renewal, uncapped indemnity, synthetic tax IDs, and metadata traces.
            </p>

            <button
              onClick={onLoadDemo}
              disabled={isLoadingDemo || isProcessing}
              className="w-full py-2.5 px-4 rounded bg-[#AD925B] hover:bg-[#8F7644] text-[#15202B] font-medium text-xs flex items-center justify-center space-x-2 transition-colors cursor-pointer disabled:opacity-50"
            >
              <span>{isLoadingDemo ? "Generating & Auditing Sample..." : "Load Sample Investigation"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Forensic Audit Capabilities Checklist */}
          <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded p-5">
            <h4 className="text-xs font-mono font-bold uppercase text-[#15202B] mb-3">
              Forensic Audit Capabilities
            </h4>
            <ul className="space-y-2.5 text-xs text-[#263238]">
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#067647] mt-0.5 shrink-0" />
                <span>
                  <strong>Clause Risk Profiling:</strong> Unilateral amendments, penalty interest, liability limitations.
                </span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#067647] mt-0.5 shrink-0" />
                <span>
                  <strong>Counterparty Investigation:</strong> Agentic web verification via TinyFish & public registers.
                </span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#067647] mt-0.5 shrink-0" />
                <span>
                  <strong>Document Integrity:</strong> PDF dictionary metadata analysis & Error Level Analysis (ELA).
                </span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#067647] mt-0.5 shrink-0" />
                <span>
                  <strong>Privacy Exposure & Redaction:</strong> Aadhaar, PAN, phone, banking PII detection & clean scrubbing.
                </span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#067647] mt-0.5 shrink-0" />
                <span>
                  <strong>Contextual Legal Copilot:</strong> Document-grounded Q&A with alternative clause redrafting.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
