/**
 * api.js — Thin fetch wrapper for the SentinelAI backend.
 *
 * All paths use the /api prefix which Vite's dev-server proxy
 * strips before forwarding to http://127.0.0.1:8000.
 *
 * GET /api/alerts     → GET http://127.0.0.1:8000/alerts
 * PATCH /api/alerts/X → PATCH http://127.0.0.1:8000/alerts/X
 */

const BASE = '/api';

async function apiFetch(path, options = {}) {
  const resp = await fetch(`${BASE}${path}`, options);
  if (!resp.ok) {
    const body = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(body.detail || `HTTP ${resp.status}`);
  }
  return resp.json();
}

/**
 * Fetch alerts list.
 * @param {Object} params - Optional query params (limit, severity, priority, status, prediction)
 */
export function fetchAlerts(params = {}) {
  const merged = { limit: 500, ...params };
  // Strip empty/falsy values so the API doesn't receive empty strings as filters
  Object.keys(merged).forEach(k => {
    if (merged[k] === '' || merged[k] === null || merged[k] === undefined) {
      delete merged[k];
    }
  });
  const qs = new URLSearchParams(merged).toString();
  return apiFetch(`/alerts/${qs ? '?' + qs : ''}`);
}

/**
 * Fetch a single alert by ID.
 */
export function fetchAlert(id) {
  return apiFetch(`/alerts/${encodeURIComponent(id)}`);
}

/**
 * Update an alert's status.
 * Valid statuses: Open | Acknowledged | Investigating | Resolved | False Positive
 */
export function patchAlertStatus(id, status) {
  return apiFetch(`/alerts/${encodeURIComponent(id)}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
}
