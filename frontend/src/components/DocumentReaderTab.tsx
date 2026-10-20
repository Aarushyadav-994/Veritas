"use client";

import React, { useState } from "react";
import { Search, ChevronLeft, ChevronRight, FileText, Image as ImageIcon } from "lucide-react";

interface PageData {
  page_number: number;
  text: string;
  character_count: number;
  word_count: number;
  has_images: boolean;
  preview_image?: string;
}

interface DocumentReaderTabProps {
  pages: PageData[];
  fullText: string;
}

export const DocumentReaderTab: React.FC<DocumentReaderTabProps> = ({
  pages,
  fullText,
}) => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [viewMode, setViewMode] = useState<"text" | "rendered">("text");

  const totalPages = pages.length || 1;
  const activePageData = pages.find((p) => p.page_number === currentPage) || pages[0];

  return (
    <div className="bg-[#FFFFFF] border border-[#D0D5DD] rounded shadow-xs overflow-hidden">
      {/* Reader Toolbar */}
      <div className="p-4 bg-[#FAFAF8] border-b border-[#EFECE4] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        {/* Pagination Controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage <= 1}
            className="p-1.5 rounded border border-[#D0D5DD] hover:bg-[#FFFFFF] disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>

          <span className="font-mono text-[#263238]">
            Page <strong>{currentPage}</strong> of <strong>{totalPages}</strong>
          </span>

          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages}
            className="p-1.5 rounded border border-[#D0D5DD] hover:bg-[#FFFFFF] disabled:opacity-40 cursor-pointer"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </button>

          {activePageData && (
            <span className="text-[11px] text-[#667085] ml-2 hidden sm:inline">
              ({activePageData.word_count} words | {activePageData.character_count} chars)
            </span>
          )}
        </div>

        {/* View Mode & Search */}
        <div className="flex items-center space-x-3">
          {activePageData?.preview_image && (
            <div className="flex items-center space-x-1 bg-[#F5F3ED] p-1 rounded border border-[#D0D5DD]">
              <button
                onClick={() => setViewMode("text")}
                className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                  viewMode === "text" ? "bg-[#15202B] text-[#FFFFFF]" : "text-[#667085]"
                }`}
              >
                Text Stream
              </button>
              <button
                onClick={() => setViewMode("rendered")}
                className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                  viewMode === "rendered" ? "bg-[#15202B] text-[#FFFFFF]" : "text-[#667085]"
                }`}
              >
                Visual Render
              </button>
            </div>
          )}

          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-[#98A2B3]" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Filter page text..."
              className="pl-8 pr-3 py-1.5 text-xs border border-[#D0D5DD] rounded bg-[#FFFFFF] focus:outline-none focus:border-[#15202B] w-40 sm:w-48"
            />
          </div>
        </div>
      </div>

      {/* Reader Content Body */}
      <div className="p-6 min-h-[450px] max-h-[650px] overflow-y-auto">
        {viewMode === "rendered" && activePageData?.preview_image ? (
          <div className="flex justify-center bg-[#FAFAF8] p-4 rounded border border-[#EFECE4]">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={activePageData.preview_image}
              alt={`Page ${currentPage} rendering`}
              className="max-w-full h-auto shadow-sm rounded border border-[#D0D5DD]"
            />
          </div>
        ) : (
          <div className="font-serif text-sm text-[#15202B] leading-relaxed whitespace-pre-wrap select-text max-w-3xl mx-auto">
            {activePageData?.text || "No text content detected on this page."}
          </div>
        )}
      </div>
    </div>
  );
};
