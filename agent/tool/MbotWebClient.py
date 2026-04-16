import sys
import os
import time as tm
# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上级目录 (即 RoBotAgent 目录)
parent_dir = os.path.dirname(current_dir)
# 根据包结构设置项目根目录
project_root = os.path.dirname(parent_dir) 

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from env import(
    MBOT_MOTION_URL,
    MBOT_MOTTION_PORT
)

from agent.tool.base import Tool
from agent.utils import to_content
from typing import Any, List, Dict
import requests
from requests.exceptions import RequestException

# ===================== 内部机械臂客户端（新增时间参数支持） =====================
class MbotWebClient:
    """无ROS依赖的纯Python客户端"""
    def __init__(self, host: str = MBOT_MOTION_URL, port: int = MBOT_MOTTION_PORT):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.timeout = 3

    def get_arm_status(self) -> Dict[str, int] | None:
        try:
            res = self.session.get(f"{self.base_url}/arm/get_status")
            res.raise_for_status()
            data = res.json()
            return data.get("data") if data.get("code") == 200 else None
        except RequestException:
            return None

    # 新增：time 参数（运动时间，单位秒）
    def set_joint(self, joint_name: str, angle: int, time: float) -> bool:
        try:
            res = self.session.post(
                f"{self.base_url}/arm/set_joint",
                json={"joint": joint_name, "angle": angle}
            )
            tm.sleep(time)
            return res.json().get("code") == 200
        except RequestException:
            return False

    # 新增：time 参数（运动时间，单位秒）
    def set_gripper(self, angle: int, time: float) -> bool:
        try:
            res = self.session.post(
                f"{self.base_url}/arm/set_gripper",
                json={"angle": angle, "time": time}
            )
            tm.sleep(time)
            return res.json().get("code") == 200
        except RequestException:
            return False

# ===================== 智能体工具类（新增时间控制参数） =====================
class ArmControlTool(Tool):
    """
    机械臂控制工具
    支持：获取状态、设置关节（带时间）、设置夹爪（带时间）
    """
    def __init__(self):
        super().__init__()
        # 从环境配置读取服务地址
        self.client = MbotWebClient(host=MBOT_MOTION_URL, port=MBOT_MOTTION_PORT)

    @property
    def name(self):
        return 'arm_control'

    @property
    def description(self):
        return "控制机械臂：获取当前姿态、设置单个关节角度（指定运动时间）、设置夹爪角度（指定运动时间）"

    @property
    def parameters(self) -> Dict[str, Any]:
        # 新增 time 参数，格式严格对齐智能体要求
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "动作：get_status(获取状态) | set_joint(设置关节) | set_gripper(设置夹爪)"
                },
                "joint_name": {
                    "type": "string",
                    "description": "关节名：joint1/joint2/joint3/joint4/joint5（仅set_joint必填）"
                },
                "angle": {
                    "type": "integer",
                    "description": "目标角度(-125~125)（set_joint/set_gripper必填）"
                },
                # ===================== 新增：时间参数 =====================
                "time": {
                    "type": "number",
                    "description": "机械臂运动时间，单位：秒，必须大于0（set_joint/set_gripper必填）"
                }
            },
            "required": ["action"]
        }

    async def execute(self, **kwargs) -> List[Dict[str, Any]]:
        action = kwargs.get("action")
        joint_name = kwargs.get("joint_name")
        angle = kwargs.get("angle")
        # ===================== 新增：获取时间参数 =====================
        move_time = kwargs.get("time")

        if action == "get_status":
            # 获取状态无需时间
            status = self.client.get_arm_status()
            if status:
                text = (f"机械臂当前状态：\n"
                        f"joint1: {status['joint1']}°\n"
                        f"joint2: {status['joint2']}°\n"
                        f"joint3: {status['joint3']}°\n"
                        f"joint4: {status['joint4']}°\n"
                        f"joint5: {status['joint5']}°\n"
                        f"夹爪: {status['gripper']}°")
            else:
                text = "获取机械臂状态失败，请检查服务是否运行"

        elif action == "set_joint":
            # 校验必填参数（角度 + 时间）
            if not joint_name or angle is None or move_time is None:
                text = "参数错误：设置关节需填写 joint_name、angle、time"
            elif not isinstance(move_time, (int, float)) or move_time <= 0:
                text = "参数错误：运动时间必须大于0秒"
            else:
                # 传入时间参数控制运动速度
                ok = self.client.set_joint(joint_name, angle, float(move_time))
                text = f"设置{joint_name}={angle}°，时间={move_time}s：{'成功' if ok else '失败'}"

        elif action == "set_gripper":
            # 校验必填参数（角度 + 时间）
            if angle is None or move_time is None:
                text = "参数错误：设置夹爪需填写 angle、time"
            elif not isinstance(move_time, (int, float)) or move_time <= 0:
                text = "参数错误：运动时间必须大于0秒"
            else:
                # 传入时间参数控制夹爪运动
                ok = self.client.set_gripper(angle, float(move_time))
                text = f"设置夹爪={angle}°，时间={move_time}s：{'成功' if ok else '失败'}"

        else:
            text = f"不支持的动作：{action}，请使用 get_status/set_joint/set_gripper"

        return to_content(text=text)