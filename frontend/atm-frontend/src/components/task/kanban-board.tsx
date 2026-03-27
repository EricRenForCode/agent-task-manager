import type { Task, TaskStatus } from '@/types';
import { TaskCard } from './task-card';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';

interface KanbanBoardProps {
  tasks: Task[];
  onTaskClick?: (task: Task) => void;
  loading?: boolean;
}

const columns: { status: TaskStatus; title: string; color: string }[] = [
  { status: 'TODO', title: 'To Do', color: 'border-slate-200 dark:border-slate-700' },
  { status: 'ONGOING', title: 'In Progress', color: 'border-amber-200 dark:border-amber-800' },
  { status: 'DONE', title: 'Done', color: 'border-emerald-200 dark:border-emerald-800' },
];

export function KanbanBoard({ tasks, onTaskClick, loading }: KanbanBoardProps) {
  const getTasksByStatus = (status: TaskStatus) => 
    tasks.filter(task => task.status === status);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map(column => (
          <div key={column.status} className="bg-slate-100 dark:bg-slate-800/50 rounded-xl p-4">
            <div className="h-6 w-24 bg-slate-200 dark:bg-slate-700 rounded animate-pulse mb-4" />
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-24 bg-white dark:bg-slate-800 rounded-lg animate-pulse" />
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {columns.map(column => {
        const columnTasks = getTasksByStatus(column.status);
        
        return (
          <div 
            key={column.status}
            className={cn(
              "bg-slate-50 dark:bg-slate-800/50 rounded-xl border-2 border-dashed",
              column.color,
              "flex flex-col max-h-[600px]"
            )}
          >
            {/* Column Header */}
            <div className="p-4 border-b border-slate-200 dark:border-slate-700">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  {column.title}
                </h3>
                <span className="text-sm text-slate-500 bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-full">
                  {columnTasks.length}
                </span>
              </div>
            </div>

            {/* Tasks */}
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-3">
                {columnTasks.map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onClick={onTaskClick}
                  />
                ))}
                {columnTasks.length === 0 && (
                  <div className="text-center py-8 text-slate-400 text-sm">
                    No tasks
                  </div>
                )}
              </div>
            </ScrollArea>
          </div>
        );
      })}
    </div>
  );
}
