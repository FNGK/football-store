"use client";

import { Suspense, FormEvent, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";

function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      let message = "Login failed";
      try {
        const data = await res.json();
        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (data.detail === "Not Found") {
          message =
            "API unreachable or misconfigured. Start the API (port 8000) and ensure NEXT_PUBLIC_API_URL is set.";
        }
      } catch {
        message = "Cannot reach the login service. Is the API running on port 8000?";
      }
      setError(message);
      return;
    }
    router.push(params.get("from") ?? "/");
    router.refresh();
  };

  return (
    <form
      onSubmit={onSubmit}
      className="w-full max-w-md space-y-4 rounded-lg border border-border bg-card p-8 shadow-sm"
    >
      <h1 className="text-xl font-semibold">Sign in</h1>
      <p className="text-sm text-muted-foreground">
        Use your organization credentials.
      </p>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <label className="block space-y-1 text-sm">
        <span>Email</span>
        <input
          type="email"
          required
          className="w-full rounded-md border border-border px-3 py-2"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </label>
      <label className="block space-y-1 text-sm">
        <span>Password</span>
        <input
          type="password"
          required
          minLength={8}
          className="w-full rounded-md border border-border px-3 py-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <Button type="submit" className="w-full">
        Sign in
      </Button>
    </form>
  );
}

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-muted/30 p-6">
      <Suspense fallback={<p className="text-sm">Loading…</p>}>
        <LoginForm />
      </Suspense>
    </main>
  );
}
