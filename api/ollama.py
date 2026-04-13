import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))


import json
import httpx
from pydantic import (
    BaseModel
)
from typing import (
    List,
    Dict,
    Any,
    Optional,
    Callable
)
from openai import (
    AsyncClient
)
from env import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_MODEL,
    SILICONFLOW_BASE_URL,
)


BASE_URL = SILICONFLOW_BASE_URL
API_KEY = SILICONFLOW_API_KEY
MODEL = SILICONFLOW_MODEL


class ChatResponse(BaseModel):
    reasoning: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None


client = AsyncClient(
    base_url=BASE_URL,
    api_key=API_KEY,
    http_client=httpx.AsyncClient(
        proxy=None,
        trust_env=False
    )
)


async def chat(
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict]] = None,
        max_tokens: int = 32 * 1024,    # 32k
        on_reasoning: Optional[Callable] = None,
        on_content: Optional[Callable] = None,
        on_tool_calls: Optional[Callable] = None,
):
    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        max_tokens=max_tokens,
        stream=True,
        # extra_body={
        #     "top_k": 20,
        #     "mm_processor_kwargs":{
        #         "fps": 2,
        #         "do_sample_frames": True
        #     }
        # }
    )

    reasoning = ""
    content = ""
    tool_calls = []
    tool_call_map = {}

    is_answering = False    # 是否进入回复阶段
    async for chunk in response:
        delta = chunk.choices[0].delta

        if getattr(delta, "reasoning", None):
            reasoning += delta.reasoning
            if on_reasoning is not None:
                on_reasoning(delta.reasoning, end="")

        if getattr(delta, "content", None) and delta.content:
            if not is_answering:
                print()
                is_answering = True
            content += delta.content
            if on_content is not None:
                on_content(delta.content, end="")

        if getattr(delta, "tool_calls", None):
            tool_call_list = delta.tool_calls
            for tool_call in tool_call_list:
                if tool_call.index not in tool_call_map:
                    tool_call_map[tool_call.index] = tool_call
                else:
                    tool_call_map[tool_call.index].function.arguments += tool_call.function.arguments

    for tool_call in tool_call_map.values():
        tool_calls.append(tool_call.model_dump())
        if on_tool_calls is not None:
            on_tool_calls("\n" + json.dumps(tool_calls[-1], indent=4, ensure_ascii=False))

    print()
    return ChatResponse(
        reasoning=reasoning,
        content=content,
        tool_calls=tool_calls,
    )


async def main():
    from agent.tool import (
        tools
    )
    from agent.utils import (
        read_base64_image
    )

    messages = [
        {
            "role": "user",
            "content": [
                # 视频输入
                # {
                #     "type": "video_url",
                #     "video_url": {
                #         "url": f"data:image/jpeg;base64,{read_base64_video('../temp/video/1.mp4')}"
                #     }
                # },
                # 视频帧输入
                # {
                #     "type": "video",
                #     "video": [
                #         f"data:image/jpeg;base64,{read_base64_image(f'../temp/video_frames/frame_000000.jpg')}",
                #         f"data:image/jpeg;base64,{read_base64_image(f'../temp/video_frames/frame_000001.jpg')}",
                #     ],
                # },
                # 图片输入
                # {
                #     "type": "image_url",
                #     "image_url": {
                #         "url": f"data:image/jpeg;base64,{read_base64_image('../temp/video_frames/frame_000002.jpg')}"
                #     }
                # },
                # 文本输入
                {
                    "type": "text",
                    "text": "你好"
                },
            ]
        }
    ]

    response: ChatResponse = await chat(
        messages=messages,
        tools=tools,
        on_reasoning=print,
        on_content=print,
        on_tool_calls=print,
    )


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())