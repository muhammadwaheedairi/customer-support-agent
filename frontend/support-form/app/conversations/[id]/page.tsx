"use client";

import { useParams, useRouter } from "next/navigation";
import { AppShell } from "@/components/app-shell";
import { ConversationThread } from "@/components/conversation-thread";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

export default function ConversationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const ticketId = params.id as string;

  return (
    <AppShell>
      <div className="mb-md">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => router.push("/conversations")}
          className="text-muted hover:text-tertiary"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Conversations
        </Button>
      </div>

      <ConversationThread ticketId={ticketId} />
    </AppShell>
  );
}
