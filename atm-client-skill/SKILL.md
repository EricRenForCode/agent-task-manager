# ATM Client Skill

与 Agent Task Manager (ATM) 交互的 OpenClaw Skill。

## 功能

- 创建任务
- 列出任务
- 查看任务详情
- 更新任务状态
- 删除任务

## 用法

### 创建任务
```bash
atm create --title "任务标题" --description "任务描述" --priority high --agent kicker
```

### 列出任务
```bash
atm list                    # 列出所有待办任务
atm list --status ongoing   # 列出进行中任务
atm list --agent kicker     # 列出指定 agent 的任务
```

### 查看任务
```bash
atm get <task-id>
```

### 更新任务
```bash
atm update <task-id> --status done
atm update <task-id> --priority low
```

### 删除任务
```bash
atm delete <task-id>
```

## 环境变量

- `ATM_API_BASE`: ATM API 地址 (默认: http://localhost:8000/api/v1)
