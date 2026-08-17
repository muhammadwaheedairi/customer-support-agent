"use client";

import { useState, useEffect } from "react";
import { ConversationRow } from "./conversation-row";
import { EmptyState } from "./empty-state";
import { MessageSquare, Loader2 } from "lucide-react";
import { Button } from "./ui/button";
import { clsx } from "clsx";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Message {
  role: string;
  content: string;
  created_at: string;
}

interface TicketData {
  ticket_id: string;
  status: "open" | "in_progress" | "resolved" | "escalated";
  subject: string;
  category: string;
  created_at: string;
  messages: Message[];
}

interface ConversationsListProps {
  onNewConversation: () => void;
}

export function ConversationsList({ onNewConversation }: ConversationsListProps) {
  const [tickets, setTickets] = useState<TicketData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | "open" | "resolved" | "escalated">("all");

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      // Get ticket IDs from localStorage
      const storedTicketIds = localStorage.getItem("lexdesk_ticket_ids");

      if (!storedTicketIds) {
        setLoading(false);
        return;
      }

      const ticketIds: string[] = JSON.parse(storedTicketIds);

      // Fetch each ticket
      const ticketPromises = ticketIds.map(async (ticketId) => {
        try {
          const response = await fetch(`${API_URL}/support/status/${ticketId}`);
          if (response.ok) {
            return await response.json();
          }
          return null;
        } catch (err) {
          console.error(`Failed to fetch ticket ${ticketId}:`, err);
          return null;
        }
      });

      const ticketResults = await Promise.all(ticketPromises);
      const validTickets = ticketResults.filter((t): t is TicketData => t !== null);

      // Sort by created date, newest first
      validTickets.sort((a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );

      setTickets(validTickets);
      setLoading(false);
    } catch (err) {
      console.error("Failed to load tickets:", err);
      setError("Failed to load conversations");
      setLoading(false);
    }
  };

  const filteredTickets = tickets.filter((ticket) => {
    if (filter === "all") return true;
    return ticket.status === filter;
  });

  const filterOptions = [
    { value: "all", label: "All" },
    { value: "open", label: "Open" },
    { value: "resolved", label: "Resolved" },
    { value: "escalated", label: "Escalated" },
  ] as const;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-xl">
        <Loader2 className="h-8 w-8 animate-spin text-muted" />
      </div>
    );
  }

  if (error) {
    return (
      <EmptyState
        icon={<MessageSquare className="h-12 w-12" />}
        title="Failed to load conversations"
        description={error}
        action={
          <Button onClick={loadTickets} variant="primary">
            Try Again
          </Button>
        }
      />
    );
  }

  if (tickets.length === 0) {
    return (
      <EmptyState
        icon={<MessageSquare className="h-12 w-12" />}
        title="No conversations yet"
        description="Start a conversation to get help from our AI support team."
        action={
          <Button onClick={onNewConversation} variant="primary">
            Start Conversation
          </Button>
        }
      />
    );
  }

  return (
    <div>
      {/* Filter Tabs */}
      <div className="flex items-center gap-xs border-b border-border mb-md">
        {filterOptions.map((option) => (
          <button
            key={option.value}
            onClick={() => setFilter(option.value)}
            className={clsx(
              "px-md py-sm label-md transition-colors border-b-2 -mb-px",
              filter === option.value
                ? "border-primary text-tertiary"
                : "border-transparent text-muted hover:text-tertiary"
            )}
          >
            {option.label}
          </button>
        ))}
      </div>

      {/* Conversations List */}
      {filteredTickets.length === 0 ? (
        <EmptyState
          icon={<MessageSquare className="h-12 w-12" />}
          title={`No ${filter} conversations`}
          description={`You don't have any ${filter === "all" ? "" : filter} conversations yet.`}
        />
      ) : (
        <div className="border border-border rounded-lg overflow-hidden bg-neutral">
          {filteredTickets.map((ticket) => {
            const lastMessage = ticket.messages[ticket.messages.length - 1];
            const hasAgentResponse = ticket.messages.some(m => m.role === "agent");

            return (
              <ConversationRow
                key={ticket.ticket_id}
                ticketId={ticket.ticket_id}
                subject={ticket.subject}
                status={ticket.status}
                category={ticket.category}
                lastMessagePreview={lastMessage?.content}
                createdAt={ticket.created_at}
                hasUnread={!hasAgentResponse}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}
