"use client";

import { StatusBadge } from "./ui/status-badge";
import { Badge } from "./ui/badge";
import { format } from "date-fns";
import { Calendar, Tag, Mail } from "lucide-react";

interface TicketData {
  ticket_id: string;
  status: "open" | "in_progress" | "resolved" | "escalated";
  subject: string;
  category: string;
  created_at: string;
  resolved_at?: string;
  customer_email: string;
}

interface TicketMetadataProps {
  ticket: TicketData;
}

export function TicketMetadata({ ticket }: TicketMetadataProps) {
  return (
    <div className="border border-border rounded-lg bg-neutral overflow-hidden sticky top-gutter">
      {/* Header */}
      <div className="border-b border-border px-md py-sm bg-surface">
        <h3 className="label-md text-tertiary">Ticket Details</h3>
      </div>

      {/* Content */}
      <div className="p-md space-y-md">
        {/* Status */}
        <div>
          <p className="label-sm text-muted mb-xs">Status</p>
          <StatusBadge status={ticket.status} />
        </div>

        {/* Category */}
        <div>
          <p className="label-sm text-muted mb-xs flex items-center gap-xs">
            <Tag className="h-4 w-4" />
            Category
          </p>
          <Badge variant="default" className="capitalize">
            {ticket.category.replace("_", " ")}
          </Badge>
        </div>

        {/* Created */}
        <div>
          <p className="label-sm text-muted mb-xs flex items-center gap-xs">
            <Calendar className="h-4 w-4" />
            Created
          </p>
          <p className="body-sm text-tertiary">
            {format(new Date(ticket.created_at), "MMM d, yyyy 'at' h:mm a")}
          </p>
        </div>

        {/* Resolved (if applicable) */}
        {ticket.resolved_at && (
          <div>
            <p className="label-sm text-muted mb-xs flex items-center gap-xs">
              <Calendar className="h-4 w-4" />
              Resolved
            </p>
            <p className="body-sm text-tertiary">
              {format(new Date(ticket.resolved_at), "MMM d, yyyy 'at' h:mm a")}
            </p>
          </div>
        )}

        {/* Customer Email */}
        <div>
          <p className="label-sm text-muted mb-xs flex items-center gap-xs">
            <Mail className="h-4 w-4" />
            Your Email
          </p>
          <p className="body-sm text-tertiary break-all">{ticket.customer_email}</p>
        </div>

        {/* Ticket ID */}
        <div>
          <p className="label-sm text-muted mb-xs">Reference Number</p>
          <code className="body-sm text-tertiary bg-surface px-sm py-xs rounded border border-border block break-all">
            {ticket.ticket_id}
          </code>
        </div>
      </div>

      {/* Footer Note */}
      <div className="border-t border-border px-md py-sm bg-surface">
        <p className="body-sm text-muted">
          Save your reference number for future inquiries.
        </p>
      </div>
    </div>
  );
}
