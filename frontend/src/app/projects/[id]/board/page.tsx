"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api, ApiError } from "@/lib/api";

interface BoardElement {
  type: string;
  ref?: string;
  color?: string;
  content?: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

interface Board {
  id: string;
  project_id: string;
  layout_data: BoardElement[];
  updated_at: string;
}

interface ImageRecord {
  id: string;
  url: string;
}

const CANVAS_WIDTH = 1200;
const CANVAS_HEIGHT = 800;

export default function BoardPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { user, token, loading: authLoading } = useAuth();

  const [board, setBoard] = useState<Board | null>(null);
  const [images, setImages] = useState<ImageRecord[]>([]);
  const [loading, setLoading] = useState(true);
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
      .get<Board>(`/boards/${projectId}`, token)
      .then(setBoard)
      .catch((err) =>
        setError(err instanceof ApiError ? err.message : "Could not load board.")
      )
      .finally(() => setLoading(false));

    api
      .get<ImageRecord[]>(`/images/project/${projectId}`, token)
      .then(setImages)
      .catch(() => setImages([]));
  }, [projectId, token]);

  function imageUrlFor(ref?: string): string | undefined {
    return images.find((img) => img.id === ref)?.url;
  }

  if (authLoading || loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-400">Loading board...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-stone-50">
      <header className="border-b border-stone-200 px-8 py-4">
        <Link
          href={`/projects/${projectId}`}
          className="text-sm text-stone-500 hover:text-stone-800"
        >
          ← Back to project
        </Link>
      </header>

      <div className="mx-auto max-w-5xl px-8 py-10">
        <h1 className="mb-6 text-xl font-semibold text-stone-900">Mood board</h1>

        {error && (
          <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
            {error.toLowerCase().includes("not found") && (
              <p className="mt-1 text-red-600">
                Run the AI analysis on the project page first to generate a board.
              </p>
            )}
          </div>
        )}

        {board && (
          <div
            className="relative mx-auto w-full overflow-hidden rounded-lg border border-stone-200 bg-white shadow-sm"
            style={{
              aspectRatio: `${CANVAS_WIDTH} / ${CANVAS_HEIGHT}`,
            }}
          >
            {board.layout_data.map((el, i) => {
              const style: React.CSSProperties = {
                position: "absolute",
                left: `${(el.x / CANVAS_WIDTH) * 100}%`,
                top: `${(el.y / CANVAS_HEIGHT) * 100}%`,
                width: `${(el.w / CANVAS_WIDTH) * 100}%`,
                height: `${(el.h / CANVAS_HEIGHT) * 100}%`,
              };

              if (el.type === "image") {
                const url = imageUrlFor(el.ref);
                return url ? (
                  <img
                    key={i}
                    src={url}
                    alt=""
                    style={style}
                    className="rounded-md object-cover"
                  />
                ) : null;
              }

              if (el.type === "swatch") {
                return (
                  <div
                    key={i}
                    style={{ ...style, backgroundColor: el.color }}
                    className="rounded-md"
                  />
                );
              }

              if (el.type === "text") {
                return (
                  <div
                    key={i}
                    style={style}
                    className="flex items-center justify-center rounded-md bg-stone-900 p-3 text-center"
                  >
                    <p className="text-sm font-medium text-white">{el.content}</p>
                  </div>
                );
              }

              return null;
            })}
          </div>
        )}
      </div>
    </main>
  );
}