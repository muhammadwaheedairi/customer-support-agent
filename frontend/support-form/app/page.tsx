"use client";

import { Hero } from "@/components/landing/hero";
import { ProductPreview } from "@/components/landing/product-preview";
import { FeatureGrid } from "@/components/landing/feature-grid";
import { FinalCTA } from "@/components/landing/final-cta";
import { TopNav } from "@/components/top-nav";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-neutral">
      <TopNav />
      <Hero />
      <ProductPreview />
      <FeatureGrid />
      <FinalCTA />
    </div>
  );
}
