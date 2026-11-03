export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, { ...init, headers: { ...(init?.body instanceof FormData ? {} : { "Content-Type": "application/json" }), ...init?.headers }, cache: "no-store" });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try { const data = await response.json(); message = data.detail || message; } catch {}
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}
