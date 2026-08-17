"use client";

import { useState, useEffect } from "react";
import { CheckCircle2, Clock, Loader2, MessageSquare } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Message {
  role: string;
  content: string;
  created_at: string;
}

interface TicketData {
  ticket_id: string;
  status: string;
  subject: string;
  category: string;
  created_at: string;
  messages: Message[];
}

interface TicketStatusProps {
  ticketId: string;
  onNewTicket: () => void;
}

export function TicketStatus({ ticketId, onNewTicket }: TicketStatusProps) {
  const [ticketData, setTicketData] = useState<TicketData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pollingCount, setPollingCount] = useState(0);

  useEffect(() => {
    const fetchTicketStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/support/status/${ticketId}`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch ticket status");
        }

        const data = await response.json();
        setTicketData(data);
        setLoading(false);

        // Check if we have an agent response
        const hasAgentResponse = data.messages.some(
          (msg: Message) => msg.role === "agent"
        );

        // Stop polling once we have an agent response or after 30 seconds (10 polls)
        if (hasAgentResponse || pollingCount >= 10) {
          return true; // Stop polling
        }

        return false; // Continue polling
      } catch (err) {
        console.error("Fetch ticket status error:", err);
        setError("Failed to fetch ticket status");
        setLoading(false);
        return true; // Stop polling on error
      }
    };

    // Initial fetch
    fetchTicketStatus();

    // Set up polling every 3 seconds
    const pollInterval = setInterval(async () => {
      setPollingCount((prev) => prev + 1);
      const shouldStop = await fetchTicketStatus();
      
      if (shouldStop) {
        clearInterval(pollInterval);
      }
    }, 3000);

    // Cleanup
    return () => clearInterval(pollInterval);
  }, [ticketId, pollingCount]);

  if (loading && !ticketData) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="animate-spin h-8 w-8 text-blue-600" />
          <span className="ml-3 text-gray-600 dark:text-gray-300">
            Loading ticket status...
          </span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
        <div className="text-center py-8">
          <div className="text-red-600 mb-4">Error: {error}</div>
          <button
            onClick={onNewTicket}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Submit Another Request
          </button>
        </div>
      </div>
    );
  }

  if (!ticketData) {
    return null;
  }

  const agentMessages = ticketData.messages.filter((msg) => msg.role === "agent");
  const hasAgentResponse = agentMessages.length > 0;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      {/* Success Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full mb-4">
          <CheckCircle2 className="w-8 h-8 text-green-600 dark:text-green-400" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {hasAgentResponse ? "Response Received!" : "Request Submitted!"}
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          {hasAgentResponse
            ? "Our AI assistant has processed your request."
            : "Our AI assistant is processing your request..."}
        </p>
      </div>

      {/* Ticket Info */}
      <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-500 dark:text-gray-400">Ticket ID</span>
          <span className="font-mono font-bold text-gray-900 dark:text-white">
            {ticketData.ticket_id}
          </span>
        </div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-500 dark:text-gray-400">Subject</span>
          <span className="text-gray-900 dark:text-white">{ticketData.subject}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500 dark:text-gray-400">Status</span>
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300">
            {ticketData.status}
          </span>
        </div>
      </div>

      {/* Processing Indicator */}
      {!hasAgentResponse && (
        <div className="flex items-center justify-center py-4 mb-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <Loader2 className="animate-spin h-5 w-5 text-blue-600 mr-2" />
          <span className="text-blue-700 dark:text-blue-300">
            AI assistant is analyzing your request...
          </span>
        </div>
      )}

      {/* Messages */}
      <div className="space-y-4 mb-6">
        {ticketData.messages.map((message, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg ${
              message.role === "customer"
                ? "bg-gray-100 dark:bg-gray-700"
                : "bg-blue-50 dark:bg-blue-900/20"
            }`}
          >
            <div className="flex items-start mb-2">
              <MessageSquare
                className={`h-5 w-5 mr-2 ${
                  message.role === "customer"
                    ? "text-gray-600 dark:text-gray-400"
                    : "text-blue-600 dark:text-blue-400"
                }`}
              />
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-sm text-gray-900 dark:text-white">
                    {message.role === "customer" ? "You" : "LexDesk AI Assistant"}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {new Date(message.created_at).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Additional Info */}
      {hasAgentResponse && (
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 mb-6">
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
            <strong>Need more help?</strong> You can reply to the email we sent to your address, or visit our{" "}
            <a
              href="https://help.lexdesk.io"
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Help Center
            </a>
            .
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Save your ticket ID for future reference: <strong>{ticketData.ticket_id}</strong>
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={onNewTicket}
          className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Submit Another Request
        </button>
        <button
          onClick={() => window.location.href = "https://help.lexdesk.io"}
          className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors font-medium"
        >
          Visit Help Center
        </button>
      </div>

      {/* Timeout Warning */}
      {!hasAgentResponse && pollingCount >= 8 && (
        <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
          <p className="text-sm text-yellow-800 dark:text-yellow-300">
            <Clock className="inline h-4 w-4 mr-1" />
            Your request is taking longer than usual. We've queued it for processing and will email you the response shortly.
          </p>
        </div>
      )}
    </div>
  );
}
