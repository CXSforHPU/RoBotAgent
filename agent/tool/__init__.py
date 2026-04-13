import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))


from agent.tool.others import (
    GetCurrentTime
)
from agent.tool.web import (
    WebFetchTool
)
from agent.tool.file import (
    ReadFileTool
)
from agent.tool.registry import (
    ToolRegistry
)
from agent.tool.weather_tool import (
    WeatherTool
)

tool_registry = ToolRegistry()
tool_registry.register(GetCurrentTime())

tool_registry.register(ReadFileTool())

tool_registry.register(WebFetchTool())

tool_registry.register(WeatherTool())

tools = tool_registry.schema()


def demo():
    import json
    print(json.dumps(tools, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    demo()

