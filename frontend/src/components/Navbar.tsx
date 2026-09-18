"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import Logo from "@/components/Logo";

/**
 * Shared site navbar. Used on every authenticated page except login/signup.
 * Wider than a plain page header (px-4 instead of px-8) so it uses more
 * of the total screen width, per request.
 */
interface NavbarProps {
  showDashboard?: boolean;
  showNewProject?: boolean;
  onExport?: () => void;
  exportDisabled?: boolean;
}

export default function Navbar({
  showDashboard = true,
  showNewProject = true,
  onExport,
  exportDisabled = false,
}: NavbarProps) {
  const router = useRouter();
  const { logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="flex items-center justify-between border-b border-neutral-200 bg-white px-4 py-4">
      <div className="flex items-center gap-8">
        <Logo />
        <nav className="flex items-center gap-6">
          <Link
            href="/feedback"
            className="text-sm text-neutral-600 hover:text-neutral-900"
          >
            Feedback
          </Link>
          <Link
            href="/about"
            className="text-sm text-neutral-600 hover:text-neutral-900"
          >
            About Us
          </Link>
          {showDashboard && (
            <Link
              href="/dashboard"
              className="text-sm text-neutral-600 hover:text-neutral-900"
            >
              Dashboard
            </Link>
          )}
        </nav>
      </div>

      <div className="relative">
        <button
          type="button"
          onClick={() => setMenuOpen((isOpen) => !isOpen)}
          aria-expanded={menuOpen}
          aria-label="Open navigation menu"
          className="flex h-10 w-10 items-center justify-center rounded-lg border border-neutral-300 text-neutral-700 transition hover:border-neutral-900 hover:text-neutral-900"
        >
          <span className="text-xl leading-none">☰</span>
        </button>
        {menuOpen && (
          <>
            <button
              type="button"
              aria-label="Close navigation menu"
              onClick={() => setMenuOpen(false)}
              className="fixed inset-0 z-10 cursor-default"
            />
            <div className="absolute right-0 top-12 z-20 w-44 rounded-lg border border-neutral-200 bg-white p-2 shadow-lg">
              {onExport && (
                <button
                  type="button"
                  onClick={() => {
                    onExport();
                    setMenuOpen(false);
                  }}
                  disabled={exportDisabled}
                  className="w-full rounded-md px-3 py-2 text-left text-sm text-neutral-700 hover:bg-neutral-100 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {exportDisabled ? "Exporting..." : "Export mood board"}
                </button>
              )}
              {showNewProject && (
                <Link
                  href="/projects/new"
                  onClick={() => setMenuOpen(false)}
                  className="block rounded-md px-3 py-2 text-sm text-neutral-700 hover:bg-neutral-100"
                >
                  New project
                </Link>
              )}
              <button
                type="button"
                onClick={() => {
                  logout();
                  router.push("/login");
                }}
                className="w-full rounded-md px-3 py-2 text-left text-sm text-red-700 hover:bg-red-50"
              >
                Log out
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
