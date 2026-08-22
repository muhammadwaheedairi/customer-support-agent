"use client";

import { ArrowRight, Shield, Clock, Zap } from "lucide-react";
import Link from "next/link";

export function Hero() {
  return (
    <section className="relative pt-[100px] pb-[120px] lg:pt-[140px] lg:pb-[160px] overflow-hidden">
      
      {/* Background subtle grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#00000008_1px,transparent_1px),linear-gradient(to_bottom,#00000008_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />

      <div className="relative mx-auto max-w-5xl px-gutter">

        {/* Badge */}
        <div className="flex justify-center mb-lg">
          <div className="inline-flex items-center gap-xs px-md py-xs rounded-full border border-border bg-surface">
            <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
            <span className="label-sm text-muted">AI-Powered • Available 24/7</span>
          </div>
        </div>

        {/* Headline */}
        <h1 className="text-center mb-lg">
          <span className="block text-[56px] lg:text-[80px] font-bold leading-[1.05] text-tertiary tracking-tight">
            Stop Losing Clients
          </span>
          <span className="block text-[56px] lg:text-[80px] font-bold leading-[1.05] tracking-tight">
            to{" "}
            <span className="relative inline-block text-tertiary">
              <span className="relative z-10">Slow Support</span>
              <span className="absolute bottom-1 left-0 right-0 h-3 lg:h-4 bg-primary -rotate-1 opacity-60 rounded-sm" />
            </span>
          </span>
        </h1>

        {/* Subheadline */}
        <p className="text-center text-[18px] lg:text-[22px] leading-[1.6] text-muted mb-xl max-w-2xl mx-auto">
          LexDesk gives your law firm a 24/7 AI support agent that resolves client inquiries instantly — no hiring, no waiting, no missed leads.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-md mb-xl">
          <Link href="/sign-up">
            <button className="inline-flex items-center gap-sm px-xl py-md bg-primary text-secondary rounded-lg text-[17px] font-semibold hover:opacity-90 transition-opacity w-full sm:w-auto justify-center">
              Start Free Trial
              <ArrowRight className="h-5 w-5" />
            </button>
          </Link>
          <Link href="/conversations">
            <button className="inline-flex items-center gap-sm px-xl py-md border border-border text-tertiary rounded-lg text-[17px] font-semibold hover:bg-surface transition-colors w-full sm:w-auto justify-center">
              See Live Demo
            </button>
          </Link>
        </div>

        {/* Stats Row */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-lg sm:gap-xl mb-xl">
          <div className="text-center">
            <p className="text-[36px] font-bold text-tertiary leading-none mb-xs">80%</p>
            <p className="body-sm text-muted">Inquiries resolved automatically</p>
          </div>
          <div className="hidden sm:block w-px h-12 bg-border" />
          <div className="text-center">
            <p className="text-[36px] font-bold text-tertiary leading-none mb-xs">&lt;30s</p>
            <p className="body-sm text-muted">Average response time</p>
          </div>
          <div className="hidden sm:block w-px h-12 bg-border" />
          <div className="text-center">
            <p className="text-[36px] font-bold text-tertiary leading-none mb-xs">99%</p>
            <p className="body-sm text-muted">Cost savings vs human agent</p>
          </div>
        </div>

        {/* Trust Pills */}
        <div className="flex flex-wrap items-center justify-center gap-sm">
          <div className="inline-flex items-center gap-xs px-md py-xs rounded-full border border-border bg-surface">
            <Shield className="h-3.5 w-3.5 text-muted" />
            <span className="label-sm text-muted">SOC 2 Compliant</span>
          </div>
          <div className="inline-flex items-center gap-xs px-md py-xs rounded-full border border-border bg-surface">
            <Clock className="h-3.5 w-3.5 text-muted" />
            <span className="label-sm text-muted">No Setup Required</span>
          </div>
          <div className="inline-flex items-center gap-xs px-md py-xs rounded-full border border-border bg-surface">
            <Zap className="h-3.5 w-3.5 text-muted" />
            <span className="label-sm text-muted">Live in 30 Minutes</span>
          </div>
        </div>

      </div>
    </section>
  );
}