import type { Agent, Task, TaskStatus, DailyCalendar, MonthlyCalendar, AgentStats, DashboardStats } from '@/types';
import { API_BASE } from '@/api/config';

function normalizeTask(t: any): Task {
  const taskDate = t.task_date || t.date || '';
  const originalDate = t.original_date || taskDate;
  return {
    id: t.id,
    title: t.title,
    description: t.description,
    status: (t.status as string).toUpperCase() as TaskStatus,
    agentId: t.agent_id || '',
    agentName: t.agent_name || '',
    tokens: t.tokens_consumed ?? 0,
    date: taskDate,
    carriedFrom: originalDate !== taskDate ? originalDate : undefined,
    createdAt: t.created_at || '',
    updatedAt: t.updated_at || '',
  };
}

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
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

  getDailyTasks: async (date: string) => {
    const raw = await fetchApi<any>(`/calendar/daily?date=${date}`);
    const tasks: DailyCalendar['tasks'] = {};
    for (const [key, list] of Object.entries(raw.tasks as Record<string, any[]>)) {
      tasks[key] = list.map(normalizeTask);
    }
    return { ...raw, tasks } as DailyCalendar;
  },

  // Tasks
  getTasks: async (params?: { date?: string; agent_id?: string; status?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.date) searchParams.append('date', params.date);
    if (params?.agent_id) searchParams.append('agent_id', params.agent_id);
    if (params?.status) searchParams.append('status', params.status);
    const raw = await fetchApi<any[]>(`/tasks?${searchParams.toString()}`);
    return raw.map(normalizeTask);
  },

  // Agents
  getAgents: () => fetchApi<Agent[]>('/agents'),

  getAgent: (id: string) => fetchApi<Agent>(`/agents/${id}`),

  getAgentStats: (id: string) => fetchApi<AgentStats>(`/agents/${id}/stats`),

  // Create task
  createTask: (data: {
    title: string;
    description?: string;
    status?: string;
    task_date: string;
    agent_id: string;
    tokens_consumed?: number;
  }) =>
    fetchApi<any>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Stats
  getDashboardStats: () => fetchApi<DashboardStats>('/stats/dashboard'),
};

export { ApiError };