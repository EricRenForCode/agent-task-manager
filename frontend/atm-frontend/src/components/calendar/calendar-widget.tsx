import { useQuery } from '@tanstack/react-query';
import { api } from '@/api/client';
import { useCalendarStore } from '@/stores';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { format, getDaysInMonth, startOfMonth, getDay, isSameDay } from 'date-fns';

const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function CalendarWidget() {
  const { selectedDate, goToPreviousMonth, goToNextMonth, setSelectedDate } = useCalendarStore();
  
  const year = selectedDate.getFullYear();
  const month = selectedDate.getMonth() + 1;

  const { data: calendarData } = useQuery({
    queryKey: ['calendar', 'monthly', year, month],
    queryFn: () => api.getMonthlyCalendar(year, month),
  });

  const daysInMonth = getDaysInMonth(selectedDate);
  const firstDayOfMonth = startOfMonth(selectedDate);
  const startingDayIndex = getDay(firstDayOfMonth);

  const getDayData = (day: number) => {
    if (!calendarData) return null;
    const dateStr = format(new Date(year, month - 1, day), 'yyyy-MM-dd');
    return calendarData.days.find(d => d.date === dateStr);
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-200 dark:border-slate-700">
        <h3 className="font-semibold text-slate-900 dark:text-white">
          {format(selectedDate, 'MMMM yyyy')}
        </h3>
        <div className="flex gap-1">
          <Button variant="ghost" size="icon" onClick={goToPreviousMonth}>
            <ChevronLeft className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={goToNextMonth}>
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Week days */}
      <div className="grid grid-cols-7 gap-px bg-slate-200 dark:bg-slate-700">
        {weekDays.map(day => (
          <div key={day} className="bg-slate-50 dark:bg-slate-800 p-2 text-center text-xs font-medium text-slate-500 dark:text-slate-400">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-px bg-slate-200 dark:bg-slate-700">
        {/* Empty cells for days before month starts */}
        {Array.from({ length: startingDayIndex }).map((_, i) => (
          <div key={`empty-${i}`} className="bg-white dark:bg-slate-800 h-20" />
        ))}

        {/* Days */}
        {Array.from({ length: daysInMonth }).map((_, i) => {
          const day = i + 1;
          const dayData = getDayData(day);
          const currentDate = new Date(year, month - 1, day);
          const isToday = isSameDay(currentDate, new Date());
          const isSelected = isSameDay(currentDate, selectedDate);

          return (
            <button
              key={day}
              onClick={() => setSelectedDate(currentDate)}
              className={cn(
                "bg-white dark:bg-slate-800 h-20 p-2 text-left transition-colors hover:bg-slate-50 dark:hover:bg-slate-700/50 relative",
                isSelected && "ring-2 ring-inset ring-blue-500",
                isToday && "bg-blue-50 dark:bg-blue-900/20"
              )}
            >
              <span className={cn(
                "text-sm font-medium",
                isToday ? "text-blue-600 dark:text-blue-400" : "text-slate-700 dark:text-slate-300"
              )}>
                {day}
              </span>

              {/* Task indicators */}
              {dayData && dayData.has_tasks && (
                <div className="flex gap-0.5 mt-1 flex-wrap">
                  {dayData.task_count.todo > 0 && (
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                  )}
                  {dayData.task_count.ongoing > 0 && (
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  )}
                  {dayData.task_count.done > 0 && (
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  )}
                </div>
              )}

              {/* Task count */}
              {dayData && dayData.has_tasks && (
                <span className="absolute bottom-1 right-1 text-xs text-slate-400">
                  {dayData.task_count.todo + dayData.task_count.ongoing + dayData.task_count.done}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
