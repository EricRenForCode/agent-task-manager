# Agent Task Manager - Component Inventory

## Layout Components
- **Sidebar**: Main navigation container
  - SidebarHeader (logo, app name)
  - SidebarNav (primary links)
  - SidebarFooter (user/profile settings)
- **Header**: Top bar with page title, actions, search
- **PageContainer**: Standard page wrapper with padding/max-width
- **Breadcrumbs**: Optional navigation trail
- **MobileNav**: Collapsible mobile sidebar/overlay

## UI Components (shadcn/ui based)
- **Button**: Primary/secondary/ghost/outline/destructive
- **Card**: Default/hoverable/outline with header/body/footer
- **Badge**: Status badges for task state
- **Avatar**: Agent/user avatar with status indicator
- **Tooltip**: Helpful hints for icons/actions
- **DropdownMenu**: Actions menu for cards
- **Dialog/Modal**: Confirmations, detail views
- **Input**: Text input
- **Select**: Dropdown selector (status/agent)
- **Tabs**: Page sub-sections (e.g., agent stats)
- **Popover**: Contextual overlays
- **Skeleton**: Loading states
- **Switch**: Theme toggle
- **Progress**: Token usage progress
- **Separator**: Section dividers
- **Toast**: Notifications
- **Calendar (shadcn)**: Base calendar primitive

## Data Display Components
- **StatCard**: KPI overview cards
- **TokenDisplay**: Token count + icon
- **EmptyState**: No data placeholder
- **Table**: Task/agent lists
- **Pagination**: For long lists
- **FilterBar**: Search + filter controls

## Domain Components

### Calendar
- **CalendarWidget**: Embedded monthly view
- **CalendarHeader**: Month navigation + actions
- **CalendarGrid**: Grid of days
- **CalendarDay**: Single day cell with status dots
- **DayDetailPanel**: Daily task summary panel

### Tasks
- **TaskCard**: Main task display card
- **TaskList**: List view of tasks
- **TaskFilters**: Status/agent/date filters
- **KanbanBoard**: Board container
- **KanbanColumn**: Column for status
- **TaskStatusBadge**: Colored status label
- **TaskMeta**: Agent + token info row

### Agents
- **AgentCard**: Agent summary
- **AgentList**: Grid/list of agents
- **AgentStats**: Charts + KPIs
- **AgentProfile**: Avatar + bio + status
- **AgentTaskHistory**: Recent tasks for agent

## Page Components
- **DashboardPage**: Calendar + today’s tasks
- **AgentsPage**: Agent list + filters
- **AgentDetailPage**: Profile + stats + tasks
- **TasksPage**: Full task list + filters
- **CalendarPage**: Full screen calendar view

## Shared/Utility Components
- **LoadingSpinner**
- **ErrorBoundary**
- **ErrorMessage**
- **SearchInput**
- **ThemeToggle**
- **StatusDot** (for calendar/day)
- **IconButton**

---

### Required by Brief (Explicit)
- Layout: **Sidebar, Header, PageContainer**
- UI: **Button, Card, Badge, Avatar, Tooltip**
- Domain: **Calendar, TaskCard, KanbanBoard, AgentStats**
