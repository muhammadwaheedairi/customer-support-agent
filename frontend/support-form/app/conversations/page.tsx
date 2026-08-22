"use client";

import { useState } from "react";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { ConversationsList } from "@/components/conversations-list";
import { NewConversationModal } from "@/components/new-conversation-modal";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function ConversationsPage() {
  const [showNewConversation, setShowNewConversation] = useState(false);

  const handleNewConversation = () => {
    setShowNewConversation(true);
  };

  const handleConversationCreated = () => {
    setShowNewConversation(false);
    // Refresh the list
    window.location.reload();
  };

  return (
    <AppShell>
      <PageHeader
        title="Conversations"
        description="View and manage your support conversations"
        action={
          <Button variant="primary" size="default" onClick={handleNewConversation}>
            <Plus className="h-5 w-5 sm:mr-2" />
            <span className="hidden sm:inline">New Conversation</span>
            <span className="inline sm:hidden">New</span>
          </Button>
        }
      />

      <ConversationsList onNewConversation={handleNewConversation} />

      {showNewConversation && (
        <NewConversationModal
          onClose={() => setShowNewConversation(false)}
          onSuccess={handleConversationCreated}
        />
      )}
    </AppShell>
  );
}