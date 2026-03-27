import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { api } from '@/api/client';
import { Layout } from '@/components/layout/sidebar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Skeleton } from '@/components/ui/skeleton';
import { TaskCard } from '@/components/task/TaskCard';
import { ArrowLeft, CheckSquare, Coins, Activity } from 'lucide-react';

export default function AgentDetail() {
  const { id } = useParams();

  const { data: agent, isLoading: agentLoading } = useQuery({
    queryKey: ['agent', id],
    queryFn: () => api.getAgent(id || ''),
    enabled: !!id,
  });

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['agent-stats', id],
    queryFn: () => api.getAgentStats(id || ''),
    enabled: !!id,
  });

  const { data: tasks, isLoading: tasksLoading } = useQuery({
    queryKey: ['agent-tasks', id],
    queryFn: () => api.getTasks({ agent_id: id }),
    enabled: !!id,
  });

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Link to="/agents" className="text-muted-foreground hover:text-foreground">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">智能体详情</h1>
            <p className="text-muted-foreground">查看智能体统计和任务历史</p>
          </div>
        </div>

        {/* Agent info */}
        <Card>
          <CardContent className="p-6">
            {agentLoading ? (
              <div className="flex items-center gap-4">
                <Skeleton className="h-16 w-16 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-32" />
                  <Skeleton className="h-3 w-48" />
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-4">
                <Avatar className="h-16 w-16">
                  <AvatarImage src={agent?.avatar_url} />
                  <AvatarFallback className="text-lg bg-primary/10 text-primary">
                    {agent?.name?.charAt(0) || 'A'}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h2 className="text-xl font-semibold">{agent?.name}</h2>
                  {agent?.description && (
                    <p className="text-muted-foreground">{agent.description}</p>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {statsLoading ? (
            <>
              <Skeleton className="h-24" />
              <Skeleton className="h-24" />
              <Skeleton className="h-24" />
            </>
          ) : (
            <>
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                      <CheckSquare className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">总任务数</p>
                      <p className="text-2xl font-bold">{stats?.totalTasks || 0}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                      <Activity className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">已完成</p>
                      <p className="text-2xl font-bold">{stats?.completedTasks || 0}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                      <Coins className="h-5 w-5 text-amber-600 dark:text-amber-400" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Token 消耗</p>
                      <p className="text-2xl font-bold">{stats?.totalTokens?.toLocaleString() || 0}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>

        {/* Activity chart */}
        <Card>
          <CardHeader>
            <CardTitle>近期活跃度</CardTitle>
          </CardHeader>
          <CardContent>
            {statsLoading ? (
              <Skeleton className="h-32" />
            ) : (
              <div className="grid grid-cols-7 gap-2">
                {stats?.dailyStats?.slice(-14).map((stat) => (
                  <div key={stat.date} className="text-center">
                    <div
                      className="bg-primary/20 rounded-md w-full"
                      style={{ height: `${Math.max(8, stat.tasks * 6)}px` }}
                    />
                    <p className="text-xs text-muted-foreground mt-1">
                      {format(new Date(stat.date), 'MM/dd')}
                    </p>
                  </div>
                ))}
                {(!stats?.dailyStats || stats.dailyStats.length === 0) && (
                  <p className="text-muted-foreground">暂无统计数据</p>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Task history */}
        <Card>
          <CardHeader>
            <CardTitle>任务历史</CardTitle>
          </CardHeader>
          <CardContent>
            {tasksLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-20" />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {tasks?.slice(0, 6).map((task) => (
                  <TaskCard key={task.id} task={task} />
                ))}
                {tasks?.length === 0 && (
                  <p className="text-center text-muted-foreground py-6">暂无任务</p>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
