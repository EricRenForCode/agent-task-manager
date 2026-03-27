import type { Task, TaskStatus } from '@/types';
import { TaskCard } from './TaskCard';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Circle, Loader2, CheckCircle2 } from 'lucide-react';

interface KanbanBoardProps {
  tasks: Task[];
  className?: string;
}

interface KanbanColumnProps {
  title: string;
  status: TaskStatus;
  tasks: Task[];
  icon: React.ReactNode;
  colorClass: string;
}

function KanbanColumn({ title, status, tasks, icon, colorClass }: KanbanColumnProps) {
  const columnTasks = tasks.filter((t) => t.status === status);

  return (
    <div className="flex flex-col min-w-[280px] w-full bg-muted/50 rounded-lg">
      <div className={cn("flex items-center gap-2 p-3 border-b", colorClass)}>
        {icon}
        <span className="font-medium text-sm">{title}</span>
        <span className="ml-auto text-xs text-muted-foreground bg-background px-2 py-0.5 rounded-full">
          {columnTasks.length}
        </span>
      </div>
      
      <ScrollArea className="flex-1 p-3">
        <div className="space-y-3">
          {columnTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
          {columnTasks.length === 0 && (
            <div className="text-center py-8 text-muted-foreground text-sm">
              暂无任务
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

export function KanbanBoard({ tasks, className }: KanbanBoardProps) {
  const columns: KanbanColumnProps[] = [
    {
      title: '待办',
      status: 'TODO',
      tasks,
      icon: <Circle className="h-4 w-4 text-muted-foreground" />,
      colorClass: 'border-border',
    },
    {
      title: '进行中',
      status: 'ONGOING',
      tasks,
      icon: <Loader2 className="h-4 w-4 text-amber-500" />,
      colorClass: 'border-amber-200 dark:border-amber-900',
    },
    {
      title: '已完成',
      status: 'DONE',
      tasks,
      icon: <CheckCircle2 className="h-4 w-4 text-emerald-500" />,
      colorClass: 'border-emerald-200 dark:border-emerald-900',
    },
  ];

  return (
    <div className={cn("grid grid-cols-1 md:grid-cols-3 gap-4 h-full", className)}>
      {columns.map((column) => (
        <KanbanColumn key={column.status} {...column} />
      ))}
    </div>
  );
}