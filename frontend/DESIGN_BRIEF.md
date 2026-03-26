# Agent Task Manager - Frontend Design Brief

## 项目概述
智能体每日任务管理系统前端，用于监控 OpenClaw 各智能体的任务状态和 token 消耗。

## 核心功能
1. **日历视图** - 月历展示，点击日期查看详情
2. **任务看板** - 当日任务分三列：TODO / ONGOING / DONE
3. **任务卡片** - 显示：任务名、简介、负责智能体、消耗 token
4. **智能体管理** - 查看智能体列表和统计

## 技术栈
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Date Handling**: date-fns
- **Icons**: Lucide React

## 页面结构
```
/                     → Dashboard (日历 + 今日任务)
/agents               → 智能体列表
/agents/:id           → 智能体详情 + 统计
/tasks                → 所有任务列表
/calendar             → 日历视图（全屏）
```

## API 端点
- `GET /api/v1/calendar/monthly?year=&month=` - 月度数据
- `GET /api/v1/calendar/daily?date=` - 单日详情
- `GET /api/v1/tasks?date=&agent_id=&status=` - 任务列表
- `GET /api/v1/agents` - 智能体列表
- `GET /api/v1/agents/:id/stats` - 智能体统计

## 设计要求

### 1. 日历组件
- 月视图，显示每日任务数量（todo/ongoing/done）
- 颜色编码：不同状态用不同颜色小圆点
- 点击日期跳转当日详情
- 支持月份切换

### 2. 任务看板 (Kanban)
- 三列布局：TODO | ONGOING | DONE
- 拖拽排序（可选）
- 任务卡片包含：
  - 任务标题
  - 简短描述（1-2行）
  - 智能体头像 + 名称
  - Token 消耗（带图标）
  - 状态标签

### 3. 视觉风格
- 现代、专业、清晰
- 支持 Light/Dark 模式
- 卡片式设计，适当的阴影和圆角
- 响应式布局（桌面优先，支持平板）

### 4. 颜色建议
- Primary: 蓝色系（科技、专业）
- Success/Done: 绿色
- Warning/Ongoing: 橙色/黄色
- Todo: 灰色/蓝色

## 文件结构
```
frontend/
├── src/
│   ├── components/          # UI 组件
│   │   ├── ui/             # shadcn 基础组件
│   │   ├── calendar/       # 日历相关
│   │   ├── task/           # 任务卡片/看板
│   │   └── layout/         # 布局组件
│   ├── pages/              # 页面
│   ├── hooks/              # 自定义 hooks
│   ├── stores/             # Zustand stores
│   ├── lib/                # 工具函数
│   ├── types/              # TypeScript 类型
│   └── api/                # API 客户端
├── public/
└── ...config files
```

## 交付物
1. 完整的设计系统规范（colors, typography, spacing）
2. 组件库（Button, Card, Badge, Calendar, etc.）
3. 页面实现（Dashboard, Agents, Tasks, Calendar）
4. API 集成
5. 响应式布局

## 公司 Design System 参考
请基于 ui-ux-pro-max 技能生成完整的设计系统规范：
- 使用 `python3 ~/.agents/skills/ui-ux-pro-max/scripts/search.py` 工具
- 产品类型：SaaS Dashboard / Admin Panel
- 关键词：minimal, professional, modern, dark-mode-ready
