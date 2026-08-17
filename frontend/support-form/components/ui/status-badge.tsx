"use client";

import { Badge } from "@/components/ui/badge";
import { clsx } from "clsx";

interface StatusBadgeProps {
  status: "open" | "in_progress" | "resolved" | "escalated";
  className?: string;
}

const statusConfig = {
  open: {
    label: "Open",
    variant: "primary" as const,
  },
  in_progress: {
    label: "In Progress",
    variant: "warning" as const,
  },
  resolved: {
    label: "Resolved",
    variant: "success" as const,
  },
  escalated: {
    label: "Escalated",
    variant: "error" as const,
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = statusConfig[status] || statusConfig.open;

  return (
    <Badge variant={config.variant} className={clsx("label-sm", className)}>
      {config.label}
    </Badge>
  );
}
