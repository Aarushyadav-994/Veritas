import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Veritas AI — Legal Document Intelligence & Investigation Platform",
  description: "Don't Just Read the Contract. Investigate It. Forensic legal contract analysis, document integrity checks, privacy auditing, and counterparty investigation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#F5F3ED] text-[#15202B]">
        {children}
      </body>
    </html>
  );
}
