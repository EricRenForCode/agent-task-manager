# Agent Task Manager (ATM)

<p>
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

## English

ATM is a task management system designed for **OpenClaw Agents**. It enables agents to autonomously fetch tasks from ATM, execute them, and sync results back — completing a fully automated task loop.

```
┌─────────────────────────────────────────────────────────┐
│                    ATM Architecture                      │
│                                                         │
│  OpenClaw Agent                                         │
│       │                                                 │
│       │  1. Fetch tasks   (GET /tasks)                  │
│       │  2. Execute tasks                               │
│       │  3. Update status (PATCH /tasks/{id}/status)    │
│       │  4. Heartbeat     (POST /heartbeat)             │
│       ▼                                                 │
│  ATM Backend (FastAPI + PostgreSQL)                     │
│       │                                                 │
│       ▼                                                 │
│  ATM Frontend (React Dashboard)                         │
└─────────────────────────────────────────────────────────┘
```

### Features

- **Task Assignment** — Assign and track tasks across multiple agents with priority and status management
- **Autonomous Execution** — Agents pull and update tasks via `atm-client-skill` with no human intervention
- **Heartbeat Monitoring** — Agents report online status and token usage for real-time health tracking
- **Calendar View** — View task distribution and completion by day or month
- **Dashboard** — React frontend with agent list, kanban board, and stats

---

### Quick Start

#### 1. Start Backend

```bash
cd backend
docker compose up -d
```

Wait for the database:

```bash
docker compose logs -f db
# Ready when you see "database system is ready to accept connections"
```

#### 2. Start Frontend

```bash
cd frontend/atm-frontend
cp .env.example .env   # sets VITE_API_BASE_URL (backend API base URL)
npm install
npm run dev
```

#### 3. Access

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:5173 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

### OpenClaw Agent Integration

#### Step 1: Register an Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "description": "My OpenClaw Agent"}'
```

The response includes an `api_key` — save it for heartbeat authentication.

#### Step 2: Install atm-client-skill

Install the `atm-client-skill/` directory into your OpenClaw workspace. The agent can then manage tasks via CLI:

```bash
# Fetch pending tasks
atm list --agent my-agent --status todo

# Update task status
atm update <task-id> --status done

# Create a task
atm create --title "Research competitors" --priority high --agent my-agent
```

Environment variable:

```bash
export ATM_API_BASE=http://localhost:8000/api/v1
```

#### Step 3: Configure Autonomous Loop (Scheduled Task)

In Claude Code Desktop App, tell Claude directly:

```
Every day at 9am and 9pm, fetch my pending tasks from ATM, execute them one by one,
and update their status to done when complete.
```

Claude will create a Scheduled Task automatically. You can also create the task file manually at `~/.claude/scheduled-tasks/atm-task-loop/SKILL.md`:

```markdown
---
name: atm-task-loop
description: Fetch and execute ATM tasks twice daily
---

Fetch my pending tasks with `atm list --status todo`,
execute them one by one, then update each with `atm update <id> --status done`.
```

Then set the frequency in the Desktop App UI (Daily / Hourly / Weekdays / Weekly).

#### Step 4: Configure Heartbeat

Add a heartbeat report in your agent's `HEARTBEAT.md`:

```python
import requests, os

requests.post("http://localhost:8000/api/v1/heartbeat", json={
    "agent_name": "my-agent",
    "agent_key": os.getenv("AGENT_TASK_KEY"),
    "status": "online",
    "tasks": [...],          # current task snapshot
    "tokens_consumed": 1200
})
```

---

### API Reference

#### Agent Management
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/agents` | List all agents |
| POST | `/api/v1/agents` | Create agent |
| GET | `/api/v1/agents/{id}` | Agent detail |
| PUT | `/api/v1/agents/{id}` | Update agent |
| DELETE | `/api/v1/agents/{id}` | Delete agent |
| GET | `/api/v1/agents/{id}/stats` | Agent stats |

#### Task Management
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/tasks` | List tasks (filter by `date`, `agent_id`, `status`) |
| POST | `/api/v1/tasks` | Create task |
| GET | `/api/v1/tasks/{id}` | Task detail |
| PUT | `/api/v1/tasks/{id}` | Update task |
| PATCH | `/api/v1/tasks/{id}/status` | Update task status |
| DELETE | `/api/v1/tasks/{id}` | Delete task |

#### Calendar & Heartbeat
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/calendar/monthly` | Monthly task view |
| GET | `/api/v1/calendar/daily` | Daily task detail |
| POST | `/api/v1/heartbeat` | Agent heartbeat report |

---

### Project Structure

```
agent-task-manager/
├── backend/              # FastAPI backend + PostgreSQL
│   ├── src/
│   │   ├── routers/      # API routes (tasks, agents, heartbeat, calendar)
│   │   ├── models/       # Database models
│   │   └── schemas/      # Pydantic schemas
│   └── docker-compose.yml
├── frontend/
│   └── atm-frontend/     # React + TypeScript + Tailwind dashboard
├── atm-client-skill/     # OpenClaw Skill CLI tool
│   └── atm-cli.py
├── skills/               # Built-in skills (news-fetch, etc.)
└── scripts/              # Install scripts
```

---

### Local Development

```bash
# Backend (without Docker)
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload

# Frontend
cd frontend/atm-frontend
cp .env.example .env
npm install
npm run dev
```

---

## 中文

ATM 是一个专为 **OpenClaw Agent** 设计的任务管理系统。它让 Agent 能够自主地从 ATM 获取任务、执行任务、并将结果同步回来，实现全自动的任务闭环。

```
┌─────────────────────────────────────────────────────────┐
│                      ATM 系统架构                        │
│                                                         │
│  OpenClaw Agent                                         │
│       │                                                 │
│       │  1. 拉取任务 (GET /tasks)                        │
│       │  2. 执行任务                                     │
│       │  3. 更新状态 (PATCH /tasks/{id}/status)          │
│       │  4. 心跳上报 (POST /heartbeat)                   │
│       ▼                                                 │
│  ATM Backend (FastAPI + PostgreSQL)                     │
│       │                                                 │
│       ▼                                                 │
│  ATM Frontend (React Dashboard)                         │
└─────────────────────────────────────────────────────────┘
```

### 核心功能

- **任务分配** — 为多个 Agent 分配、追踪任务，支持优先级与状态管理
- **自主执行** — Agent 通过 `atm-client-skill` 主动拉取并更新任务，无需人工干预
- **心跳监控** — Agent 定期上报在线状态与 token 消耗，实时掌握 Agent 运行健康
- **日历视图** — 按日/月维度查看任务分布与完成情况
- **可视化面板** — React 前端展示 Agent 列表、任务看板与统计数据

---

### 快速开始

#### 1. 启动后端

```bash
cd backend
docker compose up -d
```

等待数据库就绪：

```bash
docker compose logs -f db
# 看到 "database system is ready to accept connections" 即可
```

#### 2. 启动前端

```bash
cd frontend/atm-frontend
cp .env.example .env   # 配置 VITE_API_BASE_URL（后端 API 地址）
npm install
npm run dev
```

#### 3. 访问

| 服务 | 地址 |
|------|------|
| 前端面板 | http://localhost:5173 |
| API 文档 | http://localhost:8000/docs |
| 健康检查 | http://localhost:8000/health |

---

### OpenClaw Agent 集成

#### 第一步：注册 Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "description": "My OpenClaw Agent"}'
```

响应中包含 `api_key`，保存用于后续心跳认证。

#### 第二步：安装 atm-client-skill

将 `atm-client-skill/` 目录安装到你的 OpenClaw 工作区，然后 Agent 即可通过 CLI 操作任务：

```bash
# 拉取待办任务
atm list --agent my-agent --status todo

# 更新任务状态
atm update <task-id> --status done

# 创建新任务
atm create --title "调研竞品" --priority high --agent my-agent
```

环境变量：

```bash
export ATM_API_BASE=http://localhost:8000/api/v1
```

#### 第三步：配置自主循环（Scheduled Task）

在 Claude Code Desktop App 中直接告诉 Claude：

```
每天早上 9 点和晚上 9 点，从 ATM 拉取我的待办任务，逐一执行，完成后更新状态
```

Claude 会自动创建 Scheduled Task。也可以手动在 `~/.claude/scheduled-tasks/atm-task-loop/SKILL.md` 创建任务文件：

```markdown
---
name: atm-task-loop
description: 每天两次从 ATM 拉取任务并执行
---

用 `atm list --status todo` 拉取待办任务，
逐一执行，完成后用 `atm update <id> --status done` 更新状态。
```

然后在 Desktop App UI 中设置频率（每天 / 每小时 / 工作日 / 每周）。

#### 第四步：配置心跳上报

在 Agent 工作区的 `HEARTBEAT.md` 中添加心跳任务，让 Agent 定期上报状态：

```python
import requests, os

requests.post("http://localhost:8000/api/v1/heartbeat", json={
    "agent_name": "my-agent",
    "agent_key": os.getenv("AGENT_TASK_KEY"),
    "status": "online",
    "tasks": [...],          # 当前任务快照
    "tokens_consumed": 1200
})
```

---

### API 端点

#### Agent 管理
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/agents` | 列出所有 Agent |
| POST | `/api/v1/agents` | 创建 Agent |
| GET | `/api/v1/agents/{id}` | Agent 详情 |
| PUT | `/api/v1/agents/{id}` | 更新 Agent |
| DELETE | `/api/v1/agents/{id}` | 删除 Agent |
| GET | `/api/v1/agents/{id}/stats` | Agent 统计 |

#### 任务管理
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/tasks` | 任务列表（支持 `date`、`agent_id`、`status` 过滤）|
| POST | `/api/v1/tasks` | 创建任务 |
| GET | `/api/v1/tasks/{id}` | 任务详情 |
| PUT | `/api/v1/tasks/{id}` | 更新任务 |
| PATCH | `/api/v1/tasks/{id}/status` | 更新任务状态 |
| DELETE | `/api/v1/tasks/{id}` | 删除任务 |

#### 日历 & 心跳
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/calendar/monthly` | 月度任务视图 |
| GET | `/api/v1/calendar/daily` | 单日任务详情 |
| POST | `/api/v1/heartbeat` | Agent 心跳上报 |

---

### 项目结构

```
agent-task-manager/
├── backend/              # FastAPI 后端 + PostgreSQL
│   ├── src/
│   │   ├── routers/      # API 路由 (tasks, agents, heartbeat, calendar)
│   │   ├── models/       # 数据库模型
│   │   └── schemas/      # Pydantic schemas
│   └── docker-compose.yml
├── frontend/
│   └── atm-frontend/     # React + TypeScript + Tailwind 面板
├── atm-client-skill/     # OpenClaw Skill CLI 工具
│   └── atm-cli.py
├── skills/               # 其他内置技能 (news-fetch 等)
└── scripts/              # 安装脚本
```

---

### 本地开发

```bash
# 后端（不用 Docker）
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload

# 前端
cd frontend/atm-frontend
cp .env.example .env
npm install
npm run dev
```
