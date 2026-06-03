"""
AI 统一调用层
支持 DeepSeek / 通义千问 / OpenAI 等 OpenAI 兼容 API
提供流式和非流式调用，支持 Function Calling
"""

import json
import requests
from flask import current_app

# 提供商默认配置
PROVIDER_DEFAULTS = {
    'deepseek': {
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat',
    },
    'qwen': {
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model': 'qwen-plus',
    },
    'openai': {
        'base_url': 'https://api.openai.com/v1',
        'model': 'gpt-4o-mini',
    },
}


def _get_ai_config():
    """从 SiteConfig 读取 AI 配置"""
    from models import SiteConfig
    cfg_row = SiteConfig.query.filter_by(config_key='system').first()
    cfg = cfg_row.config_value if cfg_row and isinstance(cfg_row.config_value, dict) else {}

    provider = cfg.get('aiProvider', 'deepseek')
    api_key = cfg.get('aiApiKey', '')
    base_url = cfg.get('aiBaseUrl', '') or PROVIDER_DEFAULTS.get(provider, {}).get('base_url', '')
    model = cfg.get('aiModel', '') or PROVIDER_DEFAULTS.get(provider, {}).get('model', '')

    return {
        'provider': provider,
        'api_key': api_key,
        'base_url': base_url.rstrip('/'),
        'model': model,
    }


def is_configured():
    """检查 AI 是否已配置"""
    cfg = _get_ai_config()
    return bool(cfg['api_key'] and cfg['base_url'] and cfg['model'])


def chat(messages, tools=None, temperature=0.7, max_tokens=2000):
    """
    非流式调用
    :param messages: [{"role": "system"/"user"/"assistant"/"tool", "content": "..."}]
    :param tools: 工具定义列表（可选）
    :return: 完整响应 dict
    """
    cfg = _get_ai_config()
    if not cfg['api_key']:
        raise ValueError('AI 未配置：请在系统设置中填写 API Key')

    headers = {
        'Authorization': f'Bearer {cfg["api_key"]}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': cfg['model'],
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
    }
    if tools:
        payload['tools'] = tools

    resp = requests.post(
        f'{cfg["base_url"]}/chat/completions',
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def chat_stream(messages, tools=None, temperature=0.7, max_tokens=2000):
    """
    流式调用，yield SSE 格式的事件
    :param messages: 消息列表
    :param tools: 工具定义列表（可选）
    :yields: (event_type: str, data: dict)
        - ("text", {"content": "..."})          — 文本片段
        - ("tool_calls", {"calls": [...]})      — 工具调用请求
        - ("done", {"finish_reason": "..."})    — 完成
        - ("error", {"message": "..."})         — 错误
    """
    cfg = _get_ai_config()
    if not cfg['api_key']:
        yield ('error', {'message': 'AI 未配置：请在系统设置中填写 API Key'})
        return

    headers = {
        'Authorization': f'Bearer {cfg["api_key"]}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': cfg['model'],
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stream': True,
    }
    if tools:
        payload['tools'] = tools

    try:
        resp = requests.post(
            f'{cfg["base_url"]}/chat/completions',
            headers=headers,
            json=payload,
            stream=True,
            timeout=120,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        yield ('error', {'message': f'AI 服务请求失败: {str(e)}'})
        return

    # 收集流式 chunk 中的 tool_calls
    accumulated_tool_calls = {}
    finish_reason = None

    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith('data: '):
            data_str = line[6:]
            if data_str.strip() == '[DONE]':
                break
            try:
                chunk = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            choice = chunk.get('choices', [{}])[0]
            delta = choice.get('delta', {})
            finish_reason = choice.get('finish_reason')

            # 文本内容
            if delta.get('content'):
                yield ('text', {'content': delta['content']})

            # 工具调用（可能分多个 chunk 到达）
            if delta.get('tool_calls'):
                for tc in delta['tool_calls']:
                    idx = tc.get('index', 0)
                    if idx not in accumulated_tool_calls:
                        accumulated_tool_calls[idx] = {
                            'id': tc.get('id', ''),
                            'type': 'function',
                            'function': {'name': '', 'arguments': ''}
                        }
                    if tc.get('id'):
                        accumulated_tool_calls[idx]['id'] = tc['id']
                    if tc.get('function', {}).get('name'):
                        accumulated_tool_calls[idx]['function']['name'] += tc['function']['name']
                    if tc.get('function', {}).get('arguments'):
                        accumulated_tool_calls[idx]['function']['arguments'] += tc['function']['arguments']

    # 如果有工具调用，yield 出来
    if accumulated_tool_calls:
        calls = [accumulated_tool_calls[i] for i in sorted(accumulated_tool_calls.keys())]
        yield ('tool_calls', {'calls': calls})
    else:
        yield ('done', {'finish_reason': finish_reason})


def execute_tool_call(tool_call):
    """
    执行单个工具调用
    :param tool_call: {"id": "...", "function": {"name": "...", "arguments": "{...}"}}
    :return: {"tool_call_id": "...", "content": "JSON string"}
    """
    from ai_tools import execute_tool
    func_name = tool_call['function']['name']
    try:
        args = json.loads(tool_call['function']['arguments'])
    except json.JSONDecodeError:
        args = {}

    try:
        result = execute_tool(func_name, args)
    except Exception as e:
        result = json.dumps({'error': str(e)}, ensure_ascii=False)

    return {
        'tool_call_id': tool_call['id'],
        'role': 'tool',
        'content': result if isinstance(result, str) else json.dumps(result, ensure_ascii=False),
    }
