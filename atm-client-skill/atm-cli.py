#!/usr/bin/env python3
"""
ATM CLI - Agent Task Manager 命令行工具
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ATM_API_BASE = os.getenv("ATM_API_BASE", "http://localhost:8000/api/v1")

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
