"use client";

import Link from "next/link";

export function ProductPreview() {
  return (
    <section className="py-[80px] lg:py-[120px] bg-surface">
      <div className="mx-auto max-w-7xl px-gutter">
        {/* Section Header - Minimal */}
        <div className="text-center mb-xl max-w-3xl mx-auto">
          <h2 className="headline-lg text-tertiary mb-sm">
            Professional Support Interface
          </h2>
          <p className="body-lg text-muted">
            Production-ready workspace with AI-powered conversations, ticket management,
            and human escalation.
          </p>
        </div>

        {/* Large Product Screenshot */}
        <div className="relative">
          {/* Browser Chrome */}
          <div className="rounded-t-xl border border-border bg-neutral overflow-hidden shadow-2xl">
            {/* Browser Header */}
            <div className="border-b border-border bg-surface px-md py-sm flex items-center gap-2">
              <div className="flex items-center gap-xs">
                <div className="h-3 w-3 rounded-full bg-red-400" />
                <div className="h-3 w-3 rounded-full bg-yellow-400" />
                <div className="h-3 w-3 rounded-full bg-green-400" />
              </div>
              <div className="flex-1 text-center">
                <div className="inline-flex items-center gap-xs px-md py-xs bg-neutral border border-border rounded body-sm text-muted">
                  <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 0a1 1 0 0 1 1 1v5.268l4.562-2.634a1 1 0 1 1 1 1.732L10 8l4.562 2.634a1 1 0 1 1-1 1.732L9 9.732V15a1 1 0 1 1-2 0V9.732l-4.562 2.634a1 1 0 1 1-1-1.732L6 8 1.438 5.366a1 1 0 0 1 1-1.732L7 6.268V1a1 1 0 0 1 1-1z"/>
                  </svg>
                  <span>localhost:3000/conversations</span>
                </div>
              </div>
            </div>

            {/* Actual Product UI */}
            <div className="bg-neutral">
              {/* Mini Navigation */}
              <div className="border-b border-border px-lg py-sm flex items-center justify-between">
                <span className="headline-sm text-tertiary">LexDesk</span>
                <div className="flex items-center gap-xs">
                  <span className="body-sm text-tertiary">Conversations</span>
                  <span className="body-sm text-muted">Help Center</span>
                </div>
              </div>

              {/* Conversations Content */}
              <div className="p-lg">
                <div className="flex items-center justify-between mb-md">
                  <div>
                    <h3 className="headline-md text-tertiary">Conversations</h3>
                    <p className="body-sm text-muted">Manage support tickets</p>
                  </div>
                  <div className="inline-flex items-center gap-xs px-md py-xs bg-primary text-secondary rounded-lg label-md">
                    <span>+ New Conversation</span>
                  </div>
                </div>

                {/* Filter Tabs */}
                <div className="flex items-center gap-md border-b border-border mb-md">
                  <div className="px-md py-sm border-b-2 border-primary label-md text-tertiary">All</div>
                  <div className="px-md py-sm border-b-2 border-transparent label-md text-muted">Open</div>
                  <div className="px-md py-sm border-b-2 border-transparent label-md text-muted">Resolved</div>
                </div>

                {/* Ticket List */}
                <div className="space-y-sm">
                  {/* Ticket 1 */}
                  <div className="border border-border rounded-lg p-md hover:border-primary transition-colors bg-surface/50">
                    <div className="flex items-start justify-between mb-xs">
                      <div className="flex items-center gap-xs">
                        <div className="h-2 w-2 rounded-full bg-primary" />
                        <span className="label-md text-tertiary">How do I set up client intake forms?</span>
                      </div>
                      <div className="px-2 py-0.5 bg-primary text-secondary rounded-full text-xs font-medium">Open</div>
                    </div>
                    <p className="body-sm text-muted mb-xs">I need help configuring intake forms for family law...</p>
                    <p className="body-sm text-muted">Technical • 2 hours ago</p>
                  </div>

                  {/* Ticket 2 */}
                  <div className="border border-border rounded-lg p-md">
                    <div className="flex items-start justify-between mb-xs">
                      <span className="label-md text-tertiary">Password reset issue resolved</span>
                      <div className="px-2 py-0.5 bg-green-100 text-green-800 rounded-full text-xs font-medium">Resolved</div>
                    </div>
                    <p className="body-sm text-muted mb-xs">Thank you for the quick help with my account access.</p>
                    <p className="body-sm text-muted">Technical • 1 day ago</p>
                  </div>

                  {/* Ticket 3 */}
                  <div className="border border-border rounded-lg p-md">
                    <div className="flex items-start justify-between mb-xs">
                      <span className="label-md text-tertiary">Billing question - escalated</span>
                      <div className="px-2 py-0.5 bg-red-100 text-red-800 rounded-full text-xs font-medium">Escalated</div>
                    </div>
                    <p className="body-sm text-muted mb-xs">Need to discuss enterprise pricing options...</p>
                    <p className="body-sm text-muted">Billing • 3 days ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Caption */}
        <div className="text-center mt-lg">
          <Link href="/conversations" className="body-md text-tertiary hover:text-primary transition-colors">
            Explore the live workspace →
          </Link>
        </div>
      </div>
    </section>
  );
}
