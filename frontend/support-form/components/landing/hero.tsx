"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export function Hero() {
  return (
    <section className="relative pt-[120px] pb-[140px] lg:pt-[160px] lg:pb-[180px]">
      <div className="mx-auto max-w-6xl px-gutter">
        {/* Headline - Extra large, more spacing */}
        <h1 className="text-center mb-lg">
          <span className="block text-[72px] lg:text-[96px] font-bold leading-[1.05] text-tertiary tracking-tight">
            Customer Support
          </span>
          <span className="block text-[72px] lg:text-[96px] font-bold leading-[1.05] text-tertiary tracking-tight">
            That Actually{" "}
            <span className="relative inline-block">
              <span className="relative z-10">Works</span>
              <span className="absolute bottom-2 left-0 right-0 h-4 bg-primary -rotate-1 opacity-50" />
            </span>
          </span>
        </h1>

        {/* Subheadline - Single sentence, better spacing */}
        <p className="text-center text-[20px] lg:text-[24px] leading-[1.5] text-muted mb-xl max-w-3xl mx-auto">
          AI agent resolves 80% of inquiries in under 5 seconds using OpenAI Agents SDK,
          RAG, and automatic escalation.
        </p>

        {/* Single CTA */}
        <div className="flex justify-center mb-xl">
          <Link href="/conversations">
            <Button variant="primary" size="lg" className="text-xl px-8 py-4 h-auto">
              Try the Workspace
              <ArrowRight className="ml-2 h-6 w-6" />
            </Button>
          </Link>
        </div>

        {/* Trust indicator - smaller, more subtle */}
        <div className="text-center">
          <p className="body-sm text-muted opacity-60">
            Built for law firms • PostgreSQL + pgvector • Cohere + Qdrant
          </p>
        </div>
      </div>
    </section>
  );
}
