/**
 * Shared API client. Every page/component talks to the backend through
 * this file, never with raw fetch() calls scattered around - same
 * principle as the backend's core/database.py being the one shared
 * connection point.
 *
 * Automatically attaches the Authorization: Bearer <token> header when
 * a token is available, so individual API calls don't need to think
 * about auth at all.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    (headers as Record<string, string>)["authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON - keep default message
    }
    throw new ApiError(detail, response.status);
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response as unknown as T;
}

export const api = {
  get: <T,>(path: string, token?: string | null) =>
    request<T>(path, { method: "GET" }, token),

  post: <T,>(path: string, body: unknown, token?: string | null) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body) }, token),

  put: <T,>(path: string, body: unknown, token?: string | null) =>
    request<T>(path, { method: "PUT", body: JSON.stringify(body) }, token),
};

/** Separate helper for file uploads, since those need multipart/form-data,
 *  not JSON - mirrors the backend's image module being the one exception
 *  to the JSON-everywhere pattern. */
export async function uploadFile(
  path: string,
  formData: FormData,
  token?: string | null
) {
  const headers: HeadersInit = {};
  if (token) {
    (headers as Record<string, string>)["authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    body: formData,
    headers,
  });

  if (!response.ok) {
    let detail = `Upload failed with status ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // ignore
    }
    throw new ApiError(detail, response.status);
  }

  return response.json();
}