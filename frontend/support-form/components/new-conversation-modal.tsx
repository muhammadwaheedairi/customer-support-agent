"use client";

import { useState } from "react";
import { X, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useAuth, useUser } from "@clerk/nextjs";
import { clsx } from "clsx";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const CATEGORIES = [
  { value: "general", label: "General Question" },
  { value: "technical", label: "Technical Support" },
  { value: "billing", label: "Billing Inquiry" },
  { value: "bug_report", label: "Bug Report" },
  { value: "feedback", label: "Feedback" },
];

const PRIORITIES = [
  { value: "low", label: "Low - Not urgent" },
  { value: "medium", label: "Medium - Need help soon" },
  { value: "high", label: "High - Urgent issue" },
];

interface FormData {
  name: string;
  email: string;
  subject: string;
  category: string;
  priority: string;
  message: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  subject?: string;
  message?: string;
}

interface NewConversationModalProps {
  onClose: () => void;
  onSuccess: (ticketId: string) => void;
}

export function NewConversationModal({ onClose, onSuccess }: NewConversationModalProps) {
  const { getToken } = useAuth();
  const { user } = useUser();

  const [formData, setFormData] = useState<FormData>({
    name: user?.fullName || user?.firstName || "",
    email: user?.primaryEmailAddress?.emailAddress || "",
    subject: "",
    category: "general",
    priority: "medium",
    message: "",
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const validateField = (name: keyof FormData, value: string): string | undefined => {
    switch (name) {
      case "name":
        if (value.trim().length < 2) return "Name must be at least 2 characters";
        break;
      case "email":
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Please enter a valid email address";
        break;
      case "subject":
        if (value.trim().length < 5) return "Subject must be at least 5 characters";
        break;
      case "message":
        if (value.trim().length < 20) return "Message must be at least 20 characters";
        break;
    }
    return undefined;
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    const error = validateField(name as keyof FormData, value);
    if (error) {
      setErrors((prev) => ({ ...prev, [name]: error }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    ["name", "email", "subject", "message"].forEach((field) => {
      const error = validateField(field as keyof FormData, formData[field as keyof FormData]);
      if (error) newErrors[field as keyof FormErrors] = error;
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      // Clerk JWT token lo
      const token = await getToken();

      if (!token) {
        throw new Error("Authentication required. Please sign in again.");
      }

      const response = await fetch(`${API_URL}/support/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to submit form");
      }

      const data = await response.json();
      onSuccess(data.ticket_id);

    } catch (error) {
      console.error("Form submission error:", error);
      setSubmitError(
        error instanceof Error ? error.message : "Failed to submit form. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-overlay/50 flex items-center justify-center p-gutter z-50">
      <div className="bg-neutral rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-border">
        {/* Header */}
        <div className="sticky top-0 bg-neutral border-b border-border px-lg py-md flex items-center justify-between">
          <h2 className="headline-sm text-tertiary">New Conversation</h2>
          <button
            onClick={onClose}
            className="text-muted hover:text-tertiary transition-colors"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-lg space-y-md">
          {submitError && (
            <div className="p-md bg-red-50 border border-error rounded-lg text-error body-sm">
              {submitError}
            </div>
          )}

          {/* Name */}
          <div>
            <label htmlFor="name" className="block label-md text-tertiary mb-xs">
              Your Name <span className="text-error">*</span>
            </label>
            <Input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              onBlur={handleBlur}
              error={!!errors.name}
              placeholder="John Doe"
              required
            />
            {errors.name && <p className="mt-xs body-sm text-error">{errors.name}</p>}
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block label-md text-tertiary mb-xs">
              Email Address <span className="text-error">*</span>
            </label>
            <Input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              error={!!errors.email}
              placeholder="john@example.com"
              required
            />
            {errors.email && <p className="mt-xs body-sm text-error">{errors.email}</p>}
          </div>

          {/* Subject */}
          <div>
            <label htmlFor="subject" className="block label-md text-tertiary mb-xs">
              Subject <span className="text-error">*</span>
            </label>
            <Input
              type="text"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              onBlur={handleBlur}
              error={!!errors.subject}
              placeholder="Brief description of your issue"
              required
            />
            {errors.subject && <p className="mt-xs body-sm text-error">{errors.subject}</p>}
          </div>

          {/* Category and Priority */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-md">
            <div>
              <label htmlFor="category" className="block label-md text-tertiary mb-xs">
                Category <span className="text-error">*</span>
              </label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="flex w-full rounded-lg border border-border bg-neutral px-4 py-3 h-12 text-md text-tertiary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat.value} value={cat.value}>{cat.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="priority" className="block label-md text-tertiary mb-xs">
                Priority
              </label>
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="flex w-full rounded-lg border border-border bg-neutral px-4 py-3 h-12 text-md text-tertiary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                {PRIORITIES.map((pri) => (
                  <option key={pri.value} value={pri.value}>{pri.label}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Message */}
          <div>
            <label htmlFor="message" className="block label-md text-tertiary mb-xs">
              How can we help? <span className="text-error">*</span>
            </label>
            <Textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              onBlur={handleBlur}
              error={!!errors.message}
              rows={6}
              placeholder="Please describe your issue or question in detail..."
              required
            />
            {errors.message && <p className="mt-xs body-sm text-error">{errors.message}</p>}
            <p className="mt-xs body-sm text-muted">{formData.message.length}/5000 characters</p>
          </div>

          {/* Actions */}
          <div className="flex gap-sm justify-end pt-md">
            <Button type="button" variant="secondary" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5 mr-2" />
                  Submitting...
                </>
              ) : (
                "Submit Request"
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}