"use client";

import { useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api, ApiError } from "@/lib/api";
import Navbar from "@/components/Navbar";
import { toPng } from "html-to-image";

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

export default function BoardPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { user, token, loading: authLoading } = useAuth();

  const [board, setBoard] = useState<Board | null>(null);
  const [images, setImages] = useState<ImageRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

  const boardRef = useRef<HTMLDivElement>(null);

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

  const imageEls = (board?.layout_data.filter((el) => el.type === "image") ?? []).filter(
    (el) => imageUrlFor(el.ref)
  );
  const swatchEls = board?.layout_data.filter((el) => el.type === "swatch") ?? [];
  const textEls = board?.layout_data.filter((el) => el.type === "text") ?? [];

  // Total tiles: title tiles + images + one tile holding all swatches
  const tileCount = textEls.length + imageEls.length + (swatchEls.length > 0 ? 1 : 0);
  const cols = tileCount <= 2 ? 2 : tileCount <= 6 ? 3 : tileCount <= 12 ? 4 : 5;
  const rows = Math.max(1, Math.ceil(tileCount / cols));

  async function handleExport() {
    if (!boardRef.current) return;
    setExporting(true);
    setExportError(null);

    try {
      const dataUrl = await toPng(boardRef.current, {
        pixelRatio: 2,
        cacheBust: true,
        backgroundColor: "#ffffff",
      });
      const link = document.createElement("a");
      link.href = dataUrl;
      link.download = `moodboard-${projectId}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch {
      setExportError("Export failed. Please try again.");
    } finally {
      setExporting(false);
    }
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
      <Navbar />

      <div className="mx-auto max-w-5xl px-8 py-6">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold text-stone-900">Moodboard</h1>
          {board && (
            <button
              type="button"
              onClick={handleExport}
              disabled={exporting}
              className="inline-flex items-center rounded-md bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {exporting ? "Exporting..." : "Export"}
            </button>
          )}
        </div>

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

        {exportError && (
          <p className="mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
            {exportError}
          </p>
        )}

        {board && (
          <div
            ref={boardRef}
            className="box-border grid gap-3 rounded-lg border border-stone-200 bg-white p-4 shadow-sm"
            style={{
              height: "calc(100vh - 190px)",
              minHeight: 420,
              gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`,
              gridTemplateRows: `repeat(${rows}, minmax(0, 1fr))`,
            }}
          >
            {textEls.map((el, i) => (
              <div
                key={`t-${i}`}
                className="flex min-h-0 items-center justify-center rounded-md bg-stone-900 px-4 text-center"
              >
                <p className="text-sm font-medium text-white">{el.content}</p>
              </div>
            ))}

            {imageEls.map((el, i) => (
              <div
                key={`i-${i}`}
                className="min-h-0 overflow-hidden rounded-md bg-stone-100"
              >
                <img
                  src={imageUrlFor(el.ref)}
                  alt=""
                  crossOrigin="anonymous"
                  className="h-full w-full object-contain"
                />
              </div>
            ))}

            {swatchEls.length > 0 && (
              <div className="flex min-h-0 gap-2">
                {swatchEls.map((el, i) => (
                  <div
                    key={`s-${i}`}
                    style={{ backgroundColor: el.color }}
                    className="h-full flex-1 rounded-md border border-stone-200"
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}