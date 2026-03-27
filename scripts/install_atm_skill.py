#!/usr/bin/env python3
"""
ATM Skill Generator & Installer
生成 Agent Task Manager skill 并安装到 OpenClaw

用法:
    python3 install_atm_skill.py
"""

import os
import subprocess
import sys
from pathlib import Path

# 配置
SKILL_NAME = "atm-client"
SKILL_SOURCE_DIR = Path("/Users/eric/Documents/dev/agent-task-manager/atm-client-skill")
SKILL_INSTALL_DIR = Path.home() / ".openclaw" / "skills" / SKILL_NAME
ATM_API_BASE = "http://localhost:8000/api/v1"

def generate_atm_cli():
    """生成 atm-cli.py 内容"""
    return '''#!/usr/bin/env python3
"""
ATM CLI - Agent Task Manager 命令行工具
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ATM_API_BASE = os.getenv("ATM_API_BASE", "''' + ATM_API_BASE + '''")

def api_request(method, endpoint, data=None):
    """发送 API 请求"""
    url = f"{ATM_API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
        req = Request(url, data=data, headers=headers, method=method)
        
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        print(f"API 错误: {e.code} - {e.reason}")
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            print(f"详情: {error_body}")
        except:
            pass
        return None
    except URLError as e:
        print(f"连接错误: {e.reason}")
        print(f"请检查 ATM 服务是否运行在 {ATM_API_BASE}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def create_task(args):
    """创建任务"""
    data = {
        "title": args.title,
        "description": args.description or "",
        "status": "todo",
        "priority": args.priority or "medium",
        "agent_id": args.agent or "kicker"
    }
    
    result = api_request("POST", "/tasks", data)
    if result:
        print("✅ 任务创建成功")
        print(f"   ID: {result.get('id')}")
        print(f"   标题: {result.get('title')}")
        print(f"   优先级: {result.get('priority')}")
        print(f"   Agent: {result.get('agent_id')}")
    return result

def list_tasks(args):
    """列出任务"""
    params = []
    if args.status:
        params.append(f"status={args.status}")
    if args.agent:
        params.append(f"agent_id={args.agent}")
    
    endpoint = "/tasks"
    if params:
        endpoint += "?" + "&".join(params)
    
    result = api_request("GET", endpoint)
    if result and "items" in result:
        items = result["items"]
        if not items:
            print("📭 没有找到任务")
            return
        
        print(f"📋 找到 {len(items)} 个任务:")
        print()
        print(f"{'ID':<36} {'状态':<10} {'优先级':<8} {'Agent':<15} {'标题'}")
        print("-" * 100)
        
        for task in items:
            task_id = task.get('id', '')[:8] + "..."
            status = task.get('status', 'unknown')
            priority = task.get('priority', 'medium')
            agent = task.get('agent_id', '')[:14]
            title = task.get('title', '')[:40]
            print(f"{task_id:<36} {status:<10} {priority:<8} {agent:<15} {title}")
    return result

def get_task(args):
    """获取任务详情"""
    result = api_request("GET", f"/tasks/{args.task_id}")
    if result:
        print("📄 任务详情:")
        print()
        print(f"   ID: {result.get('id')}")
        print(f"   标题: {result.get('title')}")
        print(f"   描述: {result.get('description') or '(无)'}")
        print(f"   状态: {result.get('status')}")
        print(f"   优先级: {result.get('priority')}")
        print(f"   Agent: {result.get('agent_id')}")
        print(f"   创建时间: {result.get('created_at')}")
        print(f"   更新时间: {result.get('updated_at')}")
    return result

def update_task(args):
    """更新任务"""
    data = {}
    if args.status:
        data["status"] = args.status
    if args.priority:
        data["priority"] = args.priority
    if args.title:
        data["title"] = args.title
    if args.description:
        data["description"] = args.description
    
    if not data:
        print("❌ 请指定要更新的字段 (--status, --priority, --title, --description)")
        return
    
    result = api_request("PUT", f"/tasks/{args.task_id}", data)
    if result:
        print("✅ 任务更新成功")
        print(f"   ID: {result.get('id')}")
        print(f"   标题: {result.get('title')}")
        print(f"   状态: {result.get('status')}")
        print(f"   优先级: {result.get('priority')}")
    return result

def delete_task(args):
    """删除任务"""
    # 先获取任务信息确认
    task = api_request("GET", f"/tasks/{args.task_id}")
    if not task:
        return
    
    print(f"即将删除任务: {task.get('title')} ({args.task_id})")
    
    if not args.force:
        confirm = input("确认删除? [y/N]: ")
        if confirm.lower() != 'y':
            print("已取消")
            return
    
    result = api_request("DELETE", f"/tasks/{args.task_id}")
    if result is not None:
        print("✅ 任务已删除")
    return result

def main():
    parser = argparse.ArgumentParser(
        prog='atm',
        description='Agent Task Manager CLI'
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create
    create_parser = subparsers.add_parser('create', help='创建任务')
    create_parser.add_argument('--title', '-t', required=True, help='任务标题')
    create_parser.add_argument('--description', '-d', help='任务描述')
    create_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                               default='medium', help='优先级 (默认: medium)')
    create_parser.add_argument('--agent', '-a', default='kicker', help='Agent ID (默认: kicker)')
    
    # list
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', '-s', choices=['todo', 'ongoing', 'done'],
                            help='按状态筛选')
    list_parser.add_argument('--agent', '-a', help='按 Agent 筛选')
    
    # get
    get_parser = subparsers.add_parser('get', help='查看任务详情')
    get_parser.add_argument('task_id', help='任务 ID')
    
    # update
    update_parser = subparsers.add_parser('update', help='更新任务')
    update_parser.add_argument('task_id', help='任务 ID')
    update_parser.add_argument('--status', '-s', choices=['todo', 'ongoing', 'done'],
                              help='更新状态')
    update_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'],
                              help='更新优先级')
    update_parser.add_argument('--title', '-t', help='更新标题')
    update_parser.add_argument('--description', '-d', help='更新描述')
    
    # delete
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('task_id', help='任务 ID')
    delete_parser.add_argument('--force', '-f', action='store_true',
                              help='强制删除，不提示确认')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 路由到对应函数
    commands = {
        'create': create_task,
        'list': list_tasks,
        'get': get_task,
        'update': update_task,
        'delete': delete_task
    }
    
    result = commands[args.command](args)
    sys.exit(0 if result is not None else 1)

if __name__ == '__main__':
    main()
'''

# Skill 文件内容
SKILL_MD = '''# ATM Client Skill

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
'''

PACKAGE_JSON = '''{
  "name": "atm-client-skill",
  "version": "1.0.0",
  "description": "Agent Task Manager client skill for OpenClaw",
  "bin": {
    "atm": "./atm-cli.py"
  },
  "scripts": {
    "postinstall": "chmod +x atm-cli.py"
  }
}
'''

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def main():
    print("🚀 ATM Skill 生成器\n")
    
    # 1. 创建 skill 源目录（在开发目录）
    print(f"📁 创建 skill 源目录: {SKILL_SOURCE_DIR}")
    SKILL_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. 写入文件
    print("📝 生成 skill 文件...")
    
    # SKILL.md
    (SKILL_SOURCE_DIR / "SKILL.md").write_text(SKILL_MD)
    print(f"   ✓ SKILL.md")
    
    # atm-cli.py
    cli_path = SKILL_SOURCE_DIR / "atm-cli.py"
    cli_path.write_text(generate_atm_cli())
    cli_path.chmod(0o755)
    print(f"   ✓ atm-cli.py")
    
    # package.json
    (SKILL_SOURCE_DIR / "package.json").write_text(PACKAGE_JSON)
    print(f"   ✓ package.json")
    
    # 3. 安装到 OpenClaw
    print("\n📦 安装 skill 到 OpenClaw...")
    
    # 检查 openclaw 命令
    if not run_command(["which", "openclaw"]):
        print("❌ 未找到 openclaw 命令，请确保 OpenClaw 已安装")
        sys.exit(1)
    
    # 安装到 OpenClaw skills 目录（直接复制，不使用符号链接避免循环）
    import shutil
    
    # 如果已存在，先删除
    if SKILL_INSTALL_DIR.exists():
        print(f"   移除旧的 skill 安装...")
        shutil.rmtree(SKILL_INSTALL_DIR)
    
    # 复制文件
    shutil.copytree(SKILL_SOURCE_DIR, SKILL_INSTALL_DIR)
    print(f"   ✓ 复制 skill 到: {SKILL_INSTALL_DIR}")
    
    # 4. 验证安装
    print("\n🔍 验证安装...")
    if run_command(["openclaw", "skills", "list"]):
        print("   ✓ OpenClaw skill 列表正常")
    
    # 5. 测试 CLI
    print("\n🧪 测试 ATM CLI...")
    atm_cli = SKILL_INSTALL_DIR / "atm-cli.py"
    run_command(["python3", str(atm_cli), "--help"])
    
    print("\n" + "="*60)
    print("✅ ATM Skill 安装完成!")
    print("="*60)
    print(f"\n📍 Skill 源位置: {SKILL_SOURCE_DIR}")
    print(f"📍 Skill 安装位置: {SKILL_INSTALL_DIR}")
    print("\n💡 使用方法:")
    print(f"   python3 {SKILL_INSTALL_DIR / 'atm-cli.py'} --help")
    print(f"   python3 {SKILL_INSTALL_DIR / 'atm-cli.py'} create --title '测试任务' --priority high")
    print(f"   python3 {SKILL_INSTALL_DIR / 'atm-cli.py'} list")
    print(f"   python3 {SKILL_INSTALL_DIR / 'atm-cli.py'} get <task-id>")
    print("\n📝 或者添加到你的 PATH:")
    print(f"   export PATH=\"{SKILL_INSTALL_DIR}:$PATH\"")
    print(f"   atm --help")
    print("\n⚙️  环境变量:")
    print(f"   export ATM_API_BASE=\"{ATM_API_BASE}\"")
    print("="*60)

if __name__ == '__main__':
    main()
