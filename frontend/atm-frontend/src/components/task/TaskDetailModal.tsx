import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { Coins, Calendar, ArrowRight, AlertCircle, User, Flag } from 'lucide-react';
import type { Task, TaskStatus, TaskPriority } from '@/types';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';

interface TaskDetailModalProps {
  task: Task | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const statusConfig: Record<TaskStatus, {
  label: string;
  variant: 'default' | 'secondary' | 'destructive' | 'outline';
  bar: string;
}> = {
  TODO:    { label: '待办',  variant: 'outline',   bar: 'bg-muted-foreground/40' },
  ONGOING: { label: '进行中', variant: 'secondary', bar: 'bg-amber-400' },
  DONE:    { label: '已完成', variant: 'default',   bar: 'bg-emerald-500' },
};

function MetaRow({ icon, label, children }: {
  icon: React.ReactNode;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="mt-0.5 text-muted-foreground">{icon}</div>
      <div className="flex-1 min-w-0">
        <p className="text-xs text-muted-foreground mb-0.5">{label}</p>
        <div className="text-sm font-medium">{children}</div>
      </div>
    </div>
  );
}

const priorityConfig: Record<TaskPriority, { label: string; color: string }> = {
  low:      { label: '🟢 低',   color: 'text-slate-500' },
  medium:   { label: '🟡 中',   color: 'text-amber-500' },
  high:     { label: '🟠 高',   color: 'text-orange-500' },
  critical: { label: '🔴 紧急', color: 'text-red-500' },
};

export function TaskDetailModal({ task, open, onOpenChange }: TaskDetailModalProps) {
  if (!task) return null;

  const status = statusConfig[task.status];
  const prio = priorityConfig[task.priority] ?? priorityConfig.medium;
  const formattedDate = format(new Date(task.date), 'yyyy年MM月dd日 (EEEE)', { locale: zhCN });
  const createdAt = format(new Date(task.createdAt), 'yyyy-MM-dd HH:mm');
  const updatedAt = format(new Date(task.updatedAt), 'yyyy-MM-dd HH:mm');

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg p-0 overflow-hidden">
        {/* Colored status bar at the top */}
        <div className={cn('h-1 w-full', status.bar)} />

        <div className="p-6">
          <DialogHeader className="mb-4">
            <div className="flex items-start justify-between gap-3 pr-6">
              <DialogTitle className="text-base font-semibold leading-snug">
                {task.title}
              </DialogTitle>
              <Badge variant={status.variant} className="shrink-0 mt-0.5">
                {status.label}
              </Badge>
            </div>
          </DialogHeader>

          {/* Description */}
          {task.description ? (
            <p className="text-sm text-muted-foreground leading-relaxed mb-5">
              {task.description}
            </p>
          ) : (
            <p className="text-sm text-muted-foreground/50 italic mb-5">暂无描述</p>
          )}

          <Separator className="mb-5" />

          {/* Metadata */}
          <div className="space-y-4">
            <MetaRow icon={<User className="h-4 w-4" />} label="智能体">
              <div className="flex items-center gap-2">
                <Avatar className="h-5 w-5">
                  <AvatarImage src={task.agentAvatar} />
                  <AvatarFallback className="text-xs">
                    {task.agentName?.charAt(0) || 'A'}
                  </AvatarFallback>
                </Avatar>
                <span>{task.agentName}</span>
              </div>
            </MetaRow>

            <MetaRow icon={<Calendar className="h-4 w-4" />} label="任务日期">
              <span>{formattedDate}</span>
              {task.carriedFrom && task.status === 'TODO' && (
                <span className="ml-2 inline-flex items-center gap-1 text-xs text-amber-500 font-normal">
                  <ArrowRight className="h-3 w-3" />
                  顺延自 {task.carriedFrom}
                </span>
              )}
              {task.carriedFrom && task.status === 'ONGOING' && (
                <span className="ml-2 inline-flex items-center gap-1 text-xs text-red-500 font-normal">
                  <AlertCircle className="h-3 w-3" />
                  逾期（原定 {task.carriedFrom}）
                </span>
              )}
            </MetaRow>

            <MetaRow icon={<Flag className="h-4 w-4" />} label="优先级">
              <span className={prio.color}>{prio.label}</span>
            </MetaRow>

            {task.tokens > 0 && (
              <MetaRow icon={<Coins className="h-4 w-4" />} label="Token 消耗">
                <span>{task.tokens.toLocaleString()}</span>
              </MetaRow>
            )}
          </div>

          <Separator className="my-5" />

          {/* Timestamps */}
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>创建于 {createdAt}</span>
            <span>更新于 {updatedAt}</span>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
