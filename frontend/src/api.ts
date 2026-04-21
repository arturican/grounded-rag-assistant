import type { AskRequest, AskResponse, HealthResponse, IndexRequest, IndexResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(`API ${status}: ${detail}`);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

function extractErrorDetail(responseText: string): string {
  if (!responseText) {
    return "No details returned by backend.";
  }

  try {
    const parsed = JSON.parse(responseText) as { detail?: unknown };
    if (typeof parsed.detail === "string" && parsed.detail.trim().length > 0) {
      return parsed.detail;
    }
  } catch {
    // Keep raw body fallback for non-JSON errors.
  }

  return responseText;
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const responseText = await response.text();
    throw new ApiError(response.status, extractErrorDetail(responseText));
  }

  return (await response.json()) as T;
}

export function getHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>("/health");
}

export function postIndex(payload: IndexRequest): Promise<IndexResponse> {
  return requestJson<IndexResponse>("/index", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postAsk(payload: AskRequest): Promise<AskResponse> {
  return requestJson<AskResponse>("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
