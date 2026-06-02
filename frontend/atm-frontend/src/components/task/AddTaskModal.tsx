import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Plus, Flag } from 'lucide-react';
import { format } from 'date-fns';
import { api } from '@/api/client';
import type { TaskPriority } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

interface AddTaskModalProps {
  defaultDate?: string;
}

export function AddTaskModal({ defaultDate }: AddTaskModalProps) {
  const today = format(new Date(), 'yyyy-MM-dd');
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState(defaultDate ?? today);
  const [agentId, setAgentId] = useState('');
  const [status, setStatus] = useState('todo');
  const [priority, setPriority] = useState<TaskPriority>('medium');
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: api.getAgents,
  });

  const mutation = useMutation({
    mutationFn: api.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['tasks-all'] });
      queryClient.invalidateQueries({ queryKey: ['tasks-daily'] });
      queryClient.invalidateQueries({ queryKey: ['calendar-monthly'] });
      setOpen(false);
      resetForm();
    },
    onError: (err: any) => {
      setError(err.message ?? '创建失败，请重试');
    },
  });

  function resetForm() {
    setTitle('');
    setDescription('');
    setDate(defaultDate ?? today);
    setAgentId('');
    setStatus('todo');
    setPriority('medium');
    setError('');
  }

  function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    setError('');
    if (!title.trim()) {
      setError('请输入任务标题');
      return;
    }
    if (!agentId) {
      setError('请选择智能体');
      return;
    }
    mutation.mutate({
      title: title.trim(),
      description: description.trim() || undefined,
      status,
      priority,
      task_date: date,
      agent_id: agentId,
    });
  }

  return (
    <Dialog open={open} onOpenChange={(v) => { setOpen(v); if (!v) resetForm(); }}>
      <DialogTrigger asChild>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-1" />
          添加任务
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>添加新任务</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 mt-2">
          <div className="space-y-1">
            <label className="text-sm font-medium">任务标题 *</label>
            <Input
              placeholder="输入任务标题..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              autoFocus
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium">任务描述</label>
            <textarea
              className="w-full min-h-[80px] rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring resize-none"
              placeholder="输入任务描述（可选）..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium">日期 *</label>
              <Input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">优先级</label>
              <select
                className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
                value={priority}
                onChange={(e) => setPriority(e.target.value as TaskPriority)}
              >
                <option value="low">🟢 低</option>
                <option value="medium">🟡 中</option>
                <option value="high">🟠 高</option>
                <option value="critical">🔴 紧急</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium">状态</label>
              <select
                className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="todo">待办</option>
                <option value="ongoing">进行中</option>
                <option value="done">已完成</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">智能体 *</label>
              <select
                className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
                value={agentId}
                onChange={(e) => setAgentId(e.target.value)}
              >
                <option value="">请选择智能体...</option>
                {agents?.map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <div className="flex justify-end gap-2 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
            >
              取消
            </Button>
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? '创建中...' : '创建任务'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
