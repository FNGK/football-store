import { cookies } from "next/headers";
import { InteractivePlan } from "@/components/interactive-plan";
import { LogoutButton } from "@/components/logout-button";
import { SupportBot } from "@/components/support-bot";
import { ACCESS_COOKIE, getApiBase } from "@/lib/auth";
import Link from "next/link";

async function getSession() {
  const jar = await cookies();
  const token = jar.get(ACCESS_COOKIE)?.value;
  if (!token) return null;
  const res = await fetch(`${getApiBase()}/v1/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (!res.ok) return null;
  return res.json() as Promise<{ email: string; tenant_slug: string }>;
}

export default async function DashboardPage() {
  const session = await getSession();

  return (
    <main className="min-h-screen">
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-lg font-semibold">Agentic Marketing Control Plane</h1>
            {session && (
              <p className="text-xs text-muted-foreground">
                {session.email} · {session.tenant_slug}
              </p>
            )}
          </div>
          <nav className="flex items-center gap-4 text-sm text-muted-foreground">
            <Link href="#plan" className="hover:text-foreground">
              Campaign plan
            </Link>
            <Link href="#how-to" className="hover:text-foreground">
              How to use
            </Link>
            <LogoutButton />
          </nav>
        </div>
      </header>

      <div className="mx-auto grid max-w-6xl gap-8 px-6 py-8 lg:grid-cols-3">
        <section id="plan" className="lg:col-span-2">
          <InteractivePlan
            planId="plan-demo-001"
            title="Q2 Cross-Channel Campaign"
            sections={[
              {
                id: "objective",
                title: "Business objective",
                body: "Increase SQL volume 25% while holding blended CPA under target.",
                rationale:
                  "PPC exploratory phase validated 3 commercial keywords with SQL conversion rate above baseline.",
              },
              {
                id: "channels",
                title: "Channel mix",
                body: "Google Ads bottom-funnel tests → SEO topical clusters → retargeting on organic visitors.",
                rationale:
                  "Blueprint sequencing: paid viability first, then authority building, then cross-channel optimization.",
              },
              {
                id: "budget",
                title: "Budget guardrails",
                body: "Minimum liquidity: 50 conversions/month per ad set. MAB Thompson Sampling for creative rotation.",
                rationale:
                  "Prevents algorithmic starvation from over-fragmented micro-campaigns.",
              },
            ]}
          />
        </section>

        <aside id="support" className="space-y-6">
          <SupportBot />
        </aside>
      </div>

      <section id="how-to" className="mx-auto max-w-6xl px-6 pb-12">
        <h2 className="mb-4 text-xl font-semibold">How to use this platform</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <HowToCard
            title="Monitor agents"
            body="Watch LangGraph workflow status, Safe Mode triggers, and token budgets on the control plane API."
          />
          <HowToCard
            title="Adjust budgets"
            body="Set MVG caps, minimum liquidity per campaign, and AI CMO overlap rules."
          />
          <HowToCard
            title="Control surfaces"
            body="Edit Interactive Plans; use Undo before Approve."
          />
        </div>
      </section>
    </main>
  );
}

function HowToCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <h3 className="font-medium">{title}</h3>
      <p className="mt-2 text-sm text-muted-foreground">{body}</p>
    </div>
  );
}
