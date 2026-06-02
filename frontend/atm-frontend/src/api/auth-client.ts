/**
 * API client with automatic JWT token refresh.
 *
 * Lifecycle:
 *   1. All requests include Authorization: Bearer <access_token>
 *   2. On 401, client queues the request, attempts a single refresh,
 *      and retries all queued requests with the new token.
 *   3. Concurrent 401s are coalesced into one refresh call.
 *   4. If refresh fails, all queued requests reject and user must re-login.
 */

import { API_BASE } from '@/api/config';

// ── Token storage ────────────────────────────────────────────────────
const TOKEN_KEY = '***';

interface TokenStore {
  accessToken: string | null;
  refreshToken: string | null;
}

function loadTokens(): TokenStore {
  try {
    const raw = localStorage.getItem(TOKEN_KEY);
    return raw ? JSON.parse(raw) : { accessToken: null, refreshToken: null };
  } catch {
    return { accessToken: null, refreshToken: null };
  }
}

function saveTokens(tokens: TokenStore): void {
  localStorage.setItem(TOKEN_KEY, JSON.stringify(tokens));
}

function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY);
}

let tokenStore: TokenStore = loadTokens();

export function getAccessToken(): string | null {
  return tokenStore.accessToken;
}

export function setTokens(accessToken: string, refreshToken: string): void {
  tokenStore = { accessToken, refreshToken };
  saveTokens(tokenStore);
}

export function logout(): void {
  tokenStore = { accessToken: null, refreshToken: null };
  clearTokens();
  window.dispatchEvent(new CustomEvent('bp:auth:logout'));
}

export function isAuthenticated(): boolean {
  return tokenStore.accessToken !== null;
}

// ── Refresh queue / coalescing ───────────────────────────────────────
type QueueEntry = { resolve: (value: string) => void; reject: (reason: unknown) => void };

let refreshPromise: Promise<string> | null = null;
let refreshQueue: QueueEntry[] = [];

async function refreshAccessToken(): Promise<string> {
  if (!tokenStore.refreshToken) throw new Error('No refresh token available');
  const resp = await fetch(`${API_BASE}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: tokenStore.refreshToken }),
  });
  if (!resp.ok) throw new Error(`Refresh failed (${resp.status}): ${await resp.text()}`);
  return (await resp.json()).access_token;
}

function enqueueRefresh(): Promise<string> {
  if (refreshPromise) {
    return new Promise<string>((resolve, reject) => { refreshQueue.push({ resolve, reject }); });
  }
  refreshPromise = refreshAccessToken()
    .then((newAccessToken) => {
      tokenStore.accessToken = newAccessToken;
      saveTokens(tokenStore);
      const queue = refreshQueue; refreshQueue = []; refreshPromise = null;
      for (const entry of queue) entry.resolve(newAccessToken);
      return newAccessToken;
    })
    .catch((err) => {
      const queue = refreshQueue; refreshQueue = []; refreshPromise = null;
      logout();
      for (const entry of queue) entry.reject(err);
      throw err;
    });
  return refreshPromise;
}

// ── Core fetch wrapper ───────────────────────────────────────────────
export class ApiError extends Error {
  status: number; detail: unknown;
  constructor(status: number, detail: unknown) {
    const msg = typeof detail === 'string' ? detail : JSON.stringify(detail);
    super(msg);
    this.name = 'ApiError'; this.status = status; this.detail = detail;
  }
}

async function fetchWithAuth(
  endpoint: string, options: RequestInit = {}, retryOn401 = true,
): Promise<Response> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  if (tokenStore.accessToken) headers['Authorization'] = `Bearer ${tokenStore.accessToken}`;

  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });

  if (response.status === 401 && retryOn401 && tokenStore.refreshToken) {
    try {
      const newToken = await enqueueRefresh();
      headers['Authorization'] = `Bearer ${newToken}`;
      return await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    } catch { /* propagate original 401 */ }
  }
  return response;
}

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const resp = await fetchWithAuth(endpoint, options);
  if (!resp.ok) {
    let detail: unknown;
    try { detail = await resp.json(); } catch { detail = await resp.text(); }
    throw new ApiError(resp.status, detail);
  }
  if (resp.status === 204) return undefined as T;
  return resp.json();
}

// ── Auth endpoints (no auth header needed) ───────────────────────────
export const auth = {
  async login(username: string, password: string): Promise<void> {
    const resp = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!resp.ok) throw new ApiError(resp.status, await resp.text());
    const data = await resp.json();
    setTokens(data.access_token, data.refresh_token);
  },
  async getMe() { return fetchApi('/auth/me'); },
};
