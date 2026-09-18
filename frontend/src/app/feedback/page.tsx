"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";

const FEEDBACK_EMAIL = "nimramarrium02@gmail.com";

export default function FeedbackPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  const subject = encodeURIComponent("AuraFrame feedback");
  const body = encodeURIComponent(message);
  window.open(
    `https://mail.google.com/mail/?view=cm&fs=1&to=${FEEDBACK_EMAIL}&su=${subject}&body=${body}`,
    "_blank",
    "noopener,noreferrer"
  );
  setSent(true);
}

  if (loading || !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-white">
        <p className="text-sm text-neutral-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col bg-neutral-50">
      <Navbar />
      <div className="flex flex-1 justify-center items-start px-8 pt-16">
        <div className="w-full max-w-xl rounded-2xl border border-neutral-200 bg-white p-10 shadow-sm">
          <h1 className="mb-2 font-serif text-2xl font-medium text-neutral-900">
            Feedback
          </h1>
          <p className="mb-8 text-sm leading-relaxed text-neutral-500">
            Have a suggestion, found a bug, or just want to share a thought?
            Send it our way and Gmail will open with your message ready to send.
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <textarea
              required
              rows={6}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Tell us what's on your mind..."
              className="w-full rounded-lg border border-neutral-300 px-3.5 py-2.5 text-sm text-neutral-900 focus:border-neutral-900 focus:outline-none focus:ring-1 focus:ring-neutral-900"
            />
            <button
              type="submit"
              className="w-full cursor-pointer rounded-lg bg-neutral-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-neutral-700 active:scale-[0.99]"
            >
              Send feedback
            </button>
            {sent && (
              <p className="text-center text-sm text-neutral-500">
                Opening Gmail...
              </p>
            )}
          </form>
        </div>
      </div>
    </main>
  );
}
