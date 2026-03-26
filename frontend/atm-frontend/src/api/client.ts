import { Agent, Task, MonthlyCalendar, AgentStats, DashboardStats } from '@/types';

const API_BASE = 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await response.text());
  }

  return response.json();
}

export const api = {
  // Calendar
  getMonthlyCalendar: (year: number, month: number) =>
    fetchApi<MonthlyCalendar>(`/calendar/monthly?year=${year}&month=${month}`),

  getDailyTasks: (date: string) =>
    fetchApi<Task[]>(`/calendar/daily?date=${date}`),

  // Tasks
  getTasks: (params?: { date?: string; agent_id?: string; status?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.date) searchParams.append('date', params.date);
    if (params?.agent_id) searchParams.append('agent_id', params.agent_id);
    if (params?.status) searchParams.append('status', params.status);
    return fetchApi<Task[]>(`/tasks?${searchParams.toString()}`);
  },

  // Agents
  getAgents: () => fetchApi<Agent[]>('/agents'),

  getAgent: (id: string) => fetchApi<Agent>(`/agents/${id}`),

  getAgentStats: (id: string) => fetchApi<AgentStats>(`/agents/${id}/stats`),

  // Stats
  getDashboardStats: () => fetchApi<DashboardStats>('/stats/dashboard'),
};

export { ApiError };