import { NavLink, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  CheckSquare, 
  Calendar as CalendarIcon,
  Menu,
  X,
  Bot,
  Sun,
  Moon
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { useUIStore } from '@/stores';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/agents', label: 'Agents', icon: Users },
  { path: '/tasks', label: 'Tasks', icon: CheckSquare },
  { path: '/calendar', label: 'Calendar', icon: CalendarIcon },
];

export function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useUIStore();
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => toggleSidebar()}
        />
      )}
      
      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-50 h-screen w-64 bg-card border-r border-border transition-transform duration-300 ease-in-out lg:translate-x-0",
          !sidebarOpen && "-translate-x-full lg:hidden"
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-6 border-b border-border">
            <div className="flex items-center gap-2">
              <Bot className="h-6 w-6 text-primary" />
              <span className="text-lg font-semibold">Agent Manager</span>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={toggleSidebar}
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Navigation */}
          <ScrollArea className="flex-1 py-4">
            <nav className="px-3 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path ||
                  (item.path !== '/' && location.pathname.startsWith(item.path));
                
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                      isActive 
                        ? "bg-primary text-primary-foreground" 
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )}
                    onClick={() => {
                      if (window.innerWidth < 1024) {
                        toggleSidebar();
                      }
                    }}
                  >
                    <Icon className="h-5 w-5" />
                    {item.label}
                  </NavLink>
                );
              })}
            </nav>
          </ScrollArea>

          {/* Footer */}
          <div className="border-t border-border p-4">
            <p className="text-xs text-muted-foreground text-center">
              Agent Task Manager v1.0
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}

export function Header() {
  const { toggleSidebar } = useUIStore();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4 lg:px-8">
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={toggleSidebar}
      >
        <Menu className="h-5 w-5" />
      </Button>
      
      <div className="flex-1" />
      
      <div className="flex items-center gap-4">
        {/* Theme toggle could go here */}
      </div>
    </header>
  );
}

export function Layout({ children }: { children: React.ReactNode }) {
  const { sidebarOpen } = useUIStore();

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className={cn(
        "transition-all duration-300 ease-in-out",
        sidebarOpen ? "lg:ml-64" : "lg:ml-0"
      )}>
        <Header />
        <main className="p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}