# Agent Task Manager - Implementation Specs

## Spec 1: 项目初始化和基础架构

### 验收标准
- [ ] 创建完整的项目目录结构
- [ ] 配置 pyproject.toml 和 requirements.txt
- [ ] 创建 Dockerfile 和 docker-compose.yml
- [ ] 配置 Alembic 数据库迁移
- [ ] 基础 FastAPI 应用可运行

### 文件清单
- docker-compose.yml
- Dockerfile
- requirements.txt
- pyproject.toml
- alembic.ini
- src/main.py
- src/config.py
- src/database.py

---

## Spec 2: 数据库模型实现

### 验收标准
- [ ] Agent 模型实现 (含关系)
- [ ] Task 模型实现 (含状态枚举)
- [ ] HeartbeatLog 模型实现
- [ ] 所有模型通过 Alembic 生成迁移
- [ ] 数据库表创建成功

### 文件清单
- src/models/__init__.py
- src/models/agent.py
- src/models/task.py
- src/models/heartbeat.py
- migrations/versions/*.py

---

## Spec 3: Pydantic Schemas

### 验收标准
- [ ] Agent 相关 schemas (Create, Update, Response)
- [ ] Task 相关 schemas (Create, Update, Response, StatusUpdate)
- [ ] Heartbeat schemas (Request, Response)
- [ ] Calendar 相关 schemas
- [ ] 所有 schemas 包含字段验证

### 文件清单
- src/schemas/__init__.py
- src/schemas/agent.py
- src/schemas/task.py
- src/schemas/heartbeat.py
- src/schemas/calendar.py

---

## Spec 4: API Routers - Agents

### 验收标准
- [ ] GET /agents - 列表查询 (支持分页)
- [ ] POST /agents - 创建智能体
- [ ] GET /agents/{id} - 详情查询
- [ ] PUT /agents/{id} - 更新智能体
- [ ] DELETE /agents/{id} - 删除智能体
- [ ] GET /agents/{id}/stats - 统计信息
- [ ] 所有端点返回正确的 HTTP 状态码

### 文件清单
- src/routers/agents.py

---

## Spec 5: API Routers - Tasks

### 验收标准
- [ ] GET /tasks - 列表查询 (支持过滤: date, agent_id, status)
- [ ] POST /tasks - 创建任务
- [ ] GET /tasks/{id} - 详情查询
- [ ] PUT /tasks/{id} - 更新任务
- [ ] DELETE /tasks/{id} - 删除任务
- [ ] PATCH /tasks/{id}/status - 状态更新
- [ ] 查询参数验证正确

### 文件清单
- src/routers/tasks.py

---

## Spec 6: API Routers - Calendar

### 验收标准
- [ ] GET /calendar/monthly - 月度视图数据
- [ ] GET /calendar/daily - 单日详情
- [ ] 返回正确的任务统计 (todo/ongoing/done)
- [ ] 包含 token 消耗统计
- [ ] 日期格式正确

### 文件清单
- src/routers/calendar.py

---

## Spec 7: API Routers - Heartbeat

### 验收标准
- [ ] POST /heartbeat - 接收智能体上报
- [ ] API Key 认证验证
- [ ] 自动创建/更新任务
- [ ] 记录心跳日志
- [ ] 返回同步结果

### 文件清单
- src/routers/heartbeat.py
- src/services/heartbeat_service.py

---

## Spec 8: Services 层

### 验收标准
- [ ] AgentService - 智能体 CRUD 和统计
- [ ] TaskService - 任务管理和查询
- [ ] HeartbeatService - 心跳处理逻辑
- [ ] 业务逻辑与路由分离
- [ ] 错误处理完善

### 文件清单
- src/services/agent_service.py
- src/services/task_service.py
- src/services/heartbeat_service.py

---

## Spec 9: 认证与权限

### 验收标准
- [ ] API Key 中间件实现
- [ ] JWT 认证 (可选，用于未来 Web UI)
- [ ] 心跳端点需要 API Key
- [ ] 管理端点需要认证
- [ ] 错误响应统一格式

### 文件清单
- src/auth/__init__.py
- src/auth/api_key.py
- src/auth/jwt.py

---

## Spec 10: 测试和文档

### 验收标准
- [ ] 单元测试覆盖主要服务
- [ ] API 集成测试
- [ ] API 文档自动生成 (/docs)
- [ ] README 文档完整
- [ ] Docker 部署测试通过

### 文件清单
- tests/conftest.py
- tests/test_agents.py
- tests/test_tasks.py
- tests/test_heartbeat.py
- README.md

---

**输出完成信号:** `<promise>DONE</promise>`
