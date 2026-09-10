import type { Task, TaskStatus, TaskPriority } from '@/types';
import { format } from 'date-fns';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Coins, ArrowRight, AlertCircle, Calendar, Folder, MapPin, FileText, ArrowUpRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TaskCardProps {
  task: Task;
  className?: string;
  onClick?: (task: Task) => void;
}

const statusConfig: Record<TaskStatus, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }> = {
  TODO: { label: '待办', variant: 'outline' },
  ONGOING: { label: '进行中', variant: 'secondary' },
  DONE: { label: '已完成', variant: 'default' },
};

const priorityConfig: Record<TaskPriority, { label: string; color: string }> = {
  low: { label: '低', color: 'text-slate-400' },
  medium: { label: '中', color: 'text-amber-400' },
  high: { label: '高', color: 'text-orange-500' },
  critical: { label: '紧急', color: 'text-red-500' },
};

export function TaskCard({ task, className, onClick }: TaskCardProps) {
  const status = statusConfig[task.status];
  const prio = priorityConfig[task.priority] ?? priorityConfig.medium;
  const ctx = task.context;

  return (
    <Card
      className={cn("cursor-pointer hover:shadow-md transition-shadow", className)}
      onClick={() => onClick?.(task)}
    >
      <CardContent className="p-4">
        {/* Header: title + status/priority */}
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <h4 className="font-medium text-sm truncate">{task.title}</h4>
          </div>
          <div className="flex flex-col items-end gap-1 shrink-0">
            <Badge variant={status.variant} className="text-xs">
              {status.label}
            </Badge>
            <span className={cn('text-xs font-medium', prio.color)}>
              {prio.label}
            </span>
            {task.carriedFrom && task.status === 'TODO' && (
              <span className="flex items-center gap-0.5 text-xs text-amber-500">
                <ArrowRight className="h-3 w-3" />
                {task.carriedFrom}
              </span>
            )}
            {task.carriedFrom && task.status === 'ONGOING' && (
              <span className="flex items-center gap-0.5 text-xs text-red-500">
                <AlertCircle className="h-3 w-3" />
                逾期
              </span>
            )}
          </div>
        </div>

        {/* Structured context block */}
        {ctx ? (
          <div className="mt-2 space-y-1.5 text-xs">
            {ctx.projectName && (
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <Folder className="h-3 w-3 shrink-0 text-blue-400" />
                <span>{ctx.projectName}</span>
              </div>
            )}
            {ctx.path && (
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <MapPin className="h-3 w-3 shrink-0 text-purple-400" />
                <span className="font-mono text-[10px] truncate">{ctx.path}</span>
              </div>
            )}
            {ctx.context && (
              <div className="flex items-start gap-1.5 text-muted-foreground">
                <FileText className="h-3 w-3 shrink-0 mt-0.5 text-yellow-400" />
                <span className="line-clamp-2">{ctx.context}</span>
              </div>
            )}
            {ctx.taskDescription && (
              <div className="mt-1 p-2 rounded bg-muted/50 border border-border/50 text-muted-foreground line-clamp-3 leading-relaxed">
                {ctx.taskDescription}
              </div>
            )}
            {ctx.nextTasks && ctx.nextTasks.length > 0 && (
              <div className="mt-1">
                <div className="flex items-center gap-1 text-[10px] font-semibold uppercase text-green-400 mb-0.5">
                  <ArrowUpRight className="h-3 w-3" />
                  后续任务建议
                </div>
                <ul className="space-y-0.5 pl-4 border-l-2 border-green-500/30">
                  {ctx.nextTasks.map((nt, i) => (
                    <li key={i} className="text-[10px] text-muted-foreground truncate">
                      {nt}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : task.description ? (
          <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
            {task.description}
          </p>
        ) : null}

        {/* Date */}
        {task.date && (
          <div className="flex items-center gap-1 mt-2 text-xs text-muted-foreground">
            <Calendar className="h-3 w-3" />
            <span>{format(new Date(task.date), 'yyyy-MM-dd')}</span>
          </div>
        )}

        {/* Footer: agent + tokens */}
        <div className="flex items-center justify-between mt-3 pt-3 border-t border-border/50">
          <div className="flex items-center gap-2">
            <Avatar className="h-6 w-6">
              <AvatarImage src={task.agentAvatar} />
              <AvatarFallback className="text-xs">
                {task.agentName?.charAt(0) || 'A'}
              </AvatarFallback>
            </Avatar>
            <span className="text-xs text-muted-foreground truncate max-w-[80px]">
              {task.agentName}
            </span>
          </div>
          
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Coins className="h-3 w-3" />
            <span>{task.tokens.toLocaleString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
