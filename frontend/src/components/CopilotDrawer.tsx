"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Sparkles, HelpCircle, X, ChevronRight, MessageSquare } from "lucide-react";

interface Message {
  sender: "user" | "assistant";
  text: string;
  cited_clauses?: string[];
  engine?: string;
}

interface CopilotDrawerProps {
  sessionId: string;
  isOpen: boolean;
  onClose: () => void;
  documentTitle?: string;
}

export const CopilotDrawer: React.FC<CopilotDrawerProps> = ({
  sessionId,
  isOpen,
  onClose,
  documentTitle,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "assistant",
      text: "I am your Veritas Contextual Legal Copilot. I have indexed your contract clauses, obligations, and risk parameters. Ask any question regarding financial penalties, termination conditions, liability caps, or omitted protections.",
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isSending, setIsSending] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const quickPrompts = [
    "How can I terminate this agreement?",
    "What are my main financial penalties?",
    "Is this contract automatically renewed?",
    "Which clauses are potentially unfavorable?",
    "What protections might be missing?",
  ];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (questionToSend?: string) => {
    const q = questionToSend || inputText;
    if (!q.trim() || isSending) return;

    setInputText("");
    setMessages((prev) => [...prev, { sender: "user", text: q }]);
    setIsSending(true);

    try {
      const res = await fetch("http://localhost:8000/api/copilot/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          question: q,
        }),
      });

      if (!res.ok) {
        throw new Error("Copilot response failure");
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: data.answer,
          cited_clauses: data.cited_clauses,
          engine: data.engine,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: "Unable to retrieve answer at this time. Please verify backend connection.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-96 md:w-[450px] bg-[#FFFFFF] border-l border-[#D0D5DD] shadow-xl z-50 flex flex-col">
      {/* Drawer Header */}
      <div className="p-4 bg-[#15202B] text-[#FFFFFF] border-b border-[#263238] flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-7 h-7 rounded bg-[#263238] border border-[#AD925B] flex items-center justify-center">
            <span className="text-[#AD925B] font-serif font-bold text-sm">V</span>
          </div>
          <div>
            <h3 className="font-serif font-bold text-sm text-[#FFFFFF]">Legal Context Copilot</h3>
            <p className="text-[10px] text-[#AD925B] font-mono">
              Document-Grounded Retrieval & Clause Citations
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="text-[#D0D5DD] hover:text-[#FFFFFF] p-1 rounded hover:bg-[#263238] cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Quick Prompts Carousel */}
      <div className="p-3 bg-[#FAFAF8] border-b border-[#EFECE4] overflow-x-auto whitespace-nowrap space-x-2 text-xs flex">
        {quickPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            disabled={isSending}
            className="px-2.5 py-1 rounded bg-[#FFFFFF] text-[#263238] border border-[#D0D5DD] hover:border-[#AD925B] hover:text-[#AD925B] text-[11px] transition-colors cursor-pointer shrink-0 disabled:opacity-50"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Messages Stream */}
      <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto space-y-4 text-xs bg-[#F5F3ED]">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${
              m.sender === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`max-w-[88%] p-3.5 rounded ${
                m.sender === "user"
                  ? "bg-[#15202B] text-[#FFFFFF] rounded-br-none"
                  : "bg-[#FFFFFF] text-[#15202B] border border-[#D0D5DD] rounded-bl-none shadow-xs"
              }`}
            >
              <div className="whitespace-pre-wrap leading-relaxed font-sans">{m.text}</div>

              {m.cited_clauses && m.cited_clauses.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-[#EFECE4] flex flex-wrap gap-1 items-center">
                  <span className="text-[10px] font-mono text-[#667085] uppercase">Cited:</span>
                  {m.cited_clauses.map((c, cIdx) => (
                    <span
                      key={cIdx}
                      className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#F5F3ED] text-[#AD925B] border border-[#EFECE4]"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              )}

              {m.engine && (
                <div className="mt-1 text-[9px] font-mono text-[#98A2B3] text-right">
                  {m.engine}
                </div>
              )}
            </div>
          </div>
        ))}

        {isSending && (
          <div className="flex items-center space-x-2 text-xs text-[#667085] bg-[#FFFFFF] p-3 rounded border border-[#D0D5DD] max-w-[70%]">
            <div className="w-2 h-2 rounded-full bg-[#AD925B] animate-ping" />
            <span>Auditing contract context & citing provisions...</span>
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="p-3 bg-[#FFFFFF] border-t border-[#D0D5DD]">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center space-x-2"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask question about this contract..."
            className="flex-1 px-3 py-2 text-xs border border-[#D0D5DD] rounded bg-[#FAFAF8] focus:bg-[#FFFFFF] focus:outline-none focus:border-[#15202B]"
          />
          <button
            type="submit"
            disabled={!inputText.trim() || isSending}
            className="p-2 rounded bg-[#15202B] hover:bg-[#263238] text-[#FFFFFF] disabled:opacity-40 transition-colors cursor-pointer"
          >
            <Send className="w-3.5 h-3.5 text-[#AD925B]" />
          </button>
        </form>
        <p className="text-[10px] text-[#98A2B3] text-center mt-2">
          Strictly grounded in extracted text. Does not substitute for formal legal counsel.
        </p>
      </div>
    </div>
  );
};
