from agent.utils import (
    to_content
)
from agent.tool.base import (
    Tool
)
import re
import html
import json
import httpx
import base64
from typing import (
    Dict,
    Any,
    Optional,
    List
)


def __strip_tag(text: str) -> str:
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()


def __normalize(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def html_to_markdown(html_content: str) -> str:
    text = html_content
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',
                  lambda m: f'[{__strip_tag(m[2])}]({m[1]})', text, flags=re.I)
    text = re.sub(r'<h([1-6])[^>]*>([\s\S]*?)</h\1>',
                  lambda m: f'\n\n{"#" * int(m[1])} {__strip_tag(m[2])}\n', text, flags=re.I)
    text = re.sub(r'<li[^>]*>([\s\S]*?)</li>',
                  lambda m: f'\n- {__strip_tag(m[1])}', text, flags=re.I)
    text = re.sub(r'</(p|div|section|article|tr)>', '\n\n', text, flags=re.I)
    text = re.sub(r'<(br)\s*/?>', '\n', text, flags=re.I)
    return __normalize(__strip_tag(text))


def parse_response_content(response: httpx.Response) -> List[Dict[str, Any]]:
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("text/plain"):
        return to_content(
            text=response.text
        )

    elif content_type.startswith("text/html"):
        return to_content(
            text=html_to_markdown(response.text)
        )

    elif content_type.startswith("application/json"):
        return to_content(
            text=json.dumps(response.json(), indent=4, ensure_ascii=False)
        )

    elif content_type.startswith("image/"):
        base64_encoding = base64.b64encode(response.content).decode('utf-8')
        return to_content(
            image=f"data:{content_type};base64,{base64_encoding}"
        )

    else:
        return to_content(
            text=f"无法解析的数据格式:{content_type}"
        )


class WebFetchTool(Tool):

    @property
    def name(self) -> str:
        return "web_fetch"

    @property
    def description(self) -> str:
        return "发送get请求，并从结果中提取可读的文本或图像内容"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "请求地址,例如https://www.baidu.com",
                },
                "params": {
                    "type": "object",
                    "description": "查询参数",
                },
            },
            "required": ["url"],
        }

    async def execute(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url,
                params=params,
            )
            response.raise_for_status()
            return parse_response_content(response)


async def demo():
    from pathlib import Path
    web_fetch = WebFetchTool()
    result = await web_fetch.execute(url="https://mhworld.kiranico.com/zh/monsters/jA8SZ/hei-long")
    markdown = result[-1]["text"]
    print(markdown)
    print(len(markdown))

    file = Path("../../workspace/1.md")
    file.write_text(markdown, encoding="utf-8")


if __name__ == '__main__':
    import asyncio
    asyncio.run(demo())
