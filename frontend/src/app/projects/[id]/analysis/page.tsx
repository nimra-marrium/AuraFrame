"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import Navbar from "@/components/Navbar";

interface BriefAnalysis {
  objective?: string;
  audience?: string;
  tone: string[];
  keywords: string[];
  constraints: string[];
}

interface CollectiveAnalysis {
  recurring_colors: string[];
  recurring_motifs: string[];
  common_aesthetic?: string;
  outliers: string[];
  overall_mood?: string;
}

interface Typography {
  heading?: string;
  body?: string;
}

interface CreativeDirection {
  direction_name?: string;
  palette: string[];
  typography?: Typography;
  imagery_direction?: string;
  avoid: string[];
}

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

interface StoredAnalysis {
  briefAnalysis: BriefAnalysis | null;
  collectiveAnalysis: CollectiveAnalysis | null;
  direction: CreativeDirection | null;
  boardElements: BoardElement[] | null;
}

export default function ProjectAnalysisPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { user, token, loading: authLoading } = useAuth();

  const [data, setData] = useState<StoredAnalysis | null>(null);
  const [hasMoodBoard, setHasMoodBoard] = useState(false);
  const [checkedBoard, setCheckedBoard] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [authLoading, user, router]);

  useEffect(() => {
    const raw = sessionStorage.getItem(`auraframe_analysis_${projectId}`);
    if (raw) {
      try {
        setData(JSON.parse(raw));
      } catch {
        setData(null);
      }
    }
  }, [projectId]);

  useEffect(() => {
    if (!token) return;
    api
      .get(`/boards/${projectId}`, token)
      .then(() => setHasMoodBoard(true))
      .catch(() => setHasMoodBoard(false))
      .finally(() => setCheckedBoard(true));
  }, [projectId, token]);

  if (authLoading || !checkedBoard) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-stone-50">
        <p className="text-sm text-stone-400">Loading...</p>
      </main>
    );
  }

  const briefAnalysis = data?.briefAnalysis ?? null;
  const collectiveAnalysis = data?.collectiveAnalysis ?? null;
  const direction = data?.direction ?? null;
  const boardElements = data?.boardElements ?? null;

  return (
    <main className="min-h-screen bg-stone-50">
      <Navbar />
      <div className="mx-auto max-w-3xl px-8 py-10">
        <Link
          href={`/projects/${projectId}`}
          className="mb-6 inline-block text-sm text-stone-500 hover:text-stone-900"
        >
          ← Back to project
        </Link>

        <h1 className="mb-6 text-xl font-semibold text-stone-900">Visual identity</h1>

        {!briefAnalysis && !hasMoodBoard && (
          <p className="rounded-md bg-stone-100 px-4 py-3 text-sm text-stone-600">
            No analysis results to show here yet — run "Get visual identity" from the project page.
          </p>
        )}

        {briefAnalysis && (
          <div className="mb-4 rounded-lg border border-stone-200 bg-white p-5">
            <h3 className="mb-2 text-sm font-semibold text-stone-800">Brief analysis</h3>
            <p className="text-sm text-stone-600">
              <span className="font-medium">Objective:</span> {briefAnalysis.objective}
            </p>
            <p className="mt-1 text-sm text-stone-600">
              <span className="font-medium">Audience:</span> {briefAnalysis.audience}
            </p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {briefAnalysis.tone.map((t) => (
                <span key={t} className="rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                  {t}
                </span>
              ))}
            </div>
          </div>
        )}

        {collectiveAnalysis && (
          <div className="mb-4 rounded-lg border border-stone-200 bg-white p-5">
            <h3 className="mb-2 text-sm font-semibold text-stone-800">Visual patterns</h3>
            <p className="text-sm text-stone-600">{collectiveAnalysis.overall_mood}</p>
            <div className="mt-3 flex gap-1.5">
              {collectiveAnalysis.recurring_colors.map((c) => (
                <div
                  key={c}
                  className="h-8 w-8 rounded-full border border-stone-200"
                  style={{ backgroundColor: c }}
                  title={c}
                />
              ))}
            </div>
          </div>
        )}

        {direction && (
          <div className="mb-4 rounded-lg border border-stone-200 bg-white p-5">
            <h3 className="mb-1 text-sm font-semibold text-stone-800">
              {direction.direction_name}
            </h3>
            <p className="mt-2 text-sm text-stone-600">{direction.imagery_direction}</p>
            <div className="mt-3 flex gap-1.5">
              {direction.palette.map((c) => (
                <div
                  key={c}
                  className="h-10 w-10 rounded-md border border-stone-200"
                  style={{ backgroundColor: c }}
                  title={c}
                />
              ))}
            </div>
            {direction.typography && (
              <p className="mt-3 text-xs text-stone-500">
                Heading: {direction.typography.heading} · Body: {direction.typography.body}
              </p>
            )}
          </div>
        )}
        {(boardElements || hasMoodBoard) && (
            <div className="mb-4">
                <Link
                href={`/projects/${projectId}/board`}
                className="inline-flex rounded-md bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800">
                    View Moodboard
                </Link>
            </div>
        )}
      </div>
    </main>
  );
}