import { SahayResponse, ToolDefinition, TTEProposal } from '../types';

const metaEnv = (import.meta as any).env || {};
const isLocalhost = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

const getBaseUrl = (): string => {
  if (metaEnv.VITE_API_URL) {
    return String(metaEnv.VITE_API_URL).replace(/\/$/, '');
  }
  if (isLocalhost || metaEnv.DEV) {
    return 'http://localhost:8002';
  }
  if (typeof window !== 'undefined' && window.location.origin) {
    return window.location.origin;
  }
  return '';
};

const BASE_URL = getBaseUrl();
const API_BASE = BASE_URL ? `${BASE_URL}/api/v1` : '/api/v1';

export async function sendChatQuery(
  message: string,
  context: Record<string, any> = {},
  conversationId?: string
): Promise<SahayResponse> {
  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_context: context,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      let detail = `Server error ${response.status}`;
      try {
        const errJson = await response.json();
        detail = errJson.detail || errJson.message || detail;
      } catch {
        // Fallback
      }
      throw new Error(detail);
    }

    return await response.json();
  } catch (err: any) {
    if (err.name === 'TypeError' || err.message?.includes('fetch') || err.message?.includes('Failed to fetch')) {
      throw new Error(`Unable to connect to Sahay backend. Please ensure the backend server is running on ${BASE_URL} and try again.`);
    }
    throw err;
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/health`);
    if (res.ok) {
      const data = await res.json();
      return data.status === 'ok' || data.status === 'healthy';
    }
  } catch (e) {
    return false;
  }
  return false;
}

export async function fetchTools(): Promise<ToolDefinition[]> {
  const response = await fetch(`${API_BASE}/tools`);
  if (!response.ok) {
    throw new Error('Failed to fetch tools registry');
  }
  return response.json();
}

export async function proposeTTETool(tool_name: string, problem_context: string, generated_code: string): Promise<TTEProposal> {
  const params = new URLSearchParams({
    tool_name,
    problem_context,
    generated_code,
  });
  const response = await fetch(`${API_BASE}/tte/propose?${params.toString()}`, {
    method: 'POST',
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Proposal failed' }));
    throw new Error(err.detail || 'Failed to submit proposal');
  }
  return response.json();
}

export async function approveTTETool(proposal_id: string): Promise<ToolDefinition> {
  const response = await fetch(`${API_BASE}/tte/approve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ proposal_id, approved_by: 'ADMIN_USER' }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Approval failed' }));
    throw new Error(err.detail || 'Failed to approve proposal');
  }
  return response.json();
}
