"use client";

import { MessageSquare } from "lucide-react";

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  action?: React.ReactNode;
}

export function EmptyState({
  icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-lg sm:py-xl px-4 sm:px-gutter text-center">
      {icon && (
        <div className="mb-md text-muted">
          {icon}
        </div>
      )}
      <h3 className="headline-sm text-tertiary mb-xs">{title}</h3>
      <p className="body-md text-muted mb-lg max-w-md">{description}</p>
      {action && <div className="w-full sm:w-auto">{action}</div>}
    </div>
  );
}