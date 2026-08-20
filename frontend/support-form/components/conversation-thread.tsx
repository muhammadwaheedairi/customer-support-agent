"use client";

import { useState, useEffect, useCallback } from "react";
import { MessageBubble } from "./message-bubble";
import { TicketMetadata } from "./ticket-metadata";
import { Loader2, AlertCircle } from "lucide-react";
import { Button } from "./ui/button";
import { useAuth } from "@clerk/nextjs";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Message {
  role: string;
  content: string;
  created_at: string;
  sentiment_score?: number;
}

interface TicketData {
  ticket_id: string;
  status: "open" | "in_progress" | "resolved" | "escalated";
  subject: string;
  category: string;
  created_at: string;
  resolved_at?: string;
  customer_email: string;
  messages: Message[];
}

interface ConversationThreadProps {
  ticketId: string;
}

export function ConversationThread({ ticketId }: ConversationThreadProps) {
  const { getToken } = useAuth();
  const [ticketData, setTicketData] = useState<TicketData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pollingCount, setPollingCount] = useState(0);

  const fetchTicketStatus = useCallback(async (): Promise<boolean> => {
    try {
      const token = await getToken();

      if (!token) {
        setError("Authentication required");
        setLoading(false);
        return true;
      }

      const response = await fetch(`${API_URL}/support/status/${ticketId}`, {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (response.status === 403) {
        setError("You don't have permission to view this conversation");
        setLoading(false);
        return true;
      }

      if (!response.ok) {
        throw new Error("Failed to fetch ticket status");
      }

      const data = await response.json();
      setTicketData(data);
      setLoading(false);

      const hasAgentResponse = data.messages.some(
        (msg: Message) => msg.role === "agent"
      );

      if (hasAgentResponse || pollingCount >= 10) {
        return true;
      }

      return false;
    } catch (err) {
      console.error("Fetch ticket status error:", err);
      setError("Failed to fetch ticket status");
      setLoading(false);
      return true;
    }
  }, [ticketId, pollingCount, getToken]);

  useEffect(() => {
    fetchTicketStatus();

    const pollInterval = setInterval(async () => {
      setPollingCount((prev) => prev + 1);
      const shouldStop = await fetchTicketStatus();
      if (shouldStop) {
        clearInterval(pollInterval);
      }
    }, 3000);

    return () => clearInterval(pollInterval);
  }, [fetchTicketStatus]);

  if (loading && !ticketData) {
    return (
      <div className="flex items-center justify-center py-xl">
        <Loader2 className="h-8 w-8 animate-spin text-muted" />
        <span className="ml-sm body-md text-muted">Loading conversation...</span>
      </div>
    );
  }

  if (error || !ticketData) {
    return (
      <div className="border border-error rounded-lg p-lg bg-red-50 text-center">
        <AlertCircle className="h-12 w-12 text-error mx-auto mb-md" />
        <p className="body-lg text-error mb-md">{error || "Conversation not found"}</p>
        <Button variant="primary" onClick={() => window.location.reload()}>
          Try Again
        </Button>
      </div>
    );
  }

  const hasAgentResponse = ticketData.messages.some((msg) => msg.role === "agent");

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-lg">
      {/* Main Thread */}
      <div className="lg:col-span-2">
        <div className="border border-border rounded-lg bg-neutral overflow-hidden">
          {/* Header */}
          <div className="border-b border-border px-lg py-md">
            <h1 className="headline-sm text-tertiary mb-xs">{ticketData.subject}</h1>
            <p className="body-sm text-muted">Ticket ID: {ticketData.ticket_id}</p>
          </div>

          {/* Processing Indicator */}
          {!hasAgentResponse && (
            <div className="border-b border-border px-lg py-md bg-surface">
              <div className="flex items-center gap-sm">
                <Loader2 className="h-5 w-5 animate-spin text-primary" />
                <span className="body-md text-tertiary">
                  AI assistant is analyzing your request...
                </span>
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="p-lg space-y-md">
            {ticketData.messages.map((message, index) => (
              <MessageBubble
                key={index}
                role={message.role as "agent" | "customer" | "system"}
                content={message.content}
                timestamp={message.created_at}
              />
            ))}
          </div>

          {/* Help Note */}
          {hasAgentResponse && (
            <div className="border-t border-border px-lg py-md bg-surface">
              <p className="body-sm text-muted">
                <strong>Need more help?</strong> Start a new conversation or email us at{" "}
                <a href="mailto:support@lexdesk.io" className="text-tertiary hover:underline">
                  support@lexdesk.io
                </a>
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Metadata Sidebar */}
      <div className="lg:col-span-1">
        <TicketMetadata ticket={ticketData} />
      </div>
    </div>
  );
}