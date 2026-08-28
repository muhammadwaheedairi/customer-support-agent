"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { Star, Loader2, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface SatisfactionRatingProps {
  ticketId: string;
  existingRating?: number | null;
  existingComment?: string | null;
}

export function SatisfactionRating({
  ticketId,
  existingRating,
  existingComment,
}: SatisfactionRatingProps) {
  const { getToken } = useAuth();
  const [rating, setRating] = useState<number>(0);
  const [hovered, setHovered] = useState<number>(0);
  const [comment, setComment] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const labels = ["", "Poor", "Fair", "Good", "Very Good", "Excellent"];

  // Already rated — show existing rating
  if (existingRating || submitted) {
    const displayRating = submitted ? rating : existingRating!;
    return (
      <div className="border border-border rounded-lg p-md bg-surface">
        <div className="flex items-center gap-sm mb-sm">
          <CheckCircle2 className="h-5 w-5 text-primary" />
          <p className="label-md text-tertiary">Your Feedback</p>
        </div>
        <div className="flex items-center gap-xs mb-xs">
          {[1, 2, 3, 4, 5].map((star) => (
            <Star
              key={star}
              className={`h-6 w-6 ${
                star <= displayRating
                  ? "fill-primary text-primary"
                  : "text-border"
              }`}
            />
          ))}
          <span className="body-sm text-muted ml-xs">
            {labels[displayRating]} ({displayRating}/5)
          </span>
        </div>
        {(submitted ? comment : existingComment) && (
          <p className="body-sm text-muted italic">
            "{submitted ? comment : existingComment}"
          </p>
        )}
      </div>
    );
  }

  const handleSubmit = async () => {
    if (!rating) return;
    setSubmitting(true);
    try {
      const token = await getToken();
      const response = await fetch(`${API_URL}/tickets/${ticketId}/rate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ rating, comment }),
      });

      if (!response.ok) throw new Error("Failed to submit rating");

      setSubmitted(true);
      toast.success("Thank you for your feedback!");
    } catch (err) {
      toast.error("Failed to submit rating. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="border border-border rounded-lg p-md bg-surface">
      <p className="label-md text-tertiary mb-md">
        How satisfied are you with this response?
      </p>

      {/* Stars */}
      <div className="flex items-center gap-xs mb-sm">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => setRating(star)}
            onMouseEnter={() => setHovered(star)}
            onMouseLeave={() => setHovered(0)}
            className="transition-transform hover:scale-110"
          >
            <Star
              className={`h-8 w-8 transition-colors ${
                star <= (hovered || rating)
                  ? "fill-primary text-primary"
                  : "text-border"
              }`}
            />
          </button>
        ))}
        {(hovered || rating) > 0 && (
          <span className="body-sm text-muted ml-sm">
            {labels[hovered || rating]}
          </span>
        )}
      </div>

      {/* Comment + Submit */}
      {rating > 0 && (
        <div className="mt-md">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Any additional comments? (optional)"
            rows={3}
            className="w-full rounded-lg border border-border bg-neutral px-md py-sm body-sm text-tertiary focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            maxLength={500}
          />
          <div className="flex items-center justify-between mt-sm">
            <span className="body-sm text-muted">{comment.length}/500</span>
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="inline-flex items-center gap-xs px-md py-sm bg-primary text-secondary rounded-lg label-sm hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {submitting ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                "Submit Rating"
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}