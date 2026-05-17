export const ACCESS_COOKIE = "amp_access_token";
export const REFRESH_COOKIE = "amp_refresh_token";

export function getApiBase(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
}
