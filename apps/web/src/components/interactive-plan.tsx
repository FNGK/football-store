"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export type PlanSection = {
  id: string;
  title: string;
  body: string;
  rationale?: string;
};

type InteractivePlanProps = {
  planId: string;
  title: string;
  sections: PlanSection[];
  onApprove?: (sections: PlanSection[]) => void;
};

export function InteractivePlan({
  planId,
  title,
  sections: initial,
  onApprove,
}: InteractivePlanProps) {
  const [history, setHistory] = useState<PlanSection[][]>([initial]);
  const [index, setIndex] = useState(0);
  const sections = history[index];

  const updateSection = (id: string, body: string) => {
    const next = sections.map((s) => (s.id === id ? { ...s, body } : s));
    setHistory((h) => [...h.slice(0, index + 1), next]);
    setIndex((i) => i + 1);
  };

  const undo = () => {
    if (index > 0) setIndex((i) => i - 1);
  };

  return (
    <article className="rounded-lg border border-border bg-card p-6 shadow-sm">
      <header className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">{title}</h2>
          <p className="text-sm text-muted-foreground">Plan ID: {planId}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={undo} disabled={index === 0}>
            Undo
          </Button>
          <Button size="sm" onClick={() => onApprove?.(sections)}>
            Approve plan
          </Button>
        </div>
      </header>

      <div className="space-y-6">
        {sections.map((section) => (
          <section key={section.id} className="space-y-2">
            <h3 className="font-medium">{section.title}</h3>
            <textarea
              className="min-h-[100px] w-full rounded-md border border-border bg-background p-3 text-sm"
              value={section.body}
              onChange={(e) => updateSection(section.id, e.target.value)}
            />
            {section.rationale && (
              <details className="rounded-md bg-muted p-3 text-sm">
                <summary className="cursor-pointer font-medium">
                  Explainable rationale
                </summary>
                <p className="mt-2 text-muted-foreground">{section.rationale}</p>
              </details>
            )}
          </section>
        ))}
      </div>
    </article>
  );
}
