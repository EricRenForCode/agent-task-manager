# Agent Task Manager - Design System

## Overview
A modern, professional design system for the Agent Task Manager dashboard. Built with shadcn/ui, Tailwind CSS, and optimized for both light and dark modes.

---

## Color Palette

### Primary Colors
| Name | Hex | Tailwind | Usage |
|------|-----|----------|-------|
| Primary | `#2563EB` | `blue-600` | Main actions, links, active states |
| Primary Light | `#3B82F6` | `blue-500` | Hover states, secondary accents |
| Primary Dark | `#1D4ED8` | `blue-700` | Active/pressed states |

### Semantic Colors
| Name | Hex | Tailwind | Usage |
|------|-----|----------|-------|
| Success | `#10B981` | `emerald-500` | Completed tasks, success states |
| Success Light | `#34D399` | `emerald-400` | Success hover states |
| Warning | `#F59E0B` | `amber-500` | In-progress, ongoing tasks |
| Warning Light | `#FBBF24` | `amber-400` | Warning hover states |
| Error | `#EF4444` | `red-500` | Errors, failed tasks |
| Error Light | `#F87171` | `red-400` | Error hover states |
| Info | `#3B82F6` | `blue-500` | Informational states |

### Gray Scale (Slate)
| Name | Hex | Tailwind | Usage |
|------|-----|----------|-------|
| Gray 50 | `#F8FAFC` | `slate-50` | Light backgrounds |
| Gray 100 | `#F1F5F9` | `slate-100` | Subtle backgrounds |
| Gray 200 | `#E2E8F0` | `slate-200` | Borders, dividers |
| Gray 300 | `#CBD5E1` | `slate-300` | Disabled states |
| Gray 400 | `#94A3B8` | `slate-400` | Placeholder text |
| Gray 500 | `#64748B` | `slate-500` | Secondary text |
| Gray 600 | `#475569` | `slate-600` | Body text muted |
| Gray 700 | `#334155` | `slate-700` | Strong text |
| Gray 800 | `#1E293B` | `slate-800` | Headings, primary text |
| Gray 900 | `#0F172A` | `slate-900` | Dark mode text |

### Dark Mode Colors
| Name | Hex | Tailwind | Usage |
|------|-----|----------|-------|
| Dark Background | `#0F172A` | `slate-900` | Main dark background |
| Dark Surface | `#1E293B` | `slate-800` | Cards, elevated surfaces |
| Dark Border | `#334155` | `slate-700` | Borders in dark mode |

### Status Colors (Task States)
| Status | Light Mode | Dark Mode | Icon |
|--------|------------|-----------|------|
| TODO | `slate-500` | `slate-400` | Circle |
| ONGOING | `amber-500` | `amber-400` | Clock |
| DONE | `emerald-500` | `emerald-400` | CheckCircle |

---

## Typography

### Font Families
- **Primary**: `Inter` (Google Fonts)
- **Fallback**: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Monospace**: `JetBrains Mono` or `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`

### Type Scale
| Style | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| H1 | `text-3xl` (30px) | 700 | 1.2 | -0.025em | Page titles |
| H2 | `text-2xl` (24px) | 600 | 1.3 | -0.025em | Section headers |
| H3 | `text-xl` (20px) | 600 | 1.4 | -0.025em | Card titles |
| H4 | `text-lg` (18px) | 600 | 1.5 | -0.025em | Subsection headers |
| Body Large | `text-base` (16px) | 400 | 1.6 | 0 | Primary body text |
| Body | `text-sm` (14px) | 400 | 1.5 | 0 | Secondary text |
| Caption | `text-xs` (12px) | 500 | 1.4 | 0.025em | Labels, metadata |
| Overline | `text-xs` (12px) | 600 | 1.4 | 0.05em | Uppercase labels |

### Typography Patterns
- **Headings**: Use `font-semibold` or `font-bold` with tight letter-spacing
- **Body**: Use `font-normal` with comfortable line-height (1.5-1.6)
- **Labels**: Use `font-medium` with `text-xs` and uppercase transform
- **Numbers/Stats**: Use `tabular-nums` for aligned numeric data

---

## Spacing System

### Base Unit: 4px (0.25rem)

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Tight spacing, icon gaps |
| `space-2` | 8px | Inline elements, small gaps |
| `space-3` | 12px | Default component padding |
| `space-4` | 16px | Standard spacing |
| `space-5` | 20px | Section gaps |
| `space-6` | 24px | Card padding |
| `space-8` | 32px | Large section gaps |
| `space-10` | 40px | Page section spacing |
| `space-12` | 48px | Major section breaks |

### Layout Spacing
- **Page padding**: `px-4 sm:px-6 lg:px-8`
- **Content max-width**: `max-w-7xl mx-auto`
- **Card padding**: `p-6` (24px)
- **Card gap**: `gap-6` (24px)
- **Section gap**: `gap-8` (32px)

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `rounded-sm` | 2px | Small elements, tags |
| `rounded` | 4px | Buttons, inputs |
| `rounded-md` | 6px | Small cards, badges |
| `rounded-lg` | 8px | Default cards, modals |
| `rounded-xl` | 12px | Large cards, containers |
| `rounded-2xl` | 16px | Feature cards, hero |
| `rounded-full` | 9999px | Avatars, pills |

### Usage Guidelines
- **Buttons**: `rounded-md` (6px)
- **Cards**: `rounded-lg` or `rounded-xl` (8-12px)
- **Inputs**: `rounded-md` (6px)
- **Avatars**: `rounded-full`
- **Badges**: `rounded-full` (pills)

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `shadow-sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtle elevation |
| `shadow` | `0 1px 3px 0 rgb(0 0 0 / 0.1)` | Default cards |
| `shadow-md` | `0 4px 6px -1px rgb(0 0 0 / 0.1)` | Elevated cards |
| `shadow-lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1)` | Modals, dropdowns |
| `shadow-xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1)` | Dialogs, popovers |

### Dark Mode Shadows
- Use lower opacity shadows in dark mode
- Consider using `shadow-slate-900/20` for tinted shadows

---

## Breakpoints

| Name | Min Width | Tailwind | Usage |
|------|-----------|----------|-------|
| Mobile | 0px | Default | Base styles |
| sm | 640px | `sm:` | Large phones |
| md | 768px | `md:` | Tablets |
| lg | 1024px | `lg:` | Small laptops |
| xl | 1280px | `xl:` | Desktops |
| 2xl | 1536px | `2xl:` | Large screens |

### Responsive Patterns
- **Mobile-first**: Write base styles for mobile, use breakpoints to enhance
- **Container**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Grid**: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- **Sidebar**: Hidden on mobile, `lg:block` on desktop

---

## Component Tokens

### Buttons
```
Primary: bg-blue-600 text-white hover:bg-blue-700 rounded-md px-4 py-2
Secondary: bg-slate-100 text-slate-900 hover:bg-slate-200 rounded-md px-4 py-2
Ghost: hover:bg-slate-100 text-slate-700 rounded-md px-4 py-2
Danger: bg-red-600 text-white hover:bg-red-700 rounded-md px-4 py-2
```

### Cards
```
Default: bg-white dark:bg-slate-800 rounded-lg shadow border border-slate-200 dark:border-slate-700 p-6
Hoverable: transition-shadow hover:shadow-md cursor-pointer
```

### Inputs
```
Default: bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-md px-3 py-2
Focus: ring-2 ring-blue-500 border-blue-500 outline-none
Disabled: bg-slate-100 text-slate-500 cursor-not-allowed
```

### Badges
```
Default: inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
Status Todo: bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-200
Status Ongoing: bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200
Status Done: bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200
```

---

## Animation & Transitions

### Durations
| Duration | Usage |
|----------|-------|
| `duration-150` | Micro-interactions (buttons) |
| `duration-200` | Standard transitions |
| `duration-300` | Larger state changes |

### Easing
- **Default**: `ease-in-out`
- **Enter**: `ease-out`
- **Exit**: `ease-in`

### Common Transitions
```
Hover: transition-colors duration-200
Transform: transition-transform duration-200
All: transition-all duration-200 ease-in-out
```

### Accessibility
- Respect `prefers-reduced-motion` media query
- Avoid animations that trigger vestibular disorders

---

## Z-Index Scale

| Layer | Z-Index | Usage |
|-------|---------|-------|
| Base | 0 | Default content |
| Dropdown | 10 | Dropdown menus |
| Sticky | 20 | Sticky headers |
| Fixed | 30 | Fixed navigation |
| Modal Backdrop | 40 | Modal overlays |
| Modal | 50 | Modal content |
| Popover | 60 | Popovers, tooltips |
| Toast | 70 | Notifications |

---

## Dark Mode Implementation

### Strategy
- Use Tailwind's `dark:` modifier
- Store preference in localStorage
- Default to system preference
- Toggle class on `<html>` element

### Color Mapping
| Light Mode | Dark Mode |
|------------|-----------|
| `bg-white` | `dark:bg-slate-900` |
| `bg-slate-50` | `dark:bg-slate-800` |
| `text-slate-900` | `dark:text-slate-100` |
| `text-slate-600` | `dark:text-slate-400` |
| `border-slate-200` | `dark:border-slate-700` |

---

## Icons

### Library: Lucide React
- Consistent 24x24 viewBox
- Stroke width: 2px default
- Size classes: `w-4 h-4`, `w-5 h-5`, `w-6 h-6`

### Common Icons
| Usage | Icon Name |
|-------|-----------|
| Dashboard | `LayoutDashboard` |
| Calendar | `Calendar` |
| Tasks | `CheckSquare` |
| Agents | `Bot` |
| Settings | `Settings` |
| Search | `Search` |
| Filter | `Filter` |
| More | `MoreVertical` |
| Edit | `Pencil` |
| Delete | `Trash2` |
| Close | `X` |
| Check | `Check` |
| Chevron | `ChevronDown`, `ChevronRight` |
| Token | `Coins` |
| Time | `Clock` |

---

## Accessibility

### Requirements
- Minimum contrast ratio: 4.5:1 for normal text
- Focus indicators visible on all interactive elements
- Keyboard navigation support
- ARIA labels for icon-only buttons
- Semantic HTML structure

### Focus States
```
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
```

### Screen Reader
- Use `sr-only` class for visually hidden labels
- Provide `aria-label` for icon buttons
- Use `aria-expanded` for collapsible sections
- Use `aria-current` for active navigation items
