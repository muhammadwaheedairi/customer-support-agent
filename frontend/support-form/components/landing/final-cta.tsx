"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export function FinalCTA() {
  return (
    <section className="py-[120px] lg:py-[160px] bg-surface">
      <div className="mx-auto max-w-4xl px-gutter text-center">
        <h2 className="text-[48px] lg:text-[64px] font-bold leading-[1.1] text-tertiary tracking-tight mb-lg">
          Try it yourself
        </h2>
        <p className="body-lg text-muted mb-xl max-w-xl mx-auto">
          Open the live workspace and see how AI handles customer support conversations.
        </p>
        <Link href="/conversations">
          <Button variant="primary" size="lg" className="text-xl px-8 py-4 h-auto">
            Open Workspace
            <ArrowRight className="ml-2 h-6 w-6" />
          </Button>
        </Link>
        <p className="body-sm text-muted mt-lg">
          Portfolio project by Muhammad Waheed
        </p>
      </div>
    </section>
  );
}
