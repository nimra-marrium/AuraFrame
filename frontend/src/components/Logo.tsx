"use client";

import Link from "next/link";

export default function Logo() {
  return (
    <Link
      href="/dashboard"
      className="font-serif text-lg font-medium tracking-tight text-neutral-900 hover:text-neutral-600"
    >
      AuraFrame
    </Link>
  );
}