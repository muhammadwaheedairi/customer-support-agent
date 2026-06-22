"use client";

import { useState } from "react";
import { SupportForm } from "@/components/support-form";
import { TicketStatus } from "@/components/ticket-status";

export default function Home() {
  const [ticketId, setTicketId] = useState<string | null>(null);

  const handleSubmitSuccess = (id: string) => {
    setTicketId(id);
  };

  const handleNewTicket = () => {
    setTicketId(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              TaskFlow Support
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Get help from our AI-powered support team, available 24/7
            </p>
          </div>

          {/* Main Content */}
          {!ticketId ? (
            <SupportForm onSuccess={handleSubmitSuccess} />
          ) : (
            <TicketStatus ticketId={ticketId} onNewTicket={handleNewTicket} />
          )}

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
            <p>
              Need immediate help?{" "}
              <a
                href="https://help.taskflow.com"
                className="text-blue-600 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Visit our Help Center
              </a>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
