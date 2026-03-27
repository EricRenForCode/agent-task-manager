import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { format } from 'date-fns';
import { api } from '@/api/client';
import { Layout } from '@/components/layout/sidebar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import type { TaskStatus } from '@/types';

const statusOptions: { value: string; label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }[] = [
  { value: '', label: '全部状态', variant: 'outline' },
  { value: 'TODO', label: '待办', variant: 'outline' },
  { value: 'ONGOING', label: '进行中', variant: 'secondary' },
  { value: 'DONE', label: '已完成', variant: 'default' },
];

const statusBadgeVariant = (status: TaskStatus) => {
  switch (status) {
    case 'TODO':
      return 'outline';
    case 'ONGOING':
      return 'secondary';
    case 'DONE':
      return 'default';
    default:
      return 'outline';
  }
};

export default function Tasks() {
  const [dateFilter, setDateFilter] = useState('');
  const [agentFilter, setAgentFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: api.getAgents,
  });

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', dateFilter, agentFilter, statusFilter],
    queryFn: () => api.getTasks({
      date: dateFilter || undefined,
      agent_id: agentFilter || undefined,
      status: statusFilter || undefined,
    }),
  });

  const filteredTasks = tasks?.filter((task) => {
    if (!searchQuery) return true;
    return (
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">任务列表</h1>
          <p className="text-muted-foreground">查看和筛选所有任务</p>
        </div>

        {/* Filters */}
        <Card>
          <CardContent className="p-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Input
                type="text"
                placeholder="搜索任务标题或描述..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <Input
                type="date"
                value={dateFilter}
                onChange={(e) => setDateFilter(e.target.value)}
              />
              <select
                className="h-10 rounded-md border border-input bg-background px-3 text-sm"
                value={agentFilter}
                onChange={(e) => setAgentFilter(e.target.value)}
              >
                <option value="">全部智能体</option>
                {agents?.map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name}
                  </option>
                ))}
              </select>
              <select
                className="h-10 rounded-md border border-input bg-background px-3 text-sm"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </CardContent>
        </Card>

        {/* Tasks Table */}
        <Card>
          <CardHeader>
            <CardTitle>所有任务</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Skeleton key={i} className="h-12" />
                ))}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3">任务</th>
                      <th className="text-left p-3">智能体</th>
                      <th className="text-left p-3">状态</th>
                      <th className="text-right p-3">Token</th>
                      <th className="text-left p-3">日期</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredTasks?.map((task) => (
                      <tr key={task.id} className="border-b hover:bg-muted/50">
                        <td className="p-3">
                          <div>
                            <p className="font-medium">{task.title}</p>
                            {task.description && (
                              <p className="text-xs text-muted-foreground line-clamp-1">
                                {task.description}
                              </p>
                            )}
                          </div>
                        </td>
                        <td className="p-3">{task.agentName}</td>
                        <td className="p-3">
                          <Badge variant={statusBadgeVariant(task.status)}>
                            {task.status === 'TODO' ? '待办' : task.status === 'ONGOING' ? '进行中' : '已完成'}
                          </Badge>
                        </td>
                        <td className="p-3 text-right">{task.tokens.toLocaleString()}</td>
                        <td className="p-3">{format(new Date(task.date), 'yyyy-MM-dd')}</td>
                      </tr>
                    ))}
                    {filteredTasks?.length === 0 && (
                      <tr>
                        <td colSpan={5} className="p-8 text-center text-muted-foreground">
                          暂无任务
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
