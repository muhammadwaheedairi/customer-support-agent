import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { clsx } from "clsx";

const buttonVariants = cva(
  "inline-flex items-center justify-center font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:opacity-50 disabled:cursor-not-allowed",
  {
    variants: {
      variant: {
        primary: "bg-primary hover:bg-primary-hover text-secondary",
        secondary: "bg-transparent border border-border text-tertiary hover:bg-surface",
        tertiary: "bg-transparent text-tertiary hover:underline p-0",
        ghost: "bg-transparent text-tertiary hover:bg-surface",
      },
      size: {
        default: "h-10 px-5 py-2.5 text-lg rounded-lg",
        sm: "h-8 px-3 py-1.5 text-sm rounded",
        lg: "h-12 px-6 py-3 text-xl rounded-lg",
        icon: "h-10 w-10 rounded-lg",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={clsx(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
