"use client";

import { useState, useEffect } from "react";
import { ConversationRow } from "./conversation-row";
import { EmptyState } from "./empty-state";
import { MessageSquare, Loader2 } from "lucide-react";
import { Button } from "./ui/button";
import { useAuth } from "@clerk/nextjs";
import { clsx } from "clsx";
import { toast } from "sonner";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface TicketData {
  ticket_id: string;
  status: "open" | "in_progress" | "resolved" | "escalated";
  subject: string;
  category: string;
  created_at: string;
  message_count: number;
  has_agent_response: boolean;
}

interface ConversationsListProps {
  onNewConversation: () => void;
}

export function ConversationsList({ onNewConversation }: ConversationsListProps) {
  const { getToken } = useAuth();
  const [tickets, setTickets] = useState<TicketData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | "open" | "resolved" | "escalated">("all");

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      setLoading(true);
      setError(null);

      // Clerk JWT token lo
      const token = await getToken();

      if (!token) {
        setError("Authentication required");
        setLoading(false);
        return;
      }

      // Backend se sirf apne tickets fetch karo
      const response = await fetch(`${API_URL}/tickets/my`, {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to load conversations");
      }

      const data = await response.json();
      setTickets(data.tickets || []);
      setLoading(false);

    } catch (err) {
      console.error("Failed to load tickets:", err);
      setError("Failed to load conversations");
      setLoading(false);
    }
  };

  const handleDelete = async (ticketId: string) => {
    if (!confirm("Are you sure you want to delete this conversation?")) return;

    try {
      const token = await getToken();
      const response = await fetch(`${API_URL}/tickets/${ticketId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTickets((prev) => prev.filter((t) => t.ticket_id !== ticketId));
        toast.success("Conversation deleted successfully.");
      } else {
        toast.error("Failed to delete conversation.");
      }
    } catch (err) {
      console.error("Failed to delete ticket:", err);
      toast.error("Something went wrong. Please try again.");
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
      <div className="flex items-center gap-xs border-b border-border mb-md overflow-x-auto scrollbar-hide">
        {filterOptions.map((option) => (
          <button
            key={option.value}
            onClick={() => setFilter(option.value)}
            className={clsx(
              "px-sm sm:px-md py-sm label-md transition-colors border-b-2 -mb-px whitespace-nowrap flex-shrink-0",
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
          {filteredTickets.map((ticket) => (
            <ConversationRow
              key={ticket.ticket_id}
              ticketId={ticket.ticket_id}
              subject={ticket.subject}
              status={ticket.status}
              category={ticket.category}
              createdAt={ticket.created_at}
              hasUnread={!ticket.has_agent_response}
              onDelete={() => handleDelete(ticket.ticket_id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}