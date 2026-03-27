export interface Agent {
  id: string;
  name: string;
  description?: string;
  avatar_url?: string;
  is_active: boolean;
  api_key: string;
  created_at: string;
  updated_at: string;
  stats?: {
    totalTasks: number;
    completedTasks: number;
    totalTokens: number;
  };
}

export type TaskStatus = 'TODO' | 'ONGOING' | 'DONE';

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  agentId: string;
  agentName: string;
  agentAvatar?: string;
  tokens: number;
  date: string;
  createdAt: string;
  updatedAt: string;
}

export interface CalendarDay {
  date: string;
  has_tasks: boolean;
  task_count: {
    todo: number;
    ongoing: number;
    done: number;
  };
  total_tokens: number;
}

export interface DailyCalendar {
  date: string;
  tasks: Record<string, Task[]>;
  summary: {
    total_tasks: number;
    total_tokens: number;
    agents_involved: string[];
  };
}

export interface MonthlyCalendar {
  year: number;
  month: number;
  days: CalendarDay[];
}

export interface AgentStats {
  agentId: string;
  totalTasks: number;
  completedTasks: number;
  totalTokens: number;
  dailyStats: {
    date: string;
    tasks: number;
    tokens: number;
  }[];
}

export interface DashboardStats {
  totalAgents: number;
  totalTasks: number;
  todayTasks: number;
  todayTokens: number;
}