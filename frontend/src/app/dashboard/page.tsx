"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api, deleteImage } from "@/lib/api";
import Navbar from "@/components/Navbar";

interface Project {
  id: string;
  name: string;
  brief_text: string;
  status: string;
  created_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, token, loading } = useAuth();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  useEffect(() => {
    if (user && token) {
      api
        .get<Project[]>(`/projects/user/${user.user_id}`, token)
        .then(setProjects)
        .catch(() => setProjects([]))
        .finally(() => setLoadingProjects(false));
    }
  }, [user, token]);

  async function handleDeleteProject(project: Project) {
    if (!token) return;

    const confirmed = window.confirm(
      `Delete "${project.name}"? This will also remove its images and moodboard. This can't be undone.`
    );
    if (!confirmed) return;

    setDeletingId(project.id);
    setDeleteError(null);

    try {
      await deleteImage(`/projects/${project.id}`, token);
      setProjects((previous) => previous.filter((p) => p.id !== project.id));
    } catch (err) {
      setDeleteError(
        err instanceof Error ? err.message : "Could not delete project. Please try again."
      );
    } finally {
      setDeletingId(null);
    }
  }

  if (loading || !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-stone-50">
      <Navbar showDashboard={false} inlineActions />

      <div className="mx-auto max-w-4xl px-8 py-10">
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-stone-900">Your projects</h2>
        </div>

        {deleteError && (
          <p className="mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
            {deleteError}
          </p>
        )}

        {loadingProjects ? (
          <p className="text-sm text-stone-400">Loading projects...</p>
        ) : projects.length === 0 ? (
          <div className="rounded-lg border border-dashed border-stone-300 px-6 py-16 text-center">
            <p className="text-sm text-stone-500">
              No projects yet. Create your first one to get started.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {projects.map((project) => (
              <div
                key={project.id}
                className="relative rounded-lg border border-stone-200 bg-white p-5 transition hover:border-stone-400"
              >
                <Link
                  href={`/projects/${project.id}`}
                  className={`block ${project.status === "draft" ? "pr-28" : "pr-4"}`}
                >
                  <h3 className="font-medium text-stone-900">{project.name}</h3>
                  <p className="mt-1 line-clamp-2 text-sm text-stone-500">
                    {project.brief_text}
                  </p>
                  <span className="mt-3 inline-block rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                    {project.status}
                  </span>
                </Link>
                {project.status === "draft" && (
                  <div className="absolute right-4 top-4 flex gap-2">
  <Link
    href={`/projects/${project.id}?edit=1`}
    aria-label={`Edit ${project.name}`}
    title="Edit draft project"
    className="flex h-10 w-10 items-center justify-center rounded-md border border-stone-200 text-stone-500 transition hover:border-stone-400 hover:text-stone-900"
  >
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
    </svg>
  </Link>
  <button
    type="button"
    onClick={() => handleDeleteProject(project)}
    disabled={deletingId === project.id}
    aria-label={`Delete ${project.name}`}
    title="Delete draft project"
    className="flex h-10 w-10 items-center justify-center rounded-md border border-stone-200 text-stone-500 transition hover:border-red-300 hover:bg-red-50 hover:text-red-600 disabled:cursor-not-allowed disabled:opacity-50"
  >
    {deletingId === project.id ? (
      "…"
    ) : (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="3 6 5 6 21 6" />
        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
        <path d="M10 11v6" />
        <path d="M14 11v6" />
        <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
      </svg>
    )}
   </button>
</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}