"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
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

  if (loading || !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-stone-50">
      <Navbar showDashboard={false} />

      <div className="mx-auto max-w-4xl px-8 py-10">
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-stone-900">Your projects</h2>
        </div>

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
                <Link href={`/projects/${project.id}`} className="block pr-10">
                  <h3 className="font-medium text-stone-900">{project.name}</h3>
                  <p className="mt-1 line-clamp-2 text-sm text-stone-500">
                    {project.brief_text}
                  </p>
                  <span className="mt-3 inline-block rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                    {project.status}
                  </span>
                </Link>
                {project.status === "draft" && (
                  <Link
                    href={`/projects/${project.id}?edit=1`}
                    aria-label={`Edit ${project.name}`}
                    title="Edit draft project"
                    className="absolute right-4 top-4 rounded-md border border-stone-200 px-2 py-1 text-sm text-stone-500 transition hover:border-stone-400 hover:text-stone-900"
                  >
                    ✎
                  </Link>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
