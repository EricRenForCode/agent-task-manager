import { Task } from '@/types';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Coins, Clock, CheckCircle2, Circle } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onClick?: (task: Task) => void;
  compact?: boolean;
}

const statusConfig = {
  TODO: {
    label: 'To Do',
    color: 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-200',
    icon: Circle,
  },
  ONGOING: {
    label: 'In Progress',
    color: 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
    icon: Clock,
  },
  DONE: {
    label: 'Done',
    color: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
    icon: CheckCircle2,
  },
};

export function TaskCard({ task, onClick, compact = false }: TaskCardProps) {
  const status = statusConfig[task.status];
  const StatusIcon = status.icon;

  if (compact) {
    return (
      <div
        onClick={() => onClick?.(task)}
        className={cn(
          "p-3 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700",
          "hover:shadow-md transition-shadow cursor-pointer"
        )}
      >
        <div className="flex items-start justify-between gap-2">
          <h4 className="font-medium text-slate-900 dark:text-white text-sm line-clamp-1">
            {task.title}
          </h4>
          <StatusIcon className={cn("w-4 h-4 flex-shrink-0", 
            task.status === 'TODO' && "text-slate-400",
            task.status === 'ONGOING' && "text-amber-500",
            task.status === 'DONE' && "text-emerald-500"
          )} />
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={() => onClick?.(task)}
      className={cn(
        "p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700",
        "hover:shadow-md transition-all cursor-pointer group"
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <h4 className="font-semibold text-slate-900 dark:text-white line-clamp-2">
          {task.title}
        </h4>
        <Badge className={cn("flex-shrink-0", status.color)}>
          <StatusIcon className="w-3 h-3 mr-1" />
          {status.label}
        </Badge>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 mb-4">
          {task.description}
        </p>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between">
        {/* Agent */}
        <div className="flex items-center gap-2">
          <Avatar className="w-6 h-6">
            <AvatarFallback className="text-xs bg-blue-100 text-blue-700">
              {task.agentName.slice(0, 2).toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <span className="text-xs text-slate-600 dark:text-slate-400">
            {task.agentName}
          </span>
        </div>

        {/* Tokens */}
        <div className="flex items-center gap-1 text-xs text-slate-500">
          <Coins className="w-3.5 h-3.5" />
          <span>{task.tokens.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
}
