"use client";

import { useState } from "react";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/page-header";
import { Search, Loader2, BookOpen, ChevronDown, ChevronUp } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface SearchResult {
  title: string;
  content: string;
  category: string;
  relevance_score: number;
}

export default function HelpCenterPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setSearched(true);
    setResults([]);
    setExpandedIndex(null);

    try {
      const response = await fetch(
        `${API_URL}/help/search?q=${encodeURIComponent(query.trim())}`
      );

      if (!response.ok) throw new Error("Search failed");

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  };

  const categoryColors: Record<string, string> = {
    billing: "bg-yellow-100 text-yellow-800",
    technical: "bg-blue-100 text-blue-800",
    guide: "bg-green-100 text-green-800",
    general: "bg-gray-100 text-gray-700",
  };

  const popularTopics = [
    "How to set up intake forms",
    "Reset my password",
    "Generate LEDES invoice",
    "Connect Gmail integration",
    "Migrate from Clio",
    "Set up two-factor authentication",
    "Add team members",
    "Cancel subscription",
  ];

  return (
    <AppShell>
      <PageHeader
        title="Help Center"
        description="Search our knowledge base for instant answers"
      />

      {/* Search Box */}
      <div className="max-w-2xl mx-auto mb-xl">
        <form onSubmit={handleSearch} className="flex gap-sm">
          <div className="relative flex-1">
            <Search className="absolute left-md top-1/2 -translate-y-1/2 h-5 w-5 text-muted" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for help... e.g. 'how to reset password'"
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-border bg-neutral text-tertiary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent body-md"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-lg py-sm bg-primary text-secondary rounded-lg label-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-sm"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              "Search"
            )}
          </button>
        </form>
      </div>

      {/* Popular Topics — shown before search */}
      {!searched && (
        <div className="max-w-2xl mx-auto">
          <p className="label-md text-muted mb-md">Popular Topics</p>
          <div className="flex flex-wrap gap-sm">
            {popularTopics.map((topic) => (
              <button
                key={topic}
                onClick={() => {
                  setQuery(topic);
                }}
                className="px-md py-sm border border-border rounded-lg body-sm text-tertiary hover:bg-surface hover:border-primary transition-colors"
              >
                {topic}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-xl">
          <Loader2 className="h-8 w-8 animate-spin text-muted" />
          <span className="ml-sm body-md text-muted">Searching knowledge base...</span>
        </div>
      )}

      {/* No Results */}
      {searched && !loading && results.length === 0 && (
        <div className="max-w-2xl mx-auto text-center py-xl border border-border rounded-lg bg-neutral">
          <BookOpen className="h-12 w-12 text-muted mx-auto mb-md" />
          <p className="body-lg text-tertiary mb-sm">No results found</p>
          <p className="body-sm text-muted">
            Try different keywords or{" "}
            <a href="/conversations" className="text-primary hover:underline">
              start a conversation
            </a>{" "}
            with our support team.
          </p>
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="max-w-2xl mx-auto">
          <p className="label-md text-muted mb-md">
            {results.length} result{results.length !== 1 ? "s" : ""} for "{query}"
          </p>
          <div className="space-y-sm">
            {results.map((result, index) => (
              <div
                key={index}
                className="border border-border rounded-lg bg-neutral overflow-hidden"
              >
                {/* Result Header */}
                <button
                  onClick={() =>
                    setExpandedIndex(expandedIndex === index ? null : index)
                  }
                  className="w-full flex items-center justify-between px-lg py-md hover:bg-surface transition-colors text-left"
                >
                  <div className="flex items-center gap-sm flex-1 min-w-0">
                    <BookOpen className="h-5 w-5 text-primary flex-shrink-0" />
                    <span className="label-md text-tertiary truncate">
                      {result.title}
                    </span>
                    <span
                      className={`px-sm py-xs rounded-full text-xs font-medium flex-shrink-0 ${
                        categoryColors[result.category] || categoryColors.general
                      }`}
                    >
                      {result.category}
                    </span>
                  </div>
                  {expandedIndex === index ? (
                    <ChevronUp className="h-4 w-4 text-muted flex-shrink-0 ml-sm" />
                  ) : (
                    <ChevronDown className="h-4 w-4 text-muted flex-shrink-0 ml-sm" />
                  )}
                </button>

                {/* Result Content */}
                {expandedIndex === index && (
                  <div className="px-lg pb-lg border-t border-border pt-md">
                    <p className="body-md text-tertiary whitespace-pre-wrap">
                      {result.content}
                    </p>
                    <div className="mt-md pt-md border-t border-border">
                      <p className="body-sm text-muted">
                        Still need help?{" "}
                        <a
                          href="/conversations"
                          className="text-primary hover:underline"
                        >
                          Start a conversation
                        </a>{" "}
                        with our support team.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </AppShell>
  );
}