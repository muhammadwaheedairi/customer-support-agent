"use client";

import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";

export default function HelpCenterPage() {
  return (
    <AppShell>
      <PageHeader
        title="Help Center"
        description="Browse our knowledge base and find answers"
      />

      {/* Placeholder - Phase 5 implementation */}
      <div className="border border-border rounded-lg p-lg bg-neutral">
        <div className="text-center py-xl">
          <p className="body-lg text-muted">
            Knowledge base browser will appear here.
          </p>
          <p className="body-sm text-muted mt-sm">
            Phase 5 implementation (requires backend API).
          </p>
        </div>
      </div>
    </AppShell>
  );
}
