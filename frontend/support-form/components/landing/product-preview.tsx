"use client";

import Link from "next/link";
import { CheckCircle2, Clock, ArrowUpRight } from "lucide-react";

export function ProductPreview() {
  return (
    <section className="py-[80px] lg:py-[120px] bg-surface">
      <div className="mx-auto max-w-7xl px-gutter">
        {/* Section Header */}
        <div className="text-center mb-xl max-w-2xl mx-auto">
          <p className="label-md text-primary mb-sm uppercase tracking-wider">
            Live Product
          </p>
          <h2 className="headline-lg text-tertiary mb-sm">See It In Action</h2>
          <p className="body-lg text-muted">
            Real AI responses. Real law firm workflows. Zero wait time.
          </p>
        </div>

        {/* Two column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-lg items-center">
          {/* Left — Product UI */}
          <div className="rounded-xl border border-border bg-neutral overflow-hidden shadow-xl">
            {/* Browser bar */}
            <div className="border-b border-border bg-surface px-md py-sm flex items-center gap-sm">
              <div className="flex items-center gap-xs">
                <div className="h-2.5 w-2.5 rounded-full bg-red-400" />
                <div className="h-2.5 w-2.5 rounded-full bg-yellow-400" />
                <div className="h-2.5 w-2.5 rounded-full bg-green-400" />
              </div>
              <div className="flex-1 mx-sm">
                <div className="bg-neutral border border-border rounded px-sm py-xs body-sm text-muted text-center">
                  lexdesk.io/conversations
                </div>
              </div>
            </div>

            {/* Nav */}
            <div className="border-b border-border px-md py-sm flex items-center justify-between">
              <div className="flex items-center gap-xs">
                <div className="h-6 w-6 rounded bg-primary flex items-center justify-center">
                  <span className="text-[12px] font-bold text-secondary">
                    L
                  </span>
                </div>
                <span className="label-md text-tertiary">LexDesk</span>
              </div>
              <div className="flex items-center gap-md">
                <span className="body-sm text-tertiary border-b border-primary pb-xs">
                  Conversations
                </span>
                <span className="body-sm text-muted">Help Center</span>
              </div>
            </div>

            {/* Content */}
            <div className="p-md">
              <div className="flex items-center justify-between mb-md">
                <h3 className="label-lg text-tertiary">Conversations</h3>
                <div className="px-sm py-xs bg-primary text-secondary rounded label-sm">
                  + New
                </div>
              </div>

              {/* Tickets */}
              <div className="space-y-xs">
                {/* Active ticket */}
                <div className="border border-primary/30 rounded-lg p-sm bg-primary/5">
                  <div className="flex items-start justify-between mb-xs">
                    <div className="flex items-center gap-xs">
                      <div className="h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0 mt-1" />
                      <span className="label-sm text-tertiary text-[13px]">
                        How do I set up client intake forms?
                      </span>
                    </div>
                    <span className="px-xs py-[2px] bg-blue-100 text-blue-700 rounded-full text-[11px] font-medium flex-shrink-0">
                      Open
                    </span>
                  </div>
                  <p className="body-sm text-muted text-[12px] pl-sm">
                    general • 2 minutes ago
                  </p>
                </div>

                {/* Resolved */}
                <div className="border border-border rounded-lg p-sm">
                  <div className="flex items-start justify-between mb-xs">
                    <span className="label-sm text-tertiary text-[13px]">
                      Cannot login to my account
                    </span>
                    <span className="px-xs py-[2px] bg-green-100 text-green-700 rounded-full text-[11px] font-medium flex-shrink-0">
                      Resolved
                    </span>
                  </div>
                  <p className="body-sm text-muted text-[12px]">
                    technical • 1 hour ago
                  </p>
                </div>

                {/* Escalated */}
                <div className="border border-border rounded-lg p-sm">
                  <div className="flex items-start justify-between mb-xs">
                    <span className="label-sm text-tertiary text-[13px]">
                      Refund request for annual plan
                    </span>
                    <span className="px-xs py-[2px] bg-red-100 text-red-700 rounded-full text-[11px] font-medium flex-shrink-0">
                      Escalated
                    </span>
                  </div>
                  <p className="body-sm text-muted text-[12px]">
                    billing • 3 hours ago
                  </p>
                </div>
              </div>

              {/* AI Response Preview */}
              <div className="mt-md border border-border rounded-lg p-sm bg-surface">
                <p className="label-sm text-muted text-[11px] mb-xs">
                  LexDesk AI Assistant • 26s ago
                </p>
                <p className="body-sm text-tertiary text-[13px] leading-relaxed">
                  To set up client intake forms, go to{" "}
                  <strong>Intake &gt; Form Builder</strong>, click "New Form",
                  select your practice area template, and customize fields using
                  drag and drop...
                </p>
              </div>
            </div>
          </div>

          {/* Right — Benefits */}
          <div className="space-y-lg">
            <div>
              <h3 className="headline-md text-tertiary mb-md">
                Your clients get answers.
                <br />
                You get time back.
              </h3>
              <p className="body-lg text-muted">
                LexDesk's AI agent handles routine client inquiries around the
                clock — so your team can focus on billable work.
              </p>
            </div>

            {/* Feature list */}
            <div className="space-y-md">
              {[
                {
                  title: "Instant AI Responses",
                  desc: "Clients get accurate answers in under 30 seconds, any time of day.",
                },
                {
                  title: "Smart Escalation",
                  desc: "Billing disputes, legal threats, and angry clients are automatically routed to your team.",
                },
                {
                  title: "Complete Audit Trail",
                  desc: "Every conversation is logged, searchable, and exportable for compliance.",
                },
                {
                  title: "Works With Your Workflow",
                  desc: "Integrates with your existing intake forms, billing, and case management.",
                },
              ].map((item) => (
                <div key={item.title} className="flex items-start gap-sm">
                  <CheckCircle2 className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="label-md text-tertiary mb-xs">{item.title}</p>
                    <p className="body-sm text-muted">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Response time badge + CTA */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-md">
              <div className="inline-flex items-center gap-sm px-md py-sm border border-border rounded-lg bg-neutral">
                <Clock className="h-4 w-4 text-primary" />
                <span className="body-sm text-tertiary">
                  Average AI response time: <strong>26 seconds</strong>
                </span>
              </div>

              <Link
                href="/conversations"
                className="group inline-flex items-center gap-xs body-md font-medium text-primary bg-surface border border-default rounded-full px-4 py-2 hover:bg-secondary hover:border-strong transition-all duration-200"
              >
                Try the live workspace
                <ArrowUpRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
