# Agent Task Manager - Component Specification

## Component Hierarchy

```
App
├── Providers (ThemeProvider, QueryProvider)
├── Layout
│   ├── Sidebar
│   │   ├── SidebarHeader (Logo)
│   │   ├── Navigation
│   │   │   ├── NavItem (Dashboard, Agents, Tasks, Calendar)
│   │   └── SidebarFooter (User/Settings)
│   ├── Header
│   │   ├── PageTitle
│   │   ├── GlobalSearch
│   │   ├── ThemeToggle
│   │   └── UserMenu
│   └── PageContainer
│       └── Outlet (Routes)
│           ├── DashboardPage
│           │   ├── CalendarWidget
│           │   │   ├── CalendarHeader
│           │   │   ├── CalendarGrid
│           │   │   │   └── CalendarDay
│           │   └── TodayTasksWidget
│           │       └── KanbanBoard
│           │           └── TaskCard
│           ├── AgentsPage
│           │   ├── AgentList
│           │   │   └── AgentCard
│           │   └── AgentStats
│           ├── AgentDetailPage
│           │   ├── AgentProfile
│           │   ├── AgentStats
│           │   └── AgentTaskHistory
│           ├── TasksPage
│           │   ├── TaskFilters
│           │   └── TaskList
│           │       └── TaskCard
│           └── CalendarPage
│               ├── CalendarHeader
│               ├── CalendarGrid
│               └── DayDetailPanel
```

---

## Props Interfaces

### Layout Components

#### Sidebar Props
```typescript
interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  className?: string;
}

interface NavItemProps {
  to: string;
  icon: LucideIcon;
  label: string;
  badge?: number;
}
```

#### Header Props
```typescript
interface HeaderProps {
  title: string;
  breadcrumbs?: BreadcrumbItem[];
  actions?: React.ReactNode;
}

interface BreadcrumbItem {
  label: string;
  to?: string;
}
```

#### PageContainer Props
```typescript
interface PageContainerProps {
  children: React.ReactNode;
  className?: string;
  fullWidth?: boolean;
}
```

---

### UI Components (shadcn/ui based)

#### Button Props
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'secondary' | 'ghost' | 'outline' | 'destructive';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  loading?: boolean;
  asChild?: boolean;
}
```

#### Card Props
```typescript
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'ghost' | 'outline';
  hoverable?: boolean;
  clickable?: boolean;
}

interface CardHeaderProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
}

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}
```

#### Badge Props
```typescript
interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'secondary' | 'outline' | 'destructive';
  status?: 'todo' | 'ongoing' | 'done';
  size?: 'sm' | 'md';
}
```

#### Avatar Props
```typescript
interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  status?: 'online' | 'offline' | 'busy';
}
```

---

### Domain Components

#### Calendar Props
```typescript
interface CalendarProps {
  year: number;
  month: number;
  data: CalendarDayData[];
  onDayClick: (date: Date) => void;
  onMonthChange: (year: number, month: number) => void;
  selectedDate?: Date;
}

interface CalendarDayData {
  date: Date;
  taskCount: {
    todo: number;
    ongoing: number;
    done: number;
  };
  isCurrentMonth: boolean;
  isToday: boolean;
}

interface CalendarDayProps {
  date: Date;
  taskCount: CalendarDayData['taskCount'];
  isCurrentMonth: boolean;
  isToday: boolean;
  isSelected: boolean;
  onClick: () => void;
}
```

#### TaskCard Props
```typescript
interface TaskCardProps {
  task: Task;
  onClick?: (task: Task) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (task: Task) => void;
  draggable?: boolean;
  onDragStart?: (task: Task) => void;
  compact?: boolean;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'ongoing' | 'done';
  agent: {
    id: string;
    name: string;
    avatar?: string;
  };
  tokenCount: number;
  createdAt: string;
  updatedAt: string;
  dueDate?: string;
}
```

#### KanbanBoard Props
```typescript
interface KanbanBoardProps {
  tasks: Task[];
  onTaskMove?: (taskId: string, newStatus: TaskStatus) => void;
  onTaskClick?: (task: Task) => void;
  loading?: boolean;
}

interface KanbanColumnProps {
  status: TaskStatus;
  title: string;
  tasks: Task[];
  onTaskMove?: (taskId: string, newStatus: TaskStatus) => void;
  onTaskClick?: (task: Task) => void;
}

type TaskStatus = 'todo' | 'ongoing' | 'done';
```

#### AgentStats Props
```typescript
interface AgentStatsProps {
  agentId: string;
  period?: 'day' | 'week' | 'month';
  data?: AgentStatsData;
  loading?: boolean;
}

interface AgentStatsData {
  totalTasks: number;
  completedTasks: number;
  totalTokens: number;
  averageTokensPerTask: number;
  taskDistribution: {
    todo: number;
    ongoing: number;
    done: number;
  };
  dailyActivity: {
    date: string;
    tasks: number;
    tokens: number;
  }[];
}
```

#### AgentCard Props
```typescript
interface AgentCardProps {
  agent: Agent;
  onClick?: (agent: Agent) => void;
  showStats?: boolean;
}

interface Agent {
  id: string;
  name: string;
  description?: string;
  avatar?: string;
  status: 'active' | 'inactive';
  createdAt: string;
  stats?: {
    totalTasks: number;
    completedTasks: number;
    totalTokens: number;
  };
}
```

---

## State Management

### Zustand Store Structure

#### Theme Store
```typescript
interface ThemeStore {
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  resolvedTheme: 'light' | 'dark';
}
```

#### Calendar Store
```typescript
interface CalendarStore {
  selectedDate: Date;
  currentMonth: Date;
  view: 'month' | 'week' | 'day';
  setSelectedDate: (date: Date) => void;
  setCurrentMonth: (date: Date) => void;
  setView: (view: 'month' | 'week' | 'day') => void;
  goToToday: () => void;
  goToPreviousMonth: () => void;
  goToNextMonth: () => void;
}
```

#### Task Store
```typescript
interface TaskStore {
  tasks: Task[];
  filters: TaskFilters;
  loading: boolean;
  error: string | null;
  setFilters: (filters: Partial<TaskFilters>) => void;
  fetchTasks: () => Promise<void>;
  updateTaskStatus: (taskId: string, status: TaskStatus) => Promise<void>;
}

interface TaskFilters {
  status?: TaskStatus;
  agentId?: string;
  dateRange?: { start: Date; end: Date };
  search?: string;
}
```

#### UI Store (Sidebar State)
```typescript
interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}
```

---

## Data Fetching (TanStack Query)

### Query Keys
```typescript
const queryKeys = {
  tasks: {
    all: ['tasks'] as const,
    list: (filters: TaskFilters) => ['tasks', 'list', filters] as const,
    detail: (id: string) => ['tasks', 'detail', id] as const,
    byDate: (date: string) => ['tasks', 'byDate', date] as const,
  },
  agents: {
    all: ['agents'] as const,
    list: () => ['agents', 'list'] as const,
    detail: (id: string) => ['agents', 'detail', id] as const,
    stats: (id: string, period?: string) => ['agents', 'stats', id, period] as const,
  },
  calendar: {
    monthly: (year: number, month: number) => ['calendar', 'monthly', year, month] as const,
    daily: (date: string) => ['calendar', 'daily', date] as const,
  },
};
```

### Query Hooks
```typescript
// Tasks
function useTasks(filters?: TaskFilters);
function useTask(id: string);
function useTasksByDate(date: string);
function useUpdateTaskStatus();

// Agents
function useAgents();
function useAgent(id: string);
function useAgentStats(id: string, period?: string);

// Calendar
function useCalendarMonthly(year: number, month: number);
function useCalendarDaily(date: string);
```

---

## File Structure

```
src/
├── components/
│   ├── ui/                    # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   ├── avatar.tsx
│   │   ├── tooltip.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── skeleton.tsx
│   │   ├── tabs.tsx
│   │   └── calendar.tsx       # shadcn calendar primitive
│   │
│   ├── layout/                # Layout components
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   ├── page-container.tsx
│   │   └── navigation.tsx
│   │
│   ├── calendar/              # Calendar domain components
│   │   ├── calendar-widget.tsx
│   │   ├── calendar-grid.tsx
│   │   ├── calendar-day.tsx
│   │   └── calendar-header.tsx
│   │
│   ├── task/                  # Task domain components
│   │   ├── task-card.tsx
│   │   ├── task-list.tsx
│   │   ├── kanban-board.tsx
│   │   ├── kanban-column.tsx
│   │   └── task-filters.tsx
│   │
│   ├── agent/                 # Agent domain components
│   │   ├── agent-card.tsx
│   │   ├── agent-list.tsx
│   │   ├── agent-stats.tsx
│   │   └── agent-avatar.tsx
│   │
│   └── shared/                # Shared components
│       ├── empty-state.tsx
│       ├── loading-spinner.tsx
│       ├── error-boundary.tsx
│       └── token-display.tsx
│
├── pages/                     # Route pages
│   ├── dashboard.tsx
│   ├── agents.tsx
│   ├── agent-detail.tsx
│   ├── tasks.tsx
│   └── calendar.tsx
│
├── hooks/                     # Custom React hooks
│   ├── use-tasks.ts
│   ├── use-agents.ts
│   ├── use-calendar.ts
│   ├── use-theme.ts
│   └── use-mobile.ts
│
├── stores/                    # Zustand stores
│   ├── theme-store.ts
│   ├── calendar-store.ts
│   ├── task-store.ts
│   └── ui-store.ts
│
├── lib/                       # Utilities
│   ├── utils.ts               # cn() and helpers
│   ├── date-utils.ts
│   ├── format-utils.ts
│   └── constants.ts
│
├── api/                       # API clients
│   ├── client.ts              # Axios/fetch setup
│   ├── tasks-api.ts
│   ├── agents-api.ts
│   └── calendar-api.ts
│
├── types/                     # TypeScript types
│   ├── task.ts
│   ├── agent.ts
│   ├── calendar.ts
│   └── api.ts
│
└── styles/                    # Global styles
    └── globals.css
```

---

## Component Composition Patterns

### Compound Component Pattern
Used for complex components like KanbanBoard:
```typescript
<KanbanBoard tasks={tasks} onTaskMove={handleMove}>
  <KanbanBoard.Column status="todo" title="To Do" />
  <KanbanBoard.Column status="ongoing" title="In Progress" />
  <KanbanBoard.Column status="done" title="Done" />
</KanbanBoard>
```

### Render Props Pattern
Used for flexible list rendering:
```typescript
<TaskList
  tasks={tasks}
  renderItem={(task) => <TaskCard task={task} variant="compact" />}
  emptyState={<EmptyState message="No tasks found" />}
/>
```

### Controlled vs Uncontrolled
- Form inputs: Support both controlled (value + onChange) and uncontrolled (defaultValue)
- Calendar: Controlled component (selectedDate prop)
- Modals: Controlled (open prop)

---

## Performance Considerations

### Memoization
```typescript
// Memoize expensive calculations
const filteredTasks = useMemo(() => 
  tasks.filter(filterFn), 
  [tasks, filters]
);

// Memoize callbacks
const handleTaskClick = useCallback((task: Task) => {
  navigate(`/tasks/${task.id}`);
}, [navigate]);

// Memoize components
const TaskCard = memo(function TaskCard({ task, onClick }: TaskCardProps) {
  // Component implementation
});
```

### Virtualization
For long lists (task history), use virtualization:
```typescript
import { VirtualList } from '@/components/shared/virtual-list';

<VirtualList
  items={tasks}
  renderItem={(task) => <TaskCard task={task} />}
  itemHeight={80}
/>
```

### Code Splitting
```typescript
// Lazy load pages
const AgentsPage = lazy(() => import('./pages/agents'));
const AgentDetailPage = lazy(() => import('./pages/agent-detail'));
```

---

## Error Handling

### Error Boundary
```typescript
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

### API Error Handling
```typescript
const { data, error, isLoading } = useTasks();

if (isLoading) return <Skeleton />;
if (error) return <ErrorMessage error={error} />;
```

### Form Validation
Use Zod for schema validation:
```typescript
const taskSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
  status: z.enum(['todo', 'ongoing', 'done']),
});
```
