"use client";

import Link from "next/link";
import { StatusBadge } from "@/components/ui/status-badge";
import { formatDistanceToNow } from "date-fns";
import { Trash2 } from "lucide-react";
import { clsx } from "clsx";

interface ConversationRowProps {
  ticketId: string;
  subject: string;
  status: "open" | "in_progress" | "resolved" | "escalated";
  category: string;
  lastMessagePreview?: string;
  createdAt: string;
  hasUnread?: boolean;
  onDelete?: () => void;
}

export function ConversationRow({
  ticketId,
  subject,
  status,
  category,
  lastMessagePreview,
  createdAt,
  hasUnread = false,
  onDelete,
}: ConversationRowProps) {
  const timeAgo = formatDistanceToNow(new Date(createdAt), { addSuffix: true });

  return (
    <div
      className={clsx(
        "flex items-center border-b border-border hover:bg-surface transition-colors group",
        hasUnread && "bg-surface/50"
      )}
    >
      {/* Main link area */}
      <Link
        href={`/conversations/${ticketId}`}
        className="flex-1 block p-md min-w-0"
      >
        <div className="flex items-start justify-between gap-md">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-sm mb-xs">
              <h3 className="label-md text-tertiary truncate">{subject}</h3>
              {hasUnread && (
                <div className="h-2 w-2 rounded-full bg-primary flex-shrink-0" />
              )}
            </div>

            {lastMessagePreview && (
              <p className="body-sm text-muted line-clamp-2 mb-xs">
                {lastMessagePreview}
              </p>
            )}

            <div className="flex items-center gap-sm text-muted">
              <span className="body-sm capitalize">{category}</span>
              <span className="body-sm">•</span>
              <span className="body-sm">{timeAgo}</span>
            </div>
          </div>

          <div className="flex-shrink-0">
            <StatusBadge status={status} />
          </div>
        </div>
      </Link>

      {/* Delete button */}
      {onDelete && (
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onDelete();
          }}
          className="p-md text-muted hover:text-error opacity-0 group-hover:opacity-100 transition-all flex-shrink-0"
          aria-label="Delete conversation"
          title="Delete conversation"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}