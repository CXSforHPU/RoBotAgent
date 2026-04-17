import sys
import os
import time as tm
# 兼容项目路径（和你原有代码一致）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir) 
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 从环境配置读取传感器服务地址
from env import(
    SENSOR_URL,
    SENSOR_PORT
)
# 继承Agent核心基类
from agent.tool.base import Tool
from agent.utils import to_content
from typing import Any, List, Dict
import requests
from requests.exceptions import RequestException

# ===================== 【传感器专属】HTTP客户端（无ROS依赖） =====================
class SensorWebClient:
    """
    传感器服务纯Python客户端
    对接ROS+Flask服务端的 /sensor_data、/sensor_status 接口
    """
    def __init__(self, host: str = SENSOR_URL, port: int = SENSOR_PORT):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.timeout = 3  # 请求超时3秒

    def get_sensor_data(self) -> Dict[str, Any] | None:
        """
        获取传感器实时数据
        返回：电压、温湿度、气压、光照、空气质量、超声波状态
        """
        try:
            res = self.session.get(f"{self.base_url}/sensor_data")
            res.raise_for_status()
            data = res.json()
            return data.get("data") if data.get("status") == 200 else None
        except RequestException:
            return None

    def get_sensor_status(self) -> Dict[str, Any] | None:
        """
        获取传感器节点状态
        返回：节点运行状态、是否有数据、更新时间、订阅话题
        """
        try:
            res = self.session.get(f"{self.base_url}/sensor_status")
            res.raise_for_status()
            data = res.json()
            return data.get("data") if data.get("status") == 200 else None
        except RequestException:
            return None

# ===================== 【Agent工具】传感器数据查询工具 =====================
class SensorGetTool(Tool):
    """
    传感器数据查询工具（Agent专用）
    支持：获取实时传感器数据、获取节点运行状态
    完全对齐原有机械臂工具规范，无缝集成Agent
    """
    def __init__(self):
        super().__init__()
        # 初始化传感器客户端（从环境配置自动读取服务地址）
        self.client = SensorWebClient(host=SENSOR_URL, port=SENSOR_PORT)

    @property
    def name(self):
        return 'sensor_get'  # 工具名（唯一标识）

    @property
    def description(self):
        return "查询传感器数据：获取实时环境数据（电压/温湿度/气压/光照/空气质量/超声波）、传感器节点运行状态"

    @property
    def parameters(self) -> Dict[str, Any]:
        # 参数格式严格对齐Agent要求，极简设计（仅需action）
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "查询动作：get_data(获取实时传感器数据) | get_status(获取节点运行状态)"
                }
            },
            "required": ["action"]  # 仅action为必填参数
        }

    async def execute(self, **kwargs) -> List[Dict[str, Any]]:
        """Agent执行入口（异步方法，和原有工具保持一致）"""
        action = kwargs.get("action")

        # 1. 获取传感器实时数据
        if action == "get_data":
            data = self.client.get_sensor_data()
            if data:
                text = (f"📊 传感器实时数据：\n"
                        f"🔋 电池电压：{data['voltage']} V\n"
                        f"🌡️ 环境温度：{data['temperature']} ℃\n"
                        f"💧 环境湿度：{data['humidity']} %RH\n"
                        f"🌍 大气压强：{data['pressure']} kPa\n"
                        f"💡 光照强度：{data['light']} Lux\n"
                        f"🌫️ 空气质量1：{data['mp503']}\n"
                        f"🌫️ 空气质量2：{data['mp2']}\n"
                        f"📡 超声波1：{'检测到障碍物' if data['sonar1'] else '无障碍物'}\n"
                        f"📡 超声波2：{'检测到障碍物' if data['sonar2'] else '无障碍物'}\n"
                        f"📡 超声波3：{'检测到障碍物' if data['sonar3'] else '无障碍物'}\n"
                        f"📡 超声波4：{'检测到障碍物' if data['sonar4'] else '无障碍物'}")
            else:
                text = "❌ 获取传感器数据失败，请检查传感器服务是否运行"

        # 2. 获取传感器节点状态
        elif action == "get_status":
            status = self.client.get_sensor_status()
            if status:
                text = (f"🔧 传感器节点状态：\n"
                        f"✅ 节点状态：{'运行中' if status['node_status'] == 'running' else '已停止'}\n"
                        f"📥 数据状态：{'有数据' if status['has_data'] else '无数据'}\n"
                        f"🌐 订阅话题：{status['topic']}\n"
                        f"⏰ 最后更新时间：{status['data_update_time']:.1f}s")
            else:
                text = "❌ 获取节点状态失败，请检查传感器服务是否运行"

        # 3. 不支持的动作
        else:
            text = f"❌ 不支持的动作：{action}，请使用 get_data / get_status"

        # 返回Agent要求的格式
        return to_content(text=text)