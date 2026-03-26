import { useUIStore } from '@/stores';
import { cn } from '@/lib/utils';

interface PageContainerProps {
  children: React.ReactNode;
  className?: string;
}

export function PageContainer({ children, className }: PageContainerProps) {
  const { sidebarOpen } = useUIStore();

  return (
    <div
      className={cn(
        "min-h-screen bg-slate-50 dark:bg-slate-950 pt-16 transition-all duration-300",
        sidebarOpen ? "lg:pl-64" : "lg:pl-20",
        className
      )}
    >
      <main className="p-6">
        {children}
      </main>
    </div>
  );
}
