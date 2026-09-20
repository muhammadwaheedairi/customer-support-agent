"use client";

import {
  Clock,
  Shield,
  TrendingUp,
  Users,
  MessageSquare,
  Zap,
} from "lucide-react";

const features = [
  {
    icon: Clock,
    title: "24/7 Availability",
    description:
      "Your customers get instant answers at 2 AM, on weekends, and during holidays — without you lifting a finger.",
  },
  {
    icon: Zap,
    title: "Instant AI Responses",
    description:
      "Average response time under 30 seconds. No more customers waiting hours for a simple answer about their project or task.",
  },
  {
    icon: TrendingUp,
    title: "80% Auto-Resolved",
    description:
      "Routine inquiries — password resets, integration setup, subscription questions — handled automatically without human intervention.",
  },
  {
    icon: Shield,
    title: "Smart Escalation",
    description:
      "Frustrated customers, refund requests, and critical issues are instantly routed to your team with full context attached.",
  },
  {
    icon: MessageSquare,
    title: "Complete Audit Trail",
    description:
      "Every conversation is logged, timestamped, and exportable. Stay compliant with SOC 2 and GDPR requirements effortlessly.",
  },
  {
    icon: Users,
    title: "Customer Portal Ready",
    description:
      "Customers log in, submit inquiries, and track their ticket status — all from a branded, professional interface.",
  },
];

export function FeatureGrid() {
  return (
    <section className="py-[80px] lg:py-[120px]">
      <div className="mx-auto max-w-6xl px-gutter">
        {/* Section Header */}
        <div className="text-center mb-xl max-w-2xl mx-auto">
          <p className="label-md text-primary mb-sm uppercase tracking-wider">
            Why FlowSync
          </p>
          <h2 className="headline-lg text-tertiary mb-sm">
            Everything Your Team Needs
          </h2>
          <p className="body-lg text-muted">
            Built specifically for software teams and agencies. No generic chatbot — a support
            system that understands project management workflows.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-md">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="border border-border rounded-xl p-lg bg-neutral hover:border-primary/50 hover:bg-surface transition-all group"
              >
                <div className="mb-md">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 group-hover:bg-primary/20 transition-colors">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                </div>
                <h3 className="label-lg text-tertiary mb-xs">
                  {feature.title}
                </h3>
                <p className="body-md text-muted leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="mt-xl text-center">
          <div className="inline-flex items-center gap-sm px-lg py-md border border-border rounded-xl bg-surface">
            <span className="body-md text-muted">
              From <strong className="text-tertiary">5-person startups</strong>{" "}
              to 500+ enterprise teams
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
