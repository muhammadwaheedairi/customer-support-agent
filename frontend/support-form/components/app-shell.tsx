"use client";

import { TopNav } from "./top-nav";

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-neutral">
      <TopNav />
      <main className="mx-auto max-w-7xl px-gutter py-lg">{children}</main>
    </div>
  );
}
