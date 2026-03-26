export interface Agent {
  id: string;
  name: string;
  avatar?: string;
  description?: string;
  totalTokens: number;
  taskCount: number;
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