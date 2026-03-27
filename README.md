# Agent Task Manager

智能体每日任务管理系统

## 快速开始

### 1. 启动服务

```bash
cd projects/agent-task-manager/backend
docker-compose up -d
```

### 2. 等待数据库就绪

```bash
docker-compose logs -f db
# 看到 "database system is ready to accept connections" 即可
```

### 3. 访问 API

- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API 端点

### 智能体管理
- `GET /api/v1/agents` - 列出智能体
- `POST /api/v1/agents` - 创建智能体
- `GET /api/v1/agents/{id}` - 智能体详情
- `PUT /api/v1/agents/{id}` - 更新智能体
- `DELETE /api/v1/agents/{id}` - 删除智能体
- `GET /api/v1/agents/{id}/stats` - 智能体统计

### 任务管理
- `GET /api/v1/tasks` - 任务列表 (支持 date, agent_id, status 过滤)
- `POST /api/v1/tasks` - 创建任务
- `GET /api/v1/tasks/{id}` - 任务详情
- `PUT /api/v1/tasks/{id}` - 更新任务
- `PATCH /api/v1/tasks/{id}/status` - 更新状态
- `DELETE /api/v1/tasks/{id}` - 删除任务

### 日历视图
- `GET /api/v1/calendar/monthly?year=2024&month=3` - 月度视图
- `GET /api/v1/calendar/daily?date=2024-03-26` - 单日详情

### 心跳上报
- `POST /api/v1/heartbeat` - 智能体状态上报

## OpenClaw 集成

### 1. 创建智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "description": "My OpenClaw Agent"}'
```

响应中会包含 `api_key`，保存好用于心跳上报。

### 2. 配置 HEARTBEAT.md

在你的 OpenClaw 工作区添加:

```markdown
## Agent Task Manager Integration

### 上报任务状态

```python
import requests
import os

AGENT_NAME = "my-agent"
AGENT_KEY = os.getenv("AGENT_TASK_KEY", "your-api-key")
API_URL = "http://localhost:8000/api/v1/heartbeat"

def report_status(tasks_data, tokens_used=0):
    response = requests.post(API_URL, json={
        "agent_name": AGENT_NAME,
        "agent_key": AGENT_KEY,
        "status": "online",
        "tasks": tasks_data,
        "tokens_consumed": tokens_used
    })
    return response.json()
```
```

### 3. 配置 Cron Job

```json
{
  "name": "agent-status-report",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "payload": {
    "kind": "agentTurn",
    "message": "Report current task status to Agent Task Manager"
  }
}
```

## 前端启动

### 1. 安装依赖
```bash
cd frontend/atm-frontend
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

### 3. 访问前端
打开 http://localhost:5173

## 完整启动（前后端）

```bash
# 终端 1: 启动后端
cd backend
docker-compose up -d

# 终端 2: 启动前端
cd frontend/atm-frontend
npm run dev

# 访问:
# - 前端: http://localhost:5173
# - 后端 API: http://localhost:8000/docs
```

## 开发

### 后端开发
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload
```

### 前端开发
```bash
cd frontend/atm-frontend
npm install
npm run dev
```
