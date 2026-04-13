import httpx
import json

from agent.tool.base import (
    Tool
)

from agent.utils import (
    format_image,
    format_text,
    to_content
)
from typing import (
    Dict,
    List,
    Any
)
class WeatherTool(Tool):
    """
    一个用于查询指定城市当前天气的工具
    """

    @property
    def name(self) -> str:
        return "get_current_weather"

    @property
    def description(self) -> str:
        return "获取指定城市的当前天气状况，包括温度、湿度和天气描述。"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "需要查询天气的城市名称，例如：北京、上海、深圳"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位，默认为摄氏度(celsius)",
                    "default": "celsius"
                }
            },
            "required": ["city"]
        }

    async def execute(self, **kwargs: Any) -> List[Dict[str, Any]]:
        city = kwargs.get("city")
        unit = kwargs.get("unit", "celsius")
        
        # 模拟 API 调用或实际请求逻辑
        # 这里为了演示，使用假数据。实际项目中应替换为真实的天气 API 请求
        print(f"[WeatherTool] 正在查询 {city} 的天气...")
        
        # 模拟网络延迟
        import asyncio
        await asyncio.sleep(1)

        # 模拟返回结果
        mock_data = {
            "city": city,
            "temperature": 25 if unit == "celsius" else 77,
            "unit": unit,
            "condition": "晴朗",
            "humidity": "45%"
        }
        mock_data_str = json.dumps(mock_data,ensure_ascii=False)
        # 返回格式必须符合 List[Dict[str, Any]]
        return to_content(text=mock_data_str)