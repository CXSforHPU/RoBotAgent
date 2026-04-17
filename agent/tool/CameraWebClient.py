import sys
import os
import time as tm
import logging
from typing import Any, List, Dict, Optional
import uuid  # 生成唯一图片名，避免覆盖

# 兼容项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir) 
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 从环境配置读取摄像头服务地址
from env import CAMERA_URL, CAMERA_PORT, TEMP_PATH
# 继承Agent核心基类
from agent.tool.base import Tool
from agent.utils import to_content

import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

# 配置日志
logger = logging.getLogger(__name__)

class CameraWebClient:
    """
    摄像头服务纯Python客户端
    对接ROS+Flask相机服务端的 /status、/get_image 接口
    纯HTTP调用，无需任何ROS环境依赖
    """
    
    # 默认超时设置 (连接超时, 读取超时)
    DEFAULT_TIMEOUT = (3, 5) 

    def __init__(self, host: str = CAMERA_URL, port: int = CAMERA_PORT):
        self.host = host
        self.port = port
        # 确保 base_url 格式正确，去除末尾斜杠
        self.base_url = f"http://{host}:{port}".rstrip('/')
        self.session = requests.Session()
        # 设置默认 headers，例如 User-Agent
        self.session.headers.update({
            "User-Agent": "RoBotAgent-CameraClient/1.0"
        })
        # 自动创建temp目录
        os.makedirs(TEMP_PATH, exist_ok=True)

    def _request_json(self, endpoint: str, method: str = "GET") -> Optional[Dict[str, Any]]:
        """
        通用 JSON 请求方法，处理超时和异常
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            if method.upper() == "GET":
                res = self.session.get(url, timeout=self.DEFAULT_TIMEOUT)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            res.raise_for_status()
            return res.json()
        
        except ConnectionError:
            logger.error(f"连接摄像头服务失败: {url}")
            return None
        except Timeout:
            logger.warning(f"请求摄像头服务超时: {url}")
            return None
        except RequestException as e:
            logger.error(f"请求摄像头服务异常: {e}, URL: {url}")
            return None
        except ValueError:
            logger.error(f"响应解析JSON失败: {url}")
            return None

    def get_camera_status(self) -> Optional[Dict[str, Any]]:
        """
        获取摄像头核心状态
        返回：FPS、分辨率、连接状态、是否有画面帧
        """
        data = self._request_json("status")
        if data and data.get("code") == 200:
            return data.get("data")
        return None

    def get_camera_image_url(self) -> Optional[str]:
        """
        获取摄像头实时画面URL（供前端/Agent展示使用）
        """
        try:
            if not self.host or not self.port:
                return None
            return f"{self.base_url}/get_image"
        except Exception as e:
            logger.error(f"生成图片URL失败: {e}")
            return None

    def get_camera_image_path(self) -> Optional[str]:
        """
        【核心功能】获取照片并保存到temp目录，返回文件绝对路径
        下载图片→保存到TEMP_PATH→生成唯一文件名→返回路径
        """
        image_url = self.get_camera_image_url()
        if not image_url:
            logger.error("图片URL为空，无法下载")
            return None

        try:
            # 下载图片数据
            response = self.session.get(image_url, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            
            # 生成唯一图片名（避免覆盖）
            image_name = f"camera_{uuid.uuid4().hex[:8]}_{int(tm.time())}.jpg"
            image_path = os.path.abspath(os.path.join(TEMP_PATH, image_name))
            
            # 保存图片到temp目录
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"图片已保存到: {image_path}")
            return image_path

        except Exception as e:
            logger.error(f"下载/保存图片失败: {e}")
            return None
    
    def close(self):
        """关闭 session，释放资源"""
        if self.session:
            self.session.close()

    def __del__(self):
        """析构时尝试关闭 session"""
        self.close()


class CameraGetTool(Tool):
    """
    摄像头状态+画面查询工具（Agent专用）
    支持：获取相机状态、检查健康度、获取照片本地保存路径
    """
    
    def __init__(self):
        super().__init__()
        self.client = CameraWebClient(host=CAMERA_URL, port=CAMERA_PORT)

    @property
    def name(self) -> str:
        return 'camera_get'

    @property
    def description(self) -> str:
        return "查询摄像头状态：获取实时FPS、画面分辨率、连接状态、是否正常采集画面、获取摄像头实时照片（链接/本地路径）"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_status", "check_health", "get_image", "get_camera_status"],
                    "description": "查询动作：get_status(获取相机完整状态) | check_health(检查相机是否正常运行) | get_image(获取摄像头实时照片) | get_camera_status(简略状态)"
                },
                "model_text_input": {
                    "type": "string",
                    "description": "多模态针对该图像要进行的处理,不能为空（仅限 get_image 必填 ）"
                }
            },
            "required": ["action"]
        }

    async def execute(self, **kwargs) -> List[Dict[str, Any]]:
        """Agent执行入口"""
        action = kwargs.get("action")

        if action == "get_status":
            return self._handle_get_status()
        
        elif action == "check_health":
            return self._handle_check_health()
        
        elif action == "get_image":
            return self._handle_get_image()
        
        elif action == "get_camera_status":
            return self._handle_get_camera_status_legacy()
        
        else:
            text = f"❌ 不支持的动作：{action}，请使用 get_status / check_health / get_image"
            return to_content(text=text)

    def _handle_get_status(self) -> List[Dict[str, Any]]:
        """处理获取完整状态"""
        status = self.client.get_camera_status()
        if status:
            try:
                fps = status.get('fps', 0)
                resolution = status.get('resolution', 'Unknown')
                conn_status = status.get('status', 'Unknown')
                has_frame = status.get('has_frame', False)
                
                text = (f"📷 摄像头实时状态：\n"
                        f"🎬 实时FPS：{fps:.1f}\n"
                        f"📐 画面分辨率：{resolution}\n"
                        f"🔌 连接状态：{conn_status}\n"
                        f"🖼️ 画面状态：{'正常采集' if has_frame else '无画面'}")
            except Exception as e:
                logger.error(f"解析状态数据失败: {e}")
                text = "❌ 解析摄像头状态数据失败"
        else:
            text = "❌ 获取摄像头状态失败，请检查相机服务是否运行"
        
        return to_content(text=text)

    def _handle_check_health(self) -> List[Dict[str, Any]]:
        """处理健康检查"""
        status = self.client.get_camera_status()
        if status and status.get("has_frame"):
            fps = status.get('fps', 0)
            conn_status = status.get('status', 'Unknown')
            text = f"✅ 摄像头运行正常 | FPS:{fps:.1f} | 状态:{conn_status}"
        else:
            text = "❌ 摄像头异常：未采集到画面或服务未启动"
        
        return to_content(text=text)

    def _handle_get_image(self,model_text_input = None) -> List[Dict[str, Any]]:
        """【修复】处理获取图片（链接+本地保存），移除多余参数"""
        # 1. 获取图片URL和相机状态
        image_url = self.client.get_camera_image_url()
        status = self.client.get_camera_status()
        
        if image_url and status and status.get("has_frame"):
            # 2. 保存图片到temp目录
            image_local_path = self.client.get_camera_image_path()
            if image_local_path:
                if model_text_input is None:
                    text = f"描述一下照片内容"
                else:
                    text = model_text_input
                # 适配to_content的image_url参数
                return to_content(text=text, image=image_local_path)
            else:
                text = "❌ 照片保存失败，temp目录无写入权限"
        else:
            reason = "相机未运行" if not status else "无画面"
            text = f"❌ 获取摄像头照片失败：{reason}"
        
        return to_content(text=text)

    def _handle_get_camera_status_legacy(self) -> List[Dict[str, Any]]:
        """兼容旧版状态查询"""
        status = self.client.get_camera_status()
        if status:
            fps = status.get('fps', 0)
            conn_status = status.get('status', 'Unknown')
            text = f"FPS:{fps:.1f} | 状态:{conn_status}"
        else:
            text = "获取摄像头状态失败"
        return to_content(text=text)