from env import (
    WORKSPACE_PATH
)
from agent.utils import (
    format_text,
    to_content
)
from pathlib import (
    Path,
)
from agent.tool.base import (
    Tool
)
from typing import (
    List,
    Dict,
    Any,
)


class ReadFileTool(Tool):

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "读取文件的文本内容"

    @property
    def parameters(self) -> Dict[str, str]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "待读取的文件路径"
                }
            },
            "required": ["path"]
        }

    async def execute(self, path: str) -> List[Dict[str, Any]]:
        file_path = Path(path)
        if not file_path.exists():
            return to_content(text=f"{file_path}路径不存在。")

        if not file_path.is_file():
            return to_content(text=f"{file_path}并不是文件。")

        content = file_path.read_text(encoding="utf-8")
        return to_content(text=content)
