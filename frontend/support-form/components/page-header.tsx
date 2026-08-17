import * as React from "react";
import { clsx } from "clsx";

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function PageHeader({
  title,
  description,
  action,
  className,
}: PageHeaderProps) {
  return (
    <div className={clsx("flex items-start justify-between mb-lg", className)}>
      <div>
        <h1 className="headline-md text-tertiary">{title}</h1>
        {description && (
          <p className="body-md text-muted mt-xs">{description}</p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
