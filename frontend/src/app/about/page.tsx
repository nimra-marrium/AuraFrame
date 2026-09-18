"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";

const FEATURES = [
  {
    image: "/about/inspiration.jpg",
    title: "Collect your inspiration",
    description:
      "Bring in scattered references screenshots, photos, Pinterest finds and write a plain language brief describing what you're creating.",
  },
  {
    image: "/about/analysis.jpg",
    title: "Let AI find the pattern",
    description:
      "Five coordinated AI agents analyze your brief and images together, surfacing the colors, tone, and visual patterns already hiding in your references.",
  },
  {
    image: "/about/moodboard.jpg",
    title: "Get a finished mood board",
    description:
      "A complete creative direction palette, typography, imagery guidance rendered onto an editable board you can export and share.",
  },
];

export default function AboutPage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  if (loading || !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-white">
        <p className="text-sm text-neutral-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-white">
      <Navbar />

      <div className="mx-auto max-w-5xl px-8 py-16">
        <h1 className="mb-3 text-center font-serif text-4xl font-medium text-neutral-900">
          About AuraFrame
        </h1>
        <p className="mx-auto mb-14 max-w-lg text-center text-sm text-neutral-500">
          An AI Powered Creative Workspace that turns scattered visual
          inspiration into structured creative direction.
        </p>

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
          {FEATURES.map((feature) => (
            <div
              key={feature.title}
              className="relative overflow-hidden rounded-xl border border-neutral-200 bg-white transition-all duration-300 hover:z-10 hover:scale-[1.03] hover:shadow-lg"
            >
              <div className="aspect-square w-full bg-neutral-100">
                <img
                  src={feature.image}
                  alt=""
                  className="h-full w-full object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = "none";
                  }}
                />
              </div>
              <div className="p-5">
                <h3 className="mb-2 font-serif text-lg font-medium text-neutral-900">
                  {feature.title}
                </h3>
                <p className="text-sm leading-relaxed text-neutral-500">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}