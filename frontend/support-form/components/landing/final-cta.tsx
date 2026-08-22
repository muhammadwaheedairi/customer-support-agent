"use client";

import { ArrowRight, Check } from "lucide-react";
import Link from "next/link";

const benefits = [
  "14-day free trial — no credit card required",
  "Setup in under 30 minutes",
  "Cancel anytime",
];

export function FinalCTA() {
  return (
    <section className="py-[100px] lg:py-[140px] bg-surface">
      <div className="mx-auto max-w-4xl px-gutter text-center">

        {/* Badge */}
        <div className="inline-flex items-center gap-xs px-md py-xs rounded-full border border-border bg-neutral mb-lg">
          <div className="h-2 w-2 rounded-full bg-primary" />
          <span className="label-sm text-muted">Start free today</span>
        </div>

        {/* Headline */}
        <h2 className="text-[44px] lg:text-[60px] font-bold leading-[1.1] text-tertiary tracking-tight mb-md">
          Ready to Automate
          <br />
          Your Client Support?
        </h2>

        <p className="body-lg text-muted mb-xl max-w-xl mx-auto">
          Join hundreds of law firms that have cut support costs by 99% while improving client response times.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-md mb-xl">
          <Link href="/sign-up">
            <button className="inline-flex items-center gap-sm px-xl py-md bg-primary text-secondary rounded-lg text-[17px] font-semibold hover:opacity-90 transition-opacity w-full sm:w-auto justify-center">
              Start Free Trial
              <ArrowRight className="h-5 w-5" />
            </button>
          </Link>
          <Link href="/conversations">
            <button className="inline-flex items-center gap-sm px-xl py-md border border-border text-tertiary rounded-lg text-[17px] font-semibold hover:bg-neutral transition-colors w-full sm:w-auto justify-center">
              See Live Demo
            </button>
          </Link>
        </div>

        {/* Benefits */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-md">
          {benefits.map((benefit) => (
            <div key={benefit} className="flex items-center gap-xs">
              <Check className="h-4 w-4 text-primary flex-shrink-0" />
              <span className="body-sm text-muted">{benefit}</span>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}