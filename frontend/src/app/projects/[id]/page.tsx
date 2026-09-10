"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api, uploadFile, ApiError } from "@/lib/api";

interface Project {
  id: string;
  name: string;
  brief_text: string;
  project_type?: string;
  target_audience?: string;
  desired_mood?: string;
  status: string;
}

interface ImageRecord {
  id: string;
  url: string;
  analysis: Record<string, unknown> | null;
}

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { user, token, loading: authLoading } = useAuth();

  const [project, setProject] = useState<Project | null>(null);
  const [images, setImages] = useState<ImageRecord[]>([]);
  const [loadingProject, setLoadingProject] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [authLoading, user, router]);

  useEffect(() => {
    if (!token) return;
    setError(null);
    api
      .get<Project>(`/projects/${projectId}`, token)
      .then(setProject)
      .catch(() => setError("Could not load this project."))
      .finally(() => setLoadingProject(false));

    api
      .get<ImageRecord[]>(`/images/project/${projectId}`, token)
      .then(setImages)
      .catch(() => setImages([]));
  }, [projectId, token]);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !token) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("project_id", projectId);
      formData.append("file", file);
      const newImage = await uploadFile("/images/", formData, token);
      setImages((prev) => [...prev, newImage as ImageRecord]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Upload failed. Please try again.");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  if (authLoading || loadingProject) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-400">Loading...</p>
      </main>
    );
  }

  if (!project) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-500">Project not found.</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-stone-50">
      <header className="border-b border-stone-200 px-8 py-4">
        <Link href="/dashboard" className="text-sm text-stone-500 hover:text-stone-800">
          ← Back to dashboard
        </Link>
      </header>

      <div className="mx-auto max-w-3xl px-8 py-10">
        <div className="mb-8">
          <h1 className="text-xl font-semibold text-stone-900">{project.name}</h1>
          <p className="mt-2 text-sm text-stone-600">{project.brief_text}</p>
          <div className="mt-3 flex gap-2">
            {project.project_type && (
              <span className="rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                {project.project_type}
              </span>
            )}
            {project.target_audience && (
              <span className="rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                {project.target_audience}
              </span>
            )}
          </div>
        </div>

        <section>
          <h2 className="mb-3 text-sm font-medium text-stone-700">
            Reference images ({images.length})
          </h2>

          <div className="mb-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {images.map((img) => (
              <div
                key={img.id}
                className="aspect-square overflow-hidden rounded-md border border-stone-200 bg-white"
              >
                <img
                  src={img.url}
                  alt=""
                  className="h-full w-full object-cover"
                />
              </div>
            ))}

            <label className="flex aspect-square cursor-pointer items-center justify-center rounded-md border border-dashed border-stone-300 text-sm text-stone-400 hover:border-stone-400 hover:text-stone-600">
              {uploading ? "Uploading..." : "+ Add image"}
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                disabled={uploading}
                className="hidden"
              />
            </label>
          </div>

          {error && (
            <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
          )}
        </section>
      </div>
    </main>
  );
}