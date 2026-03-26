import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { api } from '@/api/client';
import { Layout } from '@/components/layout/sidebar';
import { CalendarWidget } from '@/components/calendar/CalendarWidget';
import { TaskCard } from '@/components/task/TaskCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useCalendarStore } from '@/stores';
import { Skeleton } from '@/components/ui/skeleton';

export default function CalendarPage() {
  const { selectedDate, setSelectedDate } = useCalendarStore();
  const dateStr = format(selectedDate, 'yyyy-MM-dd');

  const { data: calendarData } = useQuery({
    queryKey: ['calendar-monthly', selectedDate.getFullYear(), selectedDate.getMonth() + 1],
    queryFn: () => api.getMonthlyCalendar(selectedDate.getFullYear(), selectedDate.getMonth() + 1),
  });

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks-daily', dateStr],
    queryFn: () => api.getDailyTasks(dateStr),
  });

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">日历视图</h1>
          <p className="text-muted-foreground">查看每日任务安排</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <CalendarWidget
              days={calendarData?.days}
              onDateClick={(date) => setSelectedDate(date)}
            />
          </div>
          
          <div>
            <Card>
              <CardHeader>
                <CardTitle>{format(selectedDate, 'yyyy年MM月dd日')} 任务</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="space-y-3">
                    {[1, 2, 3].map((i) => (
                      <Skeleton key={i} className="h-20" />
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {tasks?.map((task) => (
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
        </div>
      </div>
    </Layout>
  );
}
