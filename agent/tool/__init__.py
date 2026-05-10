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
from agent.tool.SensorWebClient import (
    SensorGetTool
)
from agent.tool.mbot import (
    MbotMotionTool
)


tool_registry = ToolRegistry()
tool_registry.register(GetCurrentTime())

tool_registry.register(ReadFileTool())

tool_registry.register(WebFetchTool())

tool_registry.register(WeatherTool())

tool_registry.register(MbotMotionTool())

tool_registry.register(SensorGetTool())

tools = tool_registry.schema()


def demo():
    import json
    print(json.dumps(tools, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    demo()

