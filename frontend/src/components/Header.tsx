"use client";

import React from "react";
import { Shield, FileText, Download, RotateCcw, AlertTriangle, ExternalLink, Sparkles } from "lucide-react";

interface HeaderProps {
  hasDocument: boolean;
  filename?: string;
  isDemo?: boolean;
  onReset: () => void;
  onExport: () => void;
  onLoadDemo: () => void;
  isLoadingDemo?: boolean;
  engineName?: string;
  tinyfishStatus?: string;
}

export const Header: React.FC<HeaderProps> = ({
  hasDocument,
  filename,
  isDemo,
  onReset,
  onExport,
  onLoadDemo,
  isLoadingDemo,
  engineName,
  tinyfishStatus,
}) => {
  return (
    <header className="border-b border-[#D0D5DD] bg-[#FFFFFF] sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand & Tagline */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded bg-[#15202B] border border-[#AD925B] flex items-center justify-center shadow-xs">
              <span className="text-[#AD925B] font-serif font-bold text-lg">V</span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-serif font-bold tracking-tight text-lg text-[#15202B]">
                  VERITAS AI
                </span>
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[#F5F3ED] text-[#263238] border border-[#D0D5DD]">
                  Kritical Hacks 2026
                </span>
              </div>
              <p className="text-xs text-[#667085] hidden sm:block">
                Don&apos;t Just Read the Contract. Investigate It.
              </p>
            </div>
          </div>

          {/* Center Info / Active Document Title */}
          {hasDocument && (
            <div className="hidden md:flex items-center space-x-2 text-xs text-[#263238] bg-[#F5F3ED] px-3 py-1.5 rounded border border-[#D0D5DD]">
              <FileText className="w-3.5 h-3.5 text-[#AD925B]" />
              <span className="font-medium truncate max-w-xs">{filename}</span>
              {isDemo && (
                <span className="px-1.5 py-0.2 text-[10px] bg-[#E8E1D3] text-[#785E2F] font-mono rounded">
                  DEMO FIXTURE
                </span>
              )}
            </div>
          )}

          {/* Right Action Controls */}
          <div className="flex items-center space-x-2.5">
            {!hasDocument ? (
              <button
                onClick={onLoadDemo}
                disabled={isLoadingDemo}
                className="inline-flex items-center space-x-1.5 text-xs font-medium px-3.5 py-1.5 rounded bg-[#15202B] text-[#FFFFFF] hover:bg-[#263238] transition-colors border border-[#15202B] disabled:opacity-50 cursor-pointer"
              >
                <span>{isLoadingDemo ? "Loading Sample..." : "Load Sample Contract"}</span>
              </button>
            ) : (
              <>
                <button
                  onClick={onExport}
                  className="inline-flex items-center space-x-1.5 text-xs font-medium px-3 py-1.5 rounded bg-[#15202B] text-[#FFFFFF] hover:bg-[#263238] transition-colors border border-[#15202B] cursor-pointer"
                  title="Download unified PDF legal intelligence dossier"
                >
                  <Download className="w-3.5 h-3.5 text-[#AD925B]" />
                  <span className="hidden sm:inline">Export PDF Dossier</span>
                  <span className="sm:hidden">Export</span>
                </button>

                <button
                  onClick={onReset}
                  className="inline-flex items-center space-x-1 text-xs font-medium px-2.5 py-1.5 rounded bg-[#FFFFFF] text-[#B42318] hover:bg-[#FEF3F2] border border-[#FDA29B] transition-colors cursor-pointer"
                  title="Purge session state from active server memory"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Clear Session</span>
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
