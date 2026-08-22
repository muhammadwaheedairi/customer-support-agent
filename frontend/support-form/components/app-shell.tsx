"use client";

import { TopNav } from "./top-nav";

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-neutral">
      <TopNav />
      <main className="mx-auto max-w-7xl px-4 sm:px-gutter py-md sm:py-lg">{children}</main>
    </div>
  );
}