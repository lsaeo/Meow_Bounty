"""DeepSeek API converter — transforms todo items into medieval quest names."""

import json
import urllib.request
import urllib.error


def convert_task(task_name, settings, timeout=10):
    """Call DeepSeek API to convert task_name. Returns converted string or None on failure."""

    api_key = settings.get('api_key', '').strip()
    api_base = settings.get('api_base', 'https://api.deepseek.com').strip().rstrip('/')
    model = settings.get('model', 'deepseek-chat').strip()
    system_prompt = settings.get('system_prompt', '').strip()

    if not api_key:
        return None

    url = f'{api_base}/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    body = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'请把这个待办转化为悬赏任务名（15字以内，只输出任务名）：{task_name}'},
        ],
        'max_tokens': 50,
        'temperature': 0.8,
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['choices'][0]['message']['content'].strip()
            # Strip quotes and markdown
            content = content.strip('\'"`「」『』')
            if len(content) > 25:
                content = content[:25]
            return content if content else None
    except (urllib.error.URLError, urllib.error.HTTPError,
            json.JSONDecodeError, KeyError, IndexError, OSError) as e:
        print(f'[AI] Error: {e}')
        return None
