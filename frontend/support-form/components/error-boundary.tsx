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
    <div className="min-h-[400px] flex items-center justify-center p-md sm:p-lg">
      <div className="text-center max-w-md w-full">
        <div className="inline-flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-red-50 rounded-full mb-md">
          <AlertCircle className="h-7 w-7 sm:h-8 sm:w-8 text-error" />
        </div>
        <h2 className="headline-sm text-tertiary mb-sm">Something went wrong</h2>
        <p className="body-md text-muted mb-lg">
          An unexpected error occurred. Please try again or contact support if the problem persists.
        </p>
        <button
          onClick={reset}
          className="inline-flex items-center gap-sm px-md sm:px-lg py-sm bg-primary text-secondary rounded-lg label-md hover:opacity-90 transition-opacity w-full sm:w-auto justify-center"
        >
          <RefreshCw className="h-4 w-4" />
          Try Again
        </button>
      </div>
    </div>
  );
}