import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
    }),
    {
      name: 'ui-storage',
    }
  )
);

interface CalendarState {
  selectedDate: Date;
  currentView: 'month' | 'week' | 'day';
  setSelectedDate: (date: Date) => void;
  setCurrentView: (view: 'month' | 'week' | 'day') => void;
  goToToday: () => void;
  goToPreviousMonth: () => void;
  goToNextMonth: () => void;
}

export const useCalendarStore = create<CalendarState>((set) => ({
  selectedDate: new Date(),
  currentView: 'month',
  setSelectedDate: (date) => set({ selectedDate: date }),
  setCurrentView: (view) => set({ currentView: view }),
  goToToday: () => set({ selectedDate: new Date() }),
  goToPreviousMonth: () =>
    set((state) => {
      const newDate = new Date(state.selectedDate);
      newDate.setMonth(newDate.getMonth() - 1);
      return { selectedDate: newDate };
    }),
  goToNextMonth: () =>
    set((state) => {
      const newDate = new Date(state.selectedDate);
      newDate.setMonth(newDate.getMonth() + 1);
      return { selectedDate: newDate };
    }),
}));