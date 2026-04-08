"use client";

import type { ReactNode } from "react";

interface AreaSectionProps {
  name: string;
  children: ReactNode;
}

export function AreaSection({ name, children }: AreaSectionProps) {
  return (
    <section className="mb-8">
      <h2 className="text-lg font-semibold text-gray-200 mb-3 px-1">{name}</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {children}
      </div>
    </section>
  );
}
