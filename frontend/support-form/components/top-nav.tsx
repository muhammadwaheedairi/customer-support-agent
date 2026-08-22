"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { clsx } from "clsx";
import { UserButton, Show, useAuth } from "@clerk/nextjs";
import { Menu, X } from "lucide-react";

export function TopNav() {
  const pathname = usePathname();
  const { userId } = useAuth();
  const adminId = process.env.NEXT_PUBLIC_ADMIN_USER_ID;
  const isAdmin = userId === adminId;
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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
    ...(isAdmin ? [{
      href: "/admin",
      label: "Admin",
      active: pathname?.startsWith("/admin"),
    }] : []),
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-neutral/80 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-4 sm:px-gutter">
        <div className="flex h-16 items-center justify-between gap-2">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group shrink-0">
            <div className="relative h-8 w-8 rounded-lg bg-primary flex items-center justify-center transition-transform group-hover:scale-105">
              <span className="text-[18px] font-bold text-secondary">L</span>
            </div>
            <span className="text-[16px] sm:text-[20px] font-semibold text-tertiary tracking-tight">
              LexDesk
            </span>
          </Link>

          {/* Desktop right side */}
          <div className="hidden md:flex items-center gap-4">
            <Show when="signed-in">
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
                    {item.active && (
                      <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-primary rounded-full" />
                    )}
                  </Link>
                ))}
              </nav>
              <UserButton
                appearance={{
                  elements: { avatarBox: "h-8 w-8" },
                }}
              />
            </Show>

            <Show when="signed-out">
              <Link
                href="/sign-in"
                className="px-4 py-2 text-[15px] font-medium text-muted hover:text-tertiary transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/sign-up"
                className="px-4 py-2 text-[15px] font-medium bg-primary text-secondary rounded-lg hover:opacity-90 transition-opacity"
              >
                Get Started
              </Link>
            </Show>
          </div>

          {/* Mobile right side: UserButton (if signed in) + hamburger */}
          <div className="flex md:hidden items-center gap-3">
            <Show when="signed-in">
              <UserButton
                appearance={{
                  elements: { avatarBox: "h-8 w-8" },
                }}
              />
            </Show>
            <button
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              className={clsx(
                "relative h-10 w-10 flex items-center justify-center rounded-lg transition-colors duration-200",
                mobileMenuOpen
                  ? "bg-surface text-tertiary"
                  : "text-tertiary hover:bg-surface"
              )}
              aria-label="Toggle menu"
              aria-expanded={mobileMenuOpen}
            >
              <span className="relative h-5 w-5">
                <Menu
                  className={clsx(
                    "absolute inset-0 h-5 w-5 transition-all duration-200",
                    mobileMenuOpen
                      ? "opacity-0 rotate-90 scale-75"
                      : "opacity-100 rotate-0 scale-100"
                  )}
                />
                <X
                  className={clsx(
                    "absolute inset-0 h-5 w-5 transition-all duration-200",
                    mobileMenuOpen
                      ? "opacity-100 rotate-0 scale-100"
                      : "opacity-0 -rotate-90 scale-75"
                  )}
                />
              </span>
            </button>
          </div>
        </div>

        {/* Mobile dropdown menu */}
        <div
          className={clsx(
            "md:hidden grid transition-all duration-300 ease-in-out",
            mobileMenuOpen
              ? "grid-rows-[1fr] opacity-100"
              : "grid-rows-[0fr] opacity-0"
          )}
        >
          <div className="overflow-hidden">
            <div className="border-t border-border/50 py-3">
              <Show when="signed-in">
                <nav className="flex flex-col gap-0.5">
                  {navItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={clsx(
                        "px-3 py-3 rounded-lg text-[15px] font-medium transition-colors",
                        item.active
                          ? "text-tertiary bg-surface"
                          : "text-muted hover:text-tertiary hover:bg-surface/60"
                      )}
                    >
                      {item.label}
                    </Link>
                  ))}
                </nav>
              </Show>

              <Show when="signed-out">
                <div className="flex flex-col gap-2 px-1">
                  <Link
                    href="/sign-in"
                    onClick={() => setMobileMenuOpen(false)}
                    className="px-3 py-3 rounded-lg text-[15px] font-medium text-muted hover:text-tertiary hover:bg-surface/60 transition-colors text-center"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/sign-up"
                    onClick={() => setMobileMenuOpen(false)}
                    className="px-3 py-3 rounded-lg text-[15px] font-medium bg-primary text-secondary text-center hover:opacity-90 transition-opacity"
                  >
                    Get Started
                  </Link>
                </div>
              </Show>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}