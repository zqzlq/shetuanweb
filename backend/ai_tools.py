"""
AI 工具定义与执行器
定义 Function Calling 的工具 schema，封装资源中心数据库查询
"""

import json
from datetime import datetime, timezone

# ─── 工具 Schema 定义 ───

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_resources",
            "description": "搜索资源中心的文件和文件夹。根据关键词搜索资源名称和描述，可选按标签过滤。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词，匹配资源名称和描述"
                    },
                    "tag": {
                        "type": "string",
                        "description": "按标签过滤（可选），精确匹配标签名"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_resource_detail",
            "description": "获取某个资源的详细信息，包括描述、标签、下载次数、上传者等。需要资源 ID。",
            "parameters": {
                "type": "object",
                "properties": {
                    "resource_id": {
                        "type": "integer",
                        "description": "资源的数字 ID"
                    }
                },
                "required": ["resource_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_recent_resources",
            "description": "获取最近上传的资源列表，按上传时间倒序排列。",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "返回数量，默认 10，最大 30"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_resource_stats",
            "description": "获取资源中心的统计数据，包括总文件数、总大小、各标签数量、热门资源等。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_folders",
            "description": "列出所有文件夹及其完整路径，帮助了解资源中心的目录结构。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_download_link",
            "description": "为某个资源生成下载链接。用户点击后可直接下载文件。",
            "parameters": {
                "type": "object",
                "properties": {
                    "resource_id": {
                        "type": "integer",
                        "description": "资源的数字 ID"
                    }
                },
                "required": ["resource_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """你是「星雨作坊」资源中心的 AI 助手。

## 你的能力
- 搜索资源中心的文件和文件夹
- 查看资源详情、统计信息
- 列出最近上传的资源
- 为用户推荐相关资源
- 生成文件下载链接

## 搜索策略
- 搜索会匹配文件名、原始文件名、描述中的关键词
- 当用户搜索宽泛主题时（如"前端"、"Python"），用该主题词直接搜索
- 如果第一次搜索结果太少，尝试用相关词再搜一次（如搜"前端"没结果，试试"Vue"、"React"、"HTML"）
- 可以多次调用搜索工具，用不同关键词覆盖更多结果
- 搜索范围是整个资源库所有文件夹，不受当前目录限制

## 回复规范
- 使用中文，语气简洁友好
- 提到文件名时必须用 **加粗** 格式，如 **Python学习笔记.md**
- 列出资源时用编号列表，格式示例：
  1. **文件名.pdf** — 2.3MB，张三上传
  2. **文件名.docx** — 1.1MB，李四上传
- 找到资源后直接列出，不要反问用户是否需要下载（界面已有下载按钮）
- 当用户说"下载"、"需要"、"给我"等意图获取资源时，立即调用 get_download_link 工具
- 记住上下文中提到过的资源 ID，用户提及"这个"、"第一个"、"那个"时使用对应的 ID
- 没找到资源时建议换个关键词或查看最近上传
- 不要编造不存在的资源
- 回复控制在 300 字以内
- 禁止使用 emoji 表情符号"""


# ─── 工具执行函数 ───

def execute_tool(name, args):
    """
    执行工具调用，返回 JSON 字符串结果
    """
    executors = {
        'search_resources': _search_resources,
        'get_resource_detail': _get_resource_detail,
        'list_recent_resources': _list_recent_resources,
        'get_resource_stats': _get_resource_stats,
        'list_folders': _list_folders,
        'get_download_link': _get_download_link,
    }

    executor = executors.get(name)
    if not executor:
        return json.dumps({'error': f'未知工具: {name}'}, ensure_ascii=False)

    try:
        result = executor(**args)
        return json.dumps(result, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({'error': f'工具执行失败: {str(e)}'}, ensure_ascii=False)


def _search_resources(keyword, tag=None):
    """搜索资源 - 搜索整个资源库的所有文件夹"""
    from models import db, Resource

    query = Resource.query.filter_by(status='approved', is_folder=False)

    if keyword:
        like_pattern = f'%{keyword}%'
        # 搜索文件名、原始文件名、描述、扩展名、标签
        conditions = [
            Resource.name.ilike(like_pattern),
            Resource.original_name.ilike(like_pattern),
            Resource.description.ilike(like_pattern),
            Resource.file_ext.ilike(like_pattern),
        ]
        # SQLite 的 JSON 字符串搜索
        conditions.append(Resource.tags.cast(db.String).ilike(like_pattern))
        query = query.filter(db.or_(*conditions))

    if tag:
        query = query.filter(Resource.tags.cast(db.String).ilike(f'%{tag}%'))

    resources = query.order_by(Resource.updated_at.desc()).limit(30).all()

    results = []
    for r in resources:
        folder_path = _get_folder_path(r)
        results.append({
            'id': r.id,
            'name': r.original_name or r.name,
            'parent_id': r.parent_id,
            'folder': folder_path,
            'tags': r.tags or [],
            'description': (r.description[:100] + '...') if r.description and len(r.description) > 100 else r.description,
            'size': _format_size(r.file_size),
            'file_ext': r.file_ext,
            'uploader': r.uploader.name if r.uploader else None,
            'download_count': r.download_count,
            'updated_at': r.updated_at.strftime('%Y-%m-%d') if r.updated_at else None,
        })

    return {
        'count': len(results),
        'keyword': keyword,
        'tag': tag,
        'results': results,
    }


def _get_resource_detail(resource_id):
    """获取资源详情"""
    from models import Resource

    r = Resource.query.filter_by(id=resource_id, status='approved').first()
    if not r:
        return {'error': '资源不存在或未审核'}

    folder_path = _get_folder_path(r)
    return {
        'id': r.id,
        'name': r.original_name or r.name,
        'parent_id': r.parent_id,
        'is_folder': r.is_folder,
        'folder': folder_path,
        'tags': r.tags or [],
        'description': r.description,
        'file_ext': r.file_ext,
        'size': _format_size(r.file_size),
        'mime_type': r.mime_type,
        'uploader': r.uploader.name if r.uploader else None,
        'download_count': r.download_count,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else None,
        'updated_at': r.updated_at.strftime('%Y-%m-%d %H:%M') if r.updated_at else None,
    }


def _list_recent_resources(limit=10):
    """列出最近上传的资源"""
    from models import Resource

    limit = min(limit or 10, 30)
    resources = (
        Resource.query
        .filter_by(status='approved', is_folder=False)
        .order_by(Resource.created_at.desc())
        .limit(limit)
        .all()
    )

    results = []
    for r in resources:
        folder_path = _get_folder_path(r)
        results.append({
            'id': r.id,
            'name': r.original_name or r.name,
            'parent_id': r.parent_id,
            'folder': folder_path,
            'tags': r.tags or [],
            'file_ext': r.file_ext,
            'size': _format_size(r.file_size),
            'uploader': r.uploader.name if r.uploader else None,
            'created_at': r.created_at.strftime('%Y-%m-%d') if r.created_at else None,
        })

    return {'count': len(results), 'results': results}


def _get_resource_stats():
    """获取资源统计"""
    from models import Resource, db

    total_files = Resource.query.filter_by(status='approved', is_folder=False).count()
    total_folders = Resource.query.filter_by(status='approved', is_folder=True).count()

    # 总大小
    total_size_result = db.session.query(
        db.func.coalesce(db.func.sum(Resource.file_size), 0)
    ).filter_by(status='approved', is_folder=False).scalar()

    # 标签统计
    all_resources = Resource.query.filter_by(status='approved', is_folder=False).filter(Resource.tags.isnot(None)).all()
    tag_counts = {}
    for r in all_resources:
        for t in (r.tags or []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # 热门资源 Top 5
    popular = (
        Resource.query
        .filter_by(status='approved', is_folder=False)
        .order_by(Resource.download_count.desc())
        .limit(5)
        .all()
    )
    popular_list = [
        {'name': r.original_name or r.name, 'downloads': r.download_count}
        for r in popular
    ]

    return {
        'total_files': total_files,
        'total_folders': total_folders,
        'total_size': _format_size(total_size_result),
        'top_tags': [{'name': t[0], 'count': t[1]} for t in top_tags],
        'popular_resources': popular_list,
    }


def _list_folders():
    """列出所有文件夹"""
    from models import Resource

    folders = Resource.query.filter_by(status='approved', is_folder=True).order_by(Resource.name).all()
    folder_map = {f.id: f for f in folders}

    def build_path(fid):
        parts = []
        current = folder_map.get(fid)
        while current:
            parts.insert(0, current.name)
            current = folder_map.get(current.parent_id)
        return ' / '.join(parts) if parts else '根目录'

    results = [
        {'id': f.id, 'name': f.name, 'path': build_path(f.id)}
        for f in folders
    ]
    return {'count': len(results), 'folders': results}


def _get_download_link(resource_id):
    """生成下载链接"""
    from models import Resource

    r = Resource.query.filter_by(id=resource_id, status='approved', is_folder=False).first()
    if not r:
        return {'error': '资源不存在或未审核'}

    return {
        'id': r.id,
        'name': r.original_name or r.name,
        'download_url': f'/api/resources/{r.id}/download',
        'message': f'下载链接已生成，点击可下载「{r.original_name or r.name}」',
    }


# ─── 辅助函数 ───

def _get_folder_path(resource):
    """获取资源所在的文件夹路径"""
    from models import Resource

    parts = []
    current = resource
    while current.parent_id:
        parent = Resource.query.get(current.parent_id)
        if not parent:
            break
        parts.insert(0, parent.name)
        current = parent
    return ' / '.join(parts) if parts else '根目录'


def _format_size(size_bytes):
    """格式化文件大小"""
    if not size_bytes:
        return '未知'
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.1f} KB'
    elif size_bytes < 1024 * 1024 * 1024:
        return f'{size_bytes / (1024 * 1024):.1f} MB'
    else:
        return f'{size_bytes / (1024 * 1024 * 1024):.2f} GB'
