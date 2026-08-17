"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { clsx } from "clsx";

export function TopNav() {
  const pathname = usePathname();

  const navItems = [
    {
      href: "/conversations",
      label: "Conversations",
      active: pathname?.startsWith("/conversations"),
    },
    {
      href: "/help",
      label: "Help Center",
      active: pathname?.startsWith("/help"),
    },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-neutral/80 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-gutter">
        <div className="flex h-16 items-center justify-between">
          {/* Logo with icon */}
          <Link href="/" className="flex items-center gap-2 group">
            {/* Logo mark - lime square with L */}
            <div className="relative h-8 w-8 rounded-lg bg-primary flex items-center justify-center transition-transform group-hover:scale-105">
              <span className="text-[18px] font-bold text-secondary">L</span>
            </div>
            <span className="text-[20px] font-semibold text-tertiary tracking-tight">
              LexDesk
            </span>
          </Link>

          {/* Navigation - refined, minimal */}
          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={clsx(
                  "relative px-4 py-2 text-[15px] font-medium transition-colors",
                  item.active
                    ? "text-tertiary"
                    : "text-muted hover:text-tertiary"
                )}
              >
                {item.label}
                {/* Active indicator - lime underline */}
                {item.active && (
                  <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-primary rounded-full" />
                )}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
