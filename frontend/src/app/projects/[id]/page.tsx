"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { api, uploadFile, deleteImage, ApiError } from "@/lib/api";
import Navbar from "@/components/Navbar";

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
  analysis: VisualAnalysis | null;
}

interface BriefAnalysis {
  objective?: string;
  audience?: string;
  tone: string[];
  keywords: string[];
  constraints: string[];
}

interface VisualAnalysis {
  colors: string[];
  style?: string;
  objects: string[];
  composition?: string;
  lighting?: string;
  keywords: string[];
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

type AnalysisStage =
  | "idle"
  | "brief"
  | "visual"
  | "collective"
  | "direction"
  | "board"
  | "saving"
  | "done";

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { user, token, loading: authLoading } = useAuth();

  const [project, setProject] = useState<Project | null>(null);
  const [images, setImages] = useState<ImageRecord[]>([]);
  const [loadingProject, setLoadingProject] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingImageId, setDeletingImageId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [stage, setStage] = useState<AnalysisStage>("idle");
  const [briefAnalysis, setBriefAnalysis] = useState<BriefAnalysis | null>(null);
  const [collectiveAnalysis, setCollectiveAnalysis] = useState<CollectiveAnalysis | null>(null);
  const [direction, setDirection] = useState<CreativeDirection | null>(null);
  const [boardElements, setBoardElements] = useState<BoardElement[] | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [hasMoodBoard, setHasMoodBoard] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState("");
  const [editBrief, setEditBrief] = useState("");
  const [editProjectType, setEditProjectType] = useState("");
  const [editTargetAudience, setEditTargetAudience] = useState("");
  const [editDesiredMood, setEditDesiredMood] = useState("");
  const [savingProject, setSavingProject] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [authLoading, user, router]);

  useEffect(() => {
    if (window.location.search.includes("edit=1")) {
      setIsEditing(true);
    }
  }, []);

  useEffect(() => {
    if (!token) return;
    setError(null);
    api
      .get<Project>(`/projects/${projectId}`, token)
      .then((loadedProject) => {
        setProject(loadedProject);
        setEditName(loadedProject.name);
        setEditBrief(loadedProject.brief_text);
        setEditProjectType(loadedProject.project_type ?? "");
        setEditTargetAudience(loadedProject.target_audience ?? "");
        setEditDesiredMood(loadedProject.desired_mood ?? "");
      })
      .catch(() => setError("Could not load this project."))
      .finally(() => setLoadingProject(false));

    api
      .get<ImageRecord[]>(`/images/project/${projectId}`, token)
      .then(setImages)
      .catch(() => setImages([]));

    api
      .get(`/boards/${projectId}`, token)
      .then(() => setHasMoodBoard(true))
      .catch(() => setHasMoodBoard(false));
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

  async function handleDeleteImage(imageId: string) {
    if (!token) return;

    setDeletingImageId(imageId);
    setError(null);

    try {
      await deleteImage(`/images/${imageId}`, token);
      setImages((previousImages) => previousImages.filter((image) => image.id !== imageId));
    } catch (err) {
      setError(
        err instanceof ApiError || err instanceof Error
          ? err.message
          : "Could not delete image. Please try again."
      );
    } finally {
      setDeletingImageId(null);
    }
  }

  async function handleProjectSave(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;

    setSavingProject(true);
    setEditError(null);

    try {
      const updatedProject = await api.put<Project>(
        `/projects/${projectId}`,
        {
          name: editName,
          brief_text: editBrief,
          project_type: editProjectType || null,
          target_audience: editTargetAudience || null,
          desired_mood: editDesiredMood || null,
        },
        token
      );
      setProject(updatedProject);
      setIsEditing(false);
      router.replace(`/projects/${projectId}`);
    } catch (err) {
      setEditError(err instanceof ApiError ? err.message : "Could not save changes. Please try again.");
    } finally {
      setSavingProject(false);
    }
  }

  function cancelProjectEdit() {
    if (project) {
      setEditName(project.name);
      setEditBrief(project.brief_text);
      setEditProjectType(project.project_type ?? "");
      setEditTargetAudience(project.target_audience ?? "");
      setEditDesiredMood(project.desired_mood ?? "");
    }
    setEditError(null);
    setIsEditing(false);
    router.replace(`/projects/${projectId}`);
  }

  async function runAnalysis() {
    if (!project || !token || images.length < 2) return;

    setAnalysisError(null);
    setBriefAnalysis(null);
    setCollectiveAnalysis(null);
    setDirection(null);
    setBoardElements(null);
    setAnalysisProgress(0);

    const totalSteps = images.length + 5;
    let completedSteps = 0;
    const updateProgress = () => {
      completedSteps += 1;
      setAnalysisProgress(Math.round((completedSteps / totalSteps) * 100));
    };

    try {
      setStage("brief");
      const brief = await api.post<BriefAnalysis>(
        "/agents/brief/",
        { brief_text: project.brief_text },
        token
      );
      setBriefAnalysis(brief);
      updateProgress();

      setStage("visual");
      const visualAnalyses: VisualAnalysis[] = [];
      for (const img of images) {
        const analysis = await api.post<VisualAnalysis>(
          "/agents/visual/",
          { image_url: img.url },
          token
        );
        visualAnalyses.push(analysis);
        updateProgress();
      }

      setStage("collective");
      const collective = await api.post<CollectiveAnalysis>(
        "/agents/collective/",
        { analyses: visualAnalyses },
        token
      );
      setCollectiveAnalysis(collective);
      updateProgress();

      setStage("direction");
      const creativeDirection = await api.post<CreativeDirection>(
        "/agents/direction/",
        { brief_analysis: brief, collective_analysis: collective },
        token
      );
      setDirection(creativeDirection);
      updateProgress();

      setStage("board");
      const boardResult = await api.post<{ elements: BoardElement[] }>(
        "/agents/board/",
        { direction: creativeDirection, image_ids: images.map((img) => img.id) },
        token
      );
      setBoardElements(boardResult.elements);
      updateProgress();

      setStage("saving");
      await api.put(`/boards/${projectId}`, { elements: boardResult.elements }, token);
      setHasMoodBoard(true);
      updateProgress();

      setStage("done");
    } catch (err) {
      setAnalysisError(
        err instanceof ApiError ? err.message : "Analysis failed. Please try again."
      );
      setStage("idle");
    }
  }

  const stageLabels: Record<AnalysisStage, string> = {
    idle: "",
    brief: "Analyzing your brief...",
    visual: "Analyzing reference images...",
    collective: "Finding patterns across images...",
    direction: "Generating creative direction...",
    board: "Composing mood board layout...",
    saving: "Saving board...",
    done: "",
  };

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

  const isAnalyzing = stage !== "idle" && stage !== "done";

  return (
    <main className="min-h-screen bg-stone-50">
      <Navbar />
      <div className="mx-auto max-w-3xl px-8 py-10">
        {isEditing ? (
          <form onSubmit={handleProjectSave} className="mb-8 rounded-lg border border-stone-200 bg-white p-6">
            <div className="mb-5 flex items-center justify-between">
              <h1 className="text-xl font-semibold text-stone-900">Edit draft project</h1>
              <button type="button" onClick={cancelProjectEdit} className="text-sm text-stone-500 hover:text-stone-900">
                Cancel
              </button>
            </div>
            <div className="space-y-4">
              <label className="block text-sm font-medium text-stone-700">Project name
                <input required value={editName} onChange={(e) => setEditName(e.target.value)} className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500" />
              </label>
              <label className="block text-sm font-medium text-stone-700">Creative brief
                <textarea required rows={4} value={editBrief} onChange={(e) => setEditBrief(e.target.value)} className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500" />
              </label>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <label className="block text-sm font-medium text-stone-700">Project type
                  <input value={editProjectType} onChange={(e) => setEditProjectType(e.target.value)} className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500" />
                </label>
                <label className="block text-sm font-medium text-stone-700">Target audience
                  <input value={editTargetAudience} onChange={(e) => setEditTargetAudience(e.target.value)} className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500" />
                </label>
              </div>
              <label className="block text-sm font-medium text-stone-700">Desired mood
                <input value={editDesiredMood} onChange={(e) => setEditDesiredMood(e.target.value)} className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2 text-sm focus:border-stone-500 focus:outline-none focus:ring-1 focus:ring-stone-500" />
              </label>
              {editError && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{editError}</p>}
              <button disabled={savingProject} className="rounded-md bg-stone-900 px-5 py-2 text-sm font-medium text-white hover:bg-stone-800 disabled:opacity-50">
                {savingProject ? "Saving..." : "Save changes"}
              </button>
            </div>
          </form>
        ) : (
          <div className="mb-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h1 className="text-xl font-semibold text-stone-900">{project.name}</h1>
                <p className="mt-2 text-sm text-stone-600">{project.brief_text}</p>
              </div>
              {project.status === "draft" && (
                <button onClick={() => setIsEditing(true)} className="rounded-md border border-stone-200 px-3 py-1.5 text-sm text-stone-600 hover:border-stone-400 hover:text-stone-900">
                  ✎ Edit
                </button>
              )}
            </div>
            <div className="mt-3 flex gap-2">
              {project.project_type && <span className="rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">{project.project_type}</span>}
              {project.target_audience && <span className="rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-600">{project.target_audience}</span>}
            </div>
          </div>
        )}

        <section className="mb-10">
          <h2 className="mb-3 text-sm font-medium text-stone-700">
            Reference images ({images.length})
          </h2>

          <div className="mb-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {images.map((img) => (
              <div
                key={img.id}
                className="group relative aspect-square overflow-hidden rounded-md border border-stone-200 bg-white"
              >
                <img src={img.url} alt="" className="h-full w-full object-cover" />
                <button
                  type="button"
                  onClick={() => handleDeleteImage(img.id)}
                  disabled={deletingImageId === img.id}
                  aria-label="Delete reference image"
                  className="absolute right-2 top-2 rounded-full bg-neutral-900 px-2 py-1 text-xs font-medium text-white opacity-0 shadow-sm transition hover:bg-red-700 focus:opacity-100 group-hover:opacity-100 disabled:cursor-not-allowed disabled:opacity-100"
                >
                  {deletingImageId === img.id ? "Removing..." : "Delete"}
                </button>
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

        <section className="mb-10">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-stone-700">AI creative analysis</h2>
            <button
              onClick={runAnalysis}
              disabled={images.length < 2 || isAnalyzing}
              className="rounded-md bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {isAnalyzing ? `${stageLabels[stage]} ${analysisProgress}%` : "Run analysis"}
            </button>
          </div>

          {images.length < 2 && (
            <p className="mt-2 text-xs text-stone-400">
              Upload at least 2 reference images to run analysis.
            </p>
          )}

          {analysisError && (
            <p className="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
              {analysisError}
            </p>
          )}

          {briefAnalysis && (
            <div className="mt-6 rounded-lg border border-stone-200 bg-white p-5">
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
            <div className="mt-4 rounded-lg border border-stone-200 bg-white p-5">
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
            <div className="mt-4 rounded-lg border border-stone-200 bg-white p-5">
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
            <div className="mt-4 rounded-lg border border-stone-200 bg-white p-5">
              <h3 className="mb-2 text-sm font-semibold text-stone-800">
                Mood board{boardElements ? ` (${boardElements.length} elements)` : ""} saved
              </h3>
              <p className="mb-4 text-xs text-stone-500">Your board is ready to view and export.</p>
              <Link
                href={`/projects/${projectId}/board`}
                className="inline-flex rounded-md bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800"
              >
                Open mood board
              </Link>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
