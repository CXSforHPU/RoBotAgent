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


class ToolRegistry:
    def __init__(self):
        self.__tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        if tool.name in self.__tools:
            print(f"工具 {tool.name} 已经注册过了。")
            return
        self.__tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        if name in self.__tools:
            return self.__tools[name]
        print(f"工具 {name} 未注册。")
        return None

    async def execute(
            self,
            name: str,
            arguments: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        tool = self.get(name)
        if tool is None:
            return to_content(text=f"工具{name}不存在")

        try:
            return await tool.execute(**arguments)
        except Exception as error:
            return to_content(
                text=f"调用{name}工具时遇到错误: {error}"
            )

    def schema(self):
        data = []
        for tool in self.__tools.values():
            data.append(tool.schema())
        return data

    def __len__(self):
        return len(self.__tools)

    def __contains__(self, name):
        return name in self.__tools

