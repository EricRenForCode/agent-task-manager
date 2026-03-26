import { useState } from 'react';
import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, addDays, isSameMonth, isSameDay, addMonths, subMonths } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useCalendarStore } from '@/stores';
import { cn } from '@/lib/utils';
import { CalendarDay } from '@/types';

interface CalendarWidgetProps {
  days?: CalendarDay[];
  onDateClick?: (date: Date) => void;
  className?: string;
}

export function CalendarWidget({ days = [], onDateClick, className }: CalendarWidgetProps) {
  const { selectedDate, setSelectedDate, goToPreviousMonth, goToNextMonth, goToToday } = useCalendarStore();
  const [currentMonth, setCurrentMonth] = useState(selectedDate);

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  const calendarStart = startOfWeek(monthStart, { locale: zhCN });
  const calendarEnd = endOfWeek(monthEnd, { locale: zhCN });

  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

  const handlePrevMonth = () => {
    setCurrentMonth(subMonths(currentMonth, 1));
    goToPreviousMonth();
  };

  const handleNextMonth = () => {
    setCurrentMonth(addMonths(currentMonth, 1));
    goToNextMonth();
  };

  const handleToday = () => {
    const today = new Date();
    setCurrentMonth(today);
    goToToday();
  };

  const handleDateClick = (date: Date) => {
    setSelectedDate(date);
    onDateClick?.(date);
  };

  // Generate calendar grid
  const generateCalendarDays = () => {
    const days_array = [];
    let day = calendarStart;

    while (day <= calendarEnd) {
      days_array.push(day);
      day = addDays(day, 1);
    }

    return days_array;
  };

  const calendarDays = generateCalendarDays();

  const getDayTasks = (date: Date): CalendarDay | undefined => {
    const dateStr = format(date, 'yyyy-MM-dd');
    return days.find((d) => d.date === dateStr);
  };

  return (
    <Card className={cn("h-full", className)}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-semibold">
          {format(currentMonth, 'yyyy年 M月', { locale: zhCN })}
        </CardTitle>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={handlePrevMonth}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8" onClick={handleToday}>
            今天
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={handleNextMonth}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {/* Weekday headers */}
        <div className="grid grid-cols-7 mb-2">
          {weekDays.map((day) => (
            <div key={day} className="text-center text-sm font-medium text-muted-foreground py-2">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar grid */}
        <div className="grid grid-cols-7 gap-1">
          {calendarDays.map((date, index) => {
            const isCurrentMonth = isSameMonth(date, currentMonth);
            const isSelected = isSameDay(date, selectedDate);
            const isToday = isSameDay(date, new Date());
            const dayTasks = getDayTasks(date);

            return (
              <button
                key={index}
                onClick={() => handleDateClick(date)}
                className={cn(
                  "relative h-14 p-1 text-sm rounded-lg transition-colors",
                  !isCurrentMonth && "text-muted-foreground/50",
                  isSelected && "bg-primary text-primary-foreground",
                  !isSelected && isCurrentMonth && "hover:bg-accent",
                  isToday && !isSelected && "ring-2 ring-primary ring-inset"
                )}
              >
                <span className="absolute top-1 left-1">{format(date, 'd')}</span>
                
                {/* Task indicators */}
                {dayTasks && (
                  <div className="absolute bottom-1 left-1 right-1 flex justify-center gap-0.5">
                    {dayTasks.tasks.todo > 0 && (
                      <span className={cn(
                        "h-1.5 w-1.5 rounded-full",
                        isSelected ? "bg-primary-foreground/70" : "bg-muted-foreground"
                      )} />
                    )}
                    {dayTasks.tasks.ongoing > 0 && (
                      <span className={cn(
                        "h-1.5 w-1.5 rounded-full",
                        isSelected ? "bg-amber-300" : "bg-amber-500"
                      )} />
                    )}
                    {dayTasks.tasks.done > 0 && (
                      <span className={cn(
                        "h-1.5 w-1.5 rounded-full",
                        isSelected ? "bg-emerald-300" : "bg-emerald-500"
                      )} />
                    )}
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-4 mt-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-muted-foreground" />
            <span>待办</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-amber-500" />
            <span>进行中</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            <span>已完成</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}