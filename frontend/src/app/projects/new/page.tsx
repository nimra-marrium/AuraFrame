"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api, ApiError } from "@/lib/api";
import Navbar from "@/components/Navbar";

interface Project {
  id: string;
}

export default function NewProjectPage() {
  const router = useRouter();
  const { user, token } = useAuth();

  const [name, setName] = useState("");
  const [briefText, setBriefText] = useState("");
  const [projectType, setProjectType] = useState("");
  const [targetAudience, setTargetAudience] = useState("");
  const [desiredMood, setDesiredMood] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!user || !token) return;

    setError(null);
    setSubmitting(true);

    try {
      const project = await api.post<Project>(
        "/projects/",
        {
          user_id: user.user_id,
          name,
          brief_text: briefText,
          project_type: projectType || undefined,
          target_audience: targetAudience || undefined,
          desired_mood: desiredMood || undefined,
        },
        token
      );
      router.push(`/projects/${project.id}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-stone-50">
      <Navbar showNewProject={false} />

      <div className="mx-auto max-w-2xl px-8 py-10">
        <h1 className="mb-1 text-xl font-semibold text-stone-900">New project</h1>
        <p className="mb-8 text-sm text-stone-500">
          Describe what you're creating. You can add reference images next.
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="mb-1 block text-sm font-medium text-stone-700">
              Project name
            </label>
            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Matcha Café Identity"
              className="w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-stone-700">
              Creative brief
            </label>
            <textarea
              required
              rows={4}
              value={briefText}
              onChange={(e) => setBriefText(e.target.value)}
              placeholder="I want to create a visual identity for a premium matcha café aimed at young professionals. I want it to feel calm, modern, feminine, Japanese-inspired, and slightly playful."
              className="w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500"
            />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-stone-700">
                Project type <span className="text-stone-400">(optional)</span>
              </label>
              <input
                value={projectType}
                onChange={(e) => setProjectType(e.target.value)}
                placeholder="Branding"
                className="w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500"
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-stone-700">
                Target audience <span className="text-stone-400">(optional)</span>
              </label>
              <input
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                placeholder="Young professionals"
                className="w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500"
              />
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-stone-700">
              Desired mood <span className="text-stone-400">(optional)</span>
            </label>
            <input
              value={desiredMood}
              onChange={(e) => setDesiredMood(e.target.value)}
              placeholder="Calm, modern, feminine, playful"
              className="w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500"
            />
          </div>

          {error && (
            <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="rounded-md bg-stone-900 px-5 py-2 text-sm font-medium text-white hover:bg-stone-800 disabled:opacity-50"
          >
            {submitting ? "Creating..." : "Create project"}
          </button>
        </form>
      </div>
    </main>
  );
}
