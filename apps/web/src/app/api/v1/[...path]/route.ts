import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { ACCESS_COOKIE, getApiBase } from "@/lib/auth";

async function proxy(request: NextRequest, path: string[]) {
  const jar = await cookies();
  const token = jar.get(ACCESS_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });
  }
  const target = `${getApiBase()}/v1/${path.join("/")}${request.nextUrl.search}`;
  const headers = new Headers(request.headers);
  headers.set("Authorization", `Bearer ${token}`);
  headers.delete("host");
  const init: RequestInit = {
    method: request.method,
    headers,
    cache: "no-store",
  };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.text();
  }
  const res = await fetch(target, init);
  const body = await res.text();
  return new NextResponse(body, {
    status: res.status,
    headers: { "Content-Type": res.headers.get("Content-Type") ?? "application/json" },
  });
}

export async function GET(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  return proxy(req, (await ctx.params).path);
}
export async function POST(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  return proxy(req, (await ctx.params).path);
}
