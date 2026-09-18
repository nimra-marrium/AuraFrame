"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

/**
 * Shared "who's logged in + logout" chip. Derives a display name from
 * the email (everything before @) rather than showing the raw address.
 */
export default function UserMenu() {
  const router = useRouter();
  const { user, logout } = useAuth();

  if (!user) return null;

  const username = user.email.split("@")[0];

  return (
    <div className="flex items-center gap-3">
      <span className="rounded-full bg-neutral-100 px-3 py-1 text-sm font-medium text-neutral-700">
        {username}
      </span>
      <button
        onClick={() => {
          logout();
          router.push("/login");
        }}
        className="rounded-lg border border-neutral-300 px-3 py-1.5 text-sm text-neutral-600 transition hover:border-neutral-900 hover:text-neutral-900"
      >
        Log out
      </button>
    </div>
  );
}