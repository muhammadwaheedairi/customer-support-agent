"use client";

import { Bot, Zap, Shield } from "lucide-react";

const features = [
  {
    icon: Bot,
    title: "AI Agent with Function Tools",
    description: "OpenAI Agents SDK with GPT-4o and 5 specialized tools for search, escalation, and response generation.",
  },
  {
    icon: Zap,
    title: "Knowledge-Aware Responses",
    description: "RAG pipeline with Cohere embeddings, Qdrant vector search, and reranking for accurate answers from 500+ docs.",
  },
  {
    icon: Shield,
    title: "Production Infrastructure",
    description: "PostgreSQL + pgvector, async operations, connection pooling, and automatic escalation with sentiment analysis.",
  },
];

export function FeatureGrid() {
  return (
    <section className="py-[80px] lg:py-[120px]">
      <div className="mx-auto max-w-6xl px-gutter">
        {/* Section Header */}
        <div className="text-center mb-xl max-w-2xl mx-auto">
          <h2 className="headline-lg text-tertiary mb-sm">Built for Scale</h2>
          <p className="body-lg text-muted">
            Enterprise-grade AI customer support with real-time responses and automatic escalation.
          </p>
        </div>

        {/* Feature Grid - 3 columns only */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-xl">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="text-center">
                <div className="mb-md flex justify-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-surface border border-border">
                    <Icon className="h-8 w-8 text-tertiary" />
                  </div>
                </div>
                <h3 className="headline-sm text-tertiary mb-sm">{feature.title}</h3>
                <p className="body-md text-muted">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
