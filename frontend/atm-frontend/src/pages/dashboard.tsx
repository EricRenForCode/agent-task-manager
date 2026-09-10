import { useQuery } from '@tanstack/react-query';
import { api } from '@/api/client';
import { Layout } from '@/components/layout/sidebar';
import { KanbanBoard } from '@/components/task/KanbanBoard';
import { AddTaskModal } from '@/components/task/AddTaskModal';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
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
  const { data: agents, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: api.getAgents,
  });

  const { data: allTasks, isLoading: allTasksLoading } = useQuery({
    queryKey: ['tasks-all'],
    queryFn: () => api.getTasks(),
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
              title="待办任务"
              value={allTasks?.filter(t => t.status === 'TODO').length || 0}
              icon={Calendar}
              description="待处理"
            />
            <StatCard
              title="总Token消耗"
              value={(allTasks?.reduce((sum, t) => sum + (t.tokens || 0), 0) || 0).toLocaleString()}
              icon={Coins}
              description="tokens"
            />
          </>
        )}
      </div>

      {/* Kanban Board — full width */}
      <Card className="h-full">
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <CardTitle className="text-lg">任务看板 (全部任务)</CardTitle>
          <AddTaskModal defaultDate={new Date().toISOString().slice(0, 10)} />
        </CardHeader>
        <CardContent>
          {allTasksLoading ? (
            <div className="grid grid-cols-3 gap-4">
              <Skeleton className="h-96" />
              <Skeleton className="h-96" />
              <Skeleton className="h-96" />
            </div>
          ) : (
            <KanbanBoard tasks={allTasks || []} />
          )}
        </CardContent>
      </Card>
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
