import sys
import os
import time as tm
# 兼容项目路径（和你原有代码一致）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 从环境配置读取机械臂服务地址
from env import (
    MBOT_MOTION_URL,
    MBOT_MOTTION_PORT,
)
# 继承Agent核心基类
from agent.tool.base import Tool
from agent.utils import to_content
from typing import Any, List, Dict
import requests
from requests.exceptions import RequestException

# ==================== 命令常量定义 ====================

CMD_GO_HOME_POSITION = 1
CMD_COLOR_CALIBRATION = 4
CMD_GO_SORTING_POSITION = 5
CMD_GO_CAMERA_POSITION = 6

CMD_MOVE_LEFT = 16
CMD_MOVE_RIGHT = 17
CMD_MOVE_UP = 18
CMD_MOVE_DOWN = 19
CMD_MOVE_FORWARD = 20
CMD_MOVE_BACKWARD = 21

CMD_COLOR_RECOGNITION = 48
CMD_SHAPE_RECOGNITION = 49
CMD_QRCODE_RECOGNITION = 50
CMD_DRUG_IDENTIFICATION = 51
CMD_GARBAGE_IDENTIFICATION = 52
CMD_CHARACTERS_IDENTIFICATION = 53

CMD_PLACE_IN_WAREHOUSES_1 = 54
CMD_PLACE_IN_WAREHOUSES_2 = 55
CMD_PLACE_IN_WAREHOUSES_3 = 56
CMD_PLACE_IN_WAREHOUSES_4 = 57

CMD_COLOR_SORTING = 58
CMD_SHAPE_SORTING = 59
CMD_QRCODE_SORTING = 60
CMD_DRUG_SORTING = 61
CMD_GARBAGE_SORTING = 62
CMD_CHARACTERS_SORTING = 63

CMD_FACE_TRACKING = 64
CMD_GUESSING_FISTS_GAME = 65
CMD_STACKING_GAME = 67

CMD_SORTING = 201
CMD_RECOGNITION = 202
CMD_TRACKING = 203

CMD_EXEC_SUCCESS = 1
CMD_EXEC_FAIL = 2
CMD_MESSAGE_RESPONSE = 16

# 命令字符串到数字的映射
COMMAND_MAP = {
    'go_home': CMD_GO_HOME_POSITION,
    'go_home_position': CMD_GO_HOME_POSITION,
    'color_calibration': CMD_COLOR_CALIBRATION,
    'go_sorting_position': CMD_GO_SORTING_POSITION,
    'go_camera_position': CMD_GO_CAMERA_POSITION,
    'move_left': CMD_MOVE_LEFT,
    'move_right': CMD_MOVE_RIGHT,
    'move_up': CMD_MOVE_UP,
    'move_down': CMD_MOVE_DOWN,
    'move_forward': CMD_MOVE_FORWARD,
    'move_backward': CMD_MOVE_BACKWARD,
    'color_recognition': CMD_COLOR_RECOGNITION,
    'shape_recognition': CMD_SHAPE_RECOGNITION,
    'qrcode_recognition': CMD_QRCODE_RECOGNITION,
    'drug_identification': CMD_DRUG_IDENTIFICATION,
    'garbage_identification': CMD_GARBAGE_IDENTIFICATION,
    'characters_identification': CMD_CHARACTERS_IDENTIFICATION,
    'place_in_warehouse_1': CMD_PLACE_IN_WAREHOUSES_1,
    'place_in_warehouse_2': CMD_PLACE_IN_WAREHOUSES_2,
    'place_in_warehouse_3': CMD_PLACE_IN_WAREHOUSES_3,
    'place_in_warehouse_4': CMD_PLACE_IN_WAREHOUSES_4,
    'color_sorting': CMD_COLOR_SORTING,
    'shape_sorting': CMD_SHAPE_SORTING,
    'qrcode_sorting': CMD_QRCODE_SORTING,
    'drug_sorting': CMD_DRUG_SORTING,
    'garbage_sorting': CMD_GARBAGE_SORTING,
    'characters_sorting': CMD_CHARACTERS_SORTING,
    'face_tracking': CMD_FACE_TRACKING,
    'guessing_fists_game': CMD_GUESSING_FISTS_GAME,
    'stacking_game': CMD_STACKING_GAME,
}

COMMAND_MAP_REVERSE = {v: k for k, v in COMMAND_MAP.items()}


# ==================== HTTP客户端 ====================
class MbotMotionWebClient:
    """
    机械臂控制服务纯Python客户端
    对接ROS+Flask服务端的 /task/execute、/commands、/health 接口
    """
    def __init__(self, host: str = MBOT_MOTION_URL, port: int = MBOT_MOTTION_PORT):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.timeout = 5

    def execute_command(self, cmd: str, data1: int = 0, data2: int = 0) -> Dict[str, Any] | None:
        """
        执行机械臂命令
        返回：{'success': True/False, 'cmd_code': ..., 'cmd_name': ..., 'message': ...}
        """
        try:
            res = self.session.post(
                f"{self.base_url}/task/execute",
                json={"cmd": cmd, "data1": data1, "data2": data2},
            )
            res.raise_for_status()
            return res.json()
        except RequestException:
            return None

    def list_commands(self) -> Dict[str, Any] | None:
        """获取所有可用命令列表"""
        try:
            res = self.session.get(f"{self.base_url}/commands")
            res.raise_for_status()
            return res.json().get("commands")
        except RequestException:
            return None

    def health_check(self) -> bool:
        """检查服务健康状态"""
        try:
            res = self.session.get(f"{self.base_url}/health")
            res.raise_for_status()
            return True
        except RequestException:
            return False


# ==================== Agent工具 ====================
class MbotMotionTool(Tool):
    """
    机械臂控制工具（Agent专用）
    支持：移动、识别、分类、定位、游戏等机械臂命令
    完全对齐原有工具规范，无缝集成Agent
    """
    def __init__(self):
        super().__init__()
        self.client = MbotMotionWebClient(host=MBOT_MOTION_URL, port=MBOT_MOTTION_PORT)

    @property
    def name(self):
        return 'mbot_motion'

    @property
    def description(self):
        return "控制机械臂运动：执行移动、颜色/形状/二维码识别、分类放置、定位校准、互动游戏等机械臂命令"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": (
                        "操作类型：move(移动)、recognize(识别)、sort(分类)、place(放置)、"
                        "position(定位)、game(游戏)、calibration(校准)、list(列出可用命令)"
                    )
                },
                "command": {
                    "type": "string",
                    "description": (
                        "具体命令名称，根据action类型选择：\n"
                        "move: move_left/move_right/move_up/move_down/move_forward/move_backward\n"
                        "recognize: color_recognition/shape_recognition/qrcode_recognition/drug_identification/garbage_identification/characters_identification\n"
                        "sort: color_sorting/shape_sorting/qrcode_sorting/drug_sorting/garbage_sorting/characters_sorting\n"
                        "place: place_in_warehouse_1/2/3/4\n"
                        "position: go_home/go_sorting_position/go_camera_position\n"
                        "game: face_tracking/guessing_fists_game/stacking_game\n"
                        "calibration: color_calibration"
                    )
                },
                "data1": {
                    "type": "integer",
                    "description": "附加参数1（通常用于指定目标位置、编号等，默认0）"
                },
                "data2": {
                    "type": "integer",
                    "description": "附加参数2（通常用于指定目标位置、编号等，默认0）"
                },
            },
            "required": ["action", "command"],
        }

    async def execute(self, **kwargs) -> List[Dict[str, Any]]:
        action = kwargs.get("action")
        command = kwargs.get("command")
        data1 = kwargs.get("data1", 0)
        data2 = kwargs.get("data2", 0)

        # 列出可用命令
        if action == "list":
            result = self.client.list_commands()
            if result:
                text = "机械臂可用命令：\n"
                text += str(result)
            else:
                text = "获取命令列表失败，请检查机械臂服务是否运行"
            return to_content(text=text)

        # 校验action
        valid_actions = {"move", "recognize", "sort", "place", "position", "game", "calibration"}
        if action not in valid_actions:
            return to_content(
                text=f"不支持的动作：{action}，请使用 {'/'.join(valid_actions)}"
            )

        # 执行命令
        result = self.client.execute_command(command, data1, data2)
        if result is None:
            return to_content(
                text=f"发送命令失败，请检查机械臂服务({MBOT_MOTION_URL}:{MBOT_MOTTION_PORT})是否运行"
            )

        if result.get("success"):
            cmd_name = result.get("cmd_name", command)
            cmd_code = result.get("cmd_code", "?")
            text = (
                f"命令已发送\n"
                f"  命令: {cmd_name}\n"
                f"  代码: {cmd_code}\n"
                f"  参数: data1={data1}, data2={data2}"
            )
        else:
            error = result.get("error", "未知错误")
            text = f"命令执行失败: {error}"

        return to_content(text=text)
