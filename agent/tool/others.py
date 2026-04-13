from agent.tool.base import (
    Tool
)
from agent.utils import (
    to_content
)
from datetime import (
    datetime
)
from typing import (
    Any,
    List,
    Dict
)



class GetCurrentTime(Tool):
    def __init__(self):
        self.__weekdays_cn = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

    @property
    def name(self):
        return 'get_current_time'

    @property
    def description(self):
        return "获取当前的时间"

    @property
    def parameters(self):
        return {}

    async def execute(self) -> List[Dict[str, Any]]:
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d %H:%M:%S")
        weekday = self.__weekdays_cn[now.weekday()]
        return to_content(text=f"{current_time} {weekday}")