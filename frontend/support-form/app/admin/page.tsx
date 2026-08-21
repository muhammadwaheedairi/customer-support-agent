"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { Loader2, AlertCircle, Users, Ticket, TrendingUp, Clock, CheckCircle, AlertTriangle, Download } from "lucide-react";
import { clsx } from "clsx";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Stats {
  total_tickets: number;
  open_tickets: number;
  escalated_tickets: number;
  resolved_tickets: number;
  total_customers: number;
  avg_response_seconds: number | null;
  escalation_rate: number;
  resolution_rate: number;
}

interface Ticket {
  ticket_id: string;
  subject: string;
  category: string;
  status: string;
  priority: string;
  created_at: string;
  customer_email: string;
  customer_name: string;
  message_count: number;
  has_agent_response: boolean;
}

export default function AdminPage() {
  const { getToken } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const token = await getToken();

      if (!token) {
        setError("Authentication required");
        return;
      }

      const [statsRes, ticketsRes] = await Promise.all([
        fetch(`${API_URL}/admin/stats`, {
          headers: { "Authorization": `Bearer ${token}` },
        }),
        fetch(`${API_URL}/admin/tickets?limit=50`, {
          headers: { "Authorization": `Bearer ${token}` },
        }),
      ]);

      if (statsRes.status === 403 || ticketsRes.status === 403) {
        setError("Admin access required");
        setLoading(false);
        return;
      }

      const statsData = await statsRes.json();
      const ticketsData = await ticketsRes.json();

      setStats(statsData);
      setTickets(ticketsData.tickets || []);
      setLoading(false);

    } catch (err) {
      console.error("Failed to load admin data:", err);
      setError("Failed to load dashboard");
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      setExporting(true);
      const token = await getToken();
      const response = await fetch(`${API_URL}/admin/export`, {
        headers: { "Authorization": `Bearer ${token}` },
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "lexdesk-tickets.csv";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export failed:", err);
    } finally {
      setExporting(false);
    }
  };

  const filteredTickets = tickets.filter((t) => {
    if (statusFilter === "all") return true;
    return t.status === statusFilter;
  });

  const formatSeconds = (seconds: number | null) => {
    if (!seconds) return "N/A";
    if (seconds < 60) return `${Math.round(seconds)}s`;
    return `${Math.round(seconds / 60)}m`;
  };

  const statusColors: Record<string, string> = {
    open: "bg-blue-100 text-blue-800",
    escalated: "bg-red-100 text-red-800",
    resolved: "bg-green-100 text-green-800",
    in_progress: "bg-yellow-100 text-yellow-800",
  };

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-xl">
          <Loader2 className="h-8 w-8 animate-spin text-muted" />
          <span className="ml-sm body-md text-muted">Loading dashboard...</span>
        </div>
      </AppShell>
    );
  }

  if (error) {
    return (
      <AppShell>
        <div className="flex items-center justify-center py-xl">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-error mx-auto mb-md" />
            <p className="body-lg text-error">{error}</p>
          </div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader
        title="Admin Dashboard"
        description="Monitor all support conversations and metrics"
        action={
          <button
            onClick={handleExport}
            disabled={exporting}
            className="inline-flex items-center gap-sm px-md py-sm bg-primary text-secondary rounded-lg label-md hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {exporting ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Download className="h-4 w-4" />
            )}
            Export CSV
          </button>
        }
      />

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-md mb-xl">
          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <Ticket className="h-5 w-5 text-primary" />
              <span className="label-sm text-muted">Total Tickets</span>
            </div>
            <p className="headline-md text-tertiary">{stats.total_tickets}</p>
          </div>

          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <Clock className="h-5 w-5 text-blue-500" />
              <span className="label-sm text-muted">Open</span>
            </div>
            <p className="headline-md text-tertiary">{stats.open_tickets}</p>
          </div>

          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <AlertTriangle className="h-5 w-5 text-red-500" />
              <span className="label-sm text-muted">Escalated</span>
            </div>
            <p className="headline-md text-tertiary">{stats.escalated_tickets}</p>
            <p className="body-sm text-muted">{stats.escalation_rate}% rate</p>
          </div>

          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span className="label-sm text-muted">Resolved</span>
            </div>
            <p className="headline-md text-tertiary">{stats.resolved_tickets}</p>
            <p className="body-sm text-muted">{stats.resolution_rate}% rate</p>
          </div>

          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <Users className="h-5 w-5 text-primary" />
              <span className="label-sm text-muted">Total Customers</span>
            </div>
            <p className="headline-md text-tertiary">{stats.total_customers}</p>
          </div>

          <div className="border border-border rounded-lg p-md bg-neutral">
            <div className="flex items-center gap-sm mb-sm">
              <TrendingUp className="h-5 w-5 text-primary" />
              <span className="label-sm text-muted">Avg Response</span>
            </div>
            <p className="headline-md text-tertiary">
              {formatSeconds(stats.avg_response_seconds)}
            </p>
          </div>
        </div>
      )}

      {/* Tickets Table */}
      <div>
        <div className="flex items-center gap-xs border-b border-border mb-md">
          {["all", "open", "escalated", "resolved"].map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={clsx(
                "px-md py-sm label-md transition-colors border-b-2 -mb-px capitalize",
                statusFilter === s
                  ? "border-primary text-tertiary"
                  : "border-transparent text-muted hover:text-tertiary"
              )}
            >
              {s}
            </button>
          ))}
        </div>

        <div className="border border-border rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-surface border-b border-border">
              <tr>
                <th className="text-left px-md py-sm label-sm text-muted">Customer</th>
                <th className="text-left px-md py-sm label-sm text-muted">Subject</th>
                <th className="text-left px-md py-sm label-sm text-muted">Category</th>
                <th className="text-left px-md py-sm label-sm text-muted">Status</th>
                <th className="text-left px-md py-sm label-sm text-muted">Created</th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.map((ticket, index) => (
                <tr
                  key={ticket.ticket_id}
                  className={clsx(
                    "border-b border-border hover:bg-surface transition-colors cursor-pointer",
                    index % 2 === 0 ? "bg-neutral" : "bg-surface/50"
                  )}
                  onClick={() => window.open(`/conversations/${ticket.ticket_id}`, "_blank")}
                >
                  <td className="px-md py-sm">
                    <p className="label-sm text-tertiary">{ticket.customer_name || "Unknown"}</p>
                    <p className="body-sm text-muted">{ticket.customer_email}</p>
                  </td>
                  <td className="px-md py-sm">
                    <p className="body-sm text-tertiary line-clamp-1">{ticket.subject}</p>
                  </td>
                  <td className="px-md py-sm">
                    <span className="body-sm text-muted capitalize">{ticket.category}</span>
                  </td>
                  <td className="px-md py-sm">
                    <span className={clsx(
                      "px-sm py-xs rounded-full text-xs font-medium capitalize",
                      statusColors[ticket.status] || "bg-gray-100 text-gray-700"
                    )}>
                      {ticket.status}
                    </span>
                  </td>
                  <td className="px-md py-sm">
                    <p className="body-sm text-muted">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredTickets.length === 0 && (
            <div className="text-center py-xl">
              <p className="body-md text-muted">No {statusFilter} tickets found</p>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}