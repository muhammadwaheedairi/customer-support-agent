"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";
import { clsx } from "clsx";

// This component is deprecated - kept for reference only
// Use NewConversationModal instead

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const CATEGORIES = [
  { value: "general", label: "General Question" },
  { value: "technical", label: "Technical Support" },
  { value: "billing", label: "Billing Inquiry" },
  { value: "bug_report", label: "Bug Report" },
  { value: "feedback", label: "Feedback" },
];

const PRIORITIES = [
  { value: "low", label: "Low - Not urgent" },
  { value: "medium", label: "Medium - Need help soon" },
  { value: "high", label: "High - Urgent issue" },
];

interface SupportFormProps {
  onSuccess: (ticketId: string) => void;
}

export function SupportForm({ onSuccess }: SupportFormProps) {
  const router = useRouter();

  const handleSubmit = (ticketId: string) => {
    // Redirect to conversation detail
    router.push(`/conversations/${ticketId}`);
  };

  return (
    <div className="border border-border rounded-lg bg-neutral p-lg max-w-2xl mx-auto">
      <p className="body-md text-muted text-center">
        This form has been replaced by the new conversation modal.
      </p>
      <p className="body-sm text-muted text-center mt-sm">
        Please use the "New Conversation" button from the conversations page.
      </p>
    </div>
  );
}
