import { SahayResponse, ToolDefinition, TTEProposal } from '../types';

const API_BASE = '/api/v1';

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
      throw new Error('Unable to connect to Sahay backend. Please check that the server is running on http://localhost:8000 and try again.');
    }
    throw err;
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch('/health');
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
