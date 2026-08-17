"use client";

import { formatDistanceToNow } from "date-fns";
import { User, Bot } from "lucide-react";
import { clsx } from "clsx";

interface MessageBubbleProps {
  role: "customer" | "agent" | "system";
  content: string;
  timestamp: string;
}

export function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const timeAgo = formatDistanceToNow(new Date(timestamp), { addSuffix: true });

  if (role === "system") {
    return (
      <div className="flex justify-center">
        <div className="bg-surface rounded-lg px-md py-sm max-w-md">
          <p className="body-sm text-muted text-center">{content}</p>
        </div>
      </div>
    );
  }

  const isAgent = role === "agent";

  return (
    <div
      className={clsx(
        "flex gap-sm",
        isAgent ? "items-start" : "items-start"
      )}
    >
      {/* Avatar */}
      <div
        className={clsx(
          "flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center",
          isAgent ? "bg-primary" : "bg-surface border border-border"
        )}
      >
        {isAgent ? (
          <Bot className="h-5 w-5 text-secondary" />
        ) : (
          <User className="h-5 w-5 text-muted" />
        )}
      </div>

      {/* Message Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-sm mb-xs">
          <span className="label-md text-tertiary">
            {isAgent ? "LexDesk AI Assistant" : "You"}
          </span>
          <span className="body-sm text-muted">{timeAgo}</span>
        </div>

        <div
          className={clsx(
            "rounded-lg px-md py-sm",
            isAgent
              ? "bg-neutral border-l-4 border-primary"
              : "bg-surface"
          )}
        >
          <p className="body-md text-tertiary whitespace-pre-wrap">{content}</p>
        </div>
      </div>
    </div>
  );
}
