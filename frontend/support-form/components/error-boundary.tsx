"use client";

import { useEffect } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorBoundaryProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorBoundary({ error, reset }: ErrorBoundaryProps) {
  useEffect(() => {
    console.error("Error boundary caught:", error);
  }, [error]);

  return (
    <div className="min-h-[400px] flex items-center justify-center p-lg">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-red-50 rounded-full mb-md">
          <AlertCircle className="h-8 w-8 text-error" />
        </div>
        <h2 className="headline-sm text-tertiary mb-sm">Something went wrong</h2>
        <p className="body-md text-muted mb-lg">
          An unexpected error occurred. Please try again or contact support if the problem persists.
        </p>
        <button
          onClick={reset}
          className="inline-flex items-center gap-sm px-lg py-sm bg-primary text-secondary rounded-lg label-md hover:opacity-90 transition-opacity"
        >
          <RefreshCw className="h-4 w-4" />
          Try Again
        </button>
      </div>
    </div>
  );
}
