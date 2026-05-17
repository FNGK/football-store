import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { ACCESS_COOKIE, getApiBase } from "@/lib/auth";

export async function GET() {
  const jar = await cookies();
  const token = jar.get(ACCESS_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });
  }
  const res = await fetch(`${getApiBase()}/v1/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
