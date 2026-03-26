import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { api } from '@/api/client';
import { Layout } from '@/components/layout/sidebar';
import { CalendarWidget } from '@/components/calendar/CalendarWidget';
import { KanbanBoard } from '@/components/task/KanbanBoard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useCalendarStore } from '@/stores';
import { Users, CheckSquare, Coins, Calendar } from 'lucide-react';

function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  description 
}: { 
  title: string; 
  value: string | number; 
  icon: React.ElementType;
  description?: string;
}) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold mt-1">{value}</p>
            {description && (
              <p className="text-xs text-muted-foreground mt-1">{description}</p>
            )}
          </div>
          <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
            <Icon className="h-6 w-6 text-primary" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function DashboardContent() {
  const { selectedDate } = useCalendarStore();

  const { data: agents, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: api.getAgents,
  });

  const { data: allTasks, isLoading: allTasksLoading } = useQuery({
    queryKey: ['tasks-all'],
    queryFn: () => api.getTasks(),
  });

  // Fetch calendar data for current month
  const { data: calendarData } = useQuery({
    queryKey: ['calendar-monthly', selectedDate.getFullYear(), selectedDate.getMonth() + 1],
    queryFn: () => api.getMonthlyCalendar(selectedDate.getFullYear(), selectedDate.getMonth() + 1),
  });

  // Fetch today's tasks
  const { data: todayTasks, isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks-daily', format(selectedDate, 'yyyy-MM-dd')],
    queryFn: () => api.getDailyTasks(format(selectedDate, 'yyyy-MM-dd')),
  });

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {agentsLoading || allTasksLoading ? (
          <>
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
          </>
        ) : (
          <>
            <StatCard 
              title="智能体数量" 
              value={agents?.length || 0} 
              icon={Users}
              description="活跃智能体"
            />
            <StatCard 
              title="总任务数" 
              value={allTasks?.length || 0} 
              icon={CheckSquare}
              description="所有时间"
            />
            <StatCard 
              title="今日任务" 
              value={todayTasks?.length || 0} 
              icon={Calendar}
              description={format(selectedDate, 'MM月dd日')}
            />
            <StatCard 
              title="今日Token消耗" 
              value={(todayTasks?.reduce((sum, t) => sum + t.tokens, 0) || 0).toLocaleString()} 
              icon={Coins}
              description="tokens"
            />
          </>
        )}
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <div className="lg:col-span-1">
          <CalendarWidget 
            days={calendarData?.days} 
            className="h-fit"
          />
        </div>

        {/* Kanban Board */}
        <div className="lg:col-span-2">
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="text-lg">
                {format(selectedDate, 'yyyy年MM月dd日')} 任务看板
              </CardTitle>
            </CardHeader>
            <CardContent>
              {tasksLoading ? (
                <div className="grid grid-cols-3 gap-4">
                  <Skeleton className="h-96" />
                  <Skeleton className="h-96" />
                  <Skeleton className="h-96" />
                </div>
              ) : (
                <KanbanBoard tasks={todayTasks || []} />
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <Layout>
      <DashboardContent />
    </Layout>
  );
}