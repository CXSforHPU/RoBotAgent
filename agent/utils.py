import os
import base64
from urllib.parse import urlparse
from typing import (
    Dict,
    Any,
    Tuple,
    List,
    Optional
)
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

def to_content(
        text: Optional[str] = None,
        image: Optional[str] = None,
        audio: Optional[str] = None,
) -> List[Dict[str, Any]]:

    content = []
    if text is not None:
        content.append(format_text(text))

    if image is not None:
        content.append(format_image(image))
    
    if audio is not None:
        content.append(format_audio(audio))

    return content


def format_text(text: str) -> Dict[str, str]:
    return {
        "type": "text",
        "text": text
    }


def format_image(image: str) -> Dict[str, str]:
    img_url = ""
    if is_url(image):
        img_url = image
    elif os.path.isfile(image):
        # 1. 获取后缀
        ext = get_file_extension(image)
        # 2. 获取对应的 MIME 类型
        mime_type = get_image_mime_type(ext)
        # 3. 读取 base64
        base64_str = read_base64_image(image)
        # 4. 构造 Data URI
        img_url = f"data:{mime_type};base64,{base64_str}"
    else:
        raise ValueError(f"Invalid image source: {image}")

    return {
        "type": "image_url",
        "image_url": {
            "url": img_url,
            "detail": "auto"
        }
    }

def format_audio(audio: str) -> Dict[str, str]:
    audio_url = ""
    
    # 判断是否是 URL
    if is_url(audio):
        audio_url = audio
    elif os.path.isfile(audio):
        # 1. 获取后缀
        ext = get_file_extension(audio)
        # 2. 获取对应的 MIME 类型
        mime_type = get_audio_mime_type(ext)
        # 3. 读取 base64
        base64_str = read_base64_audio(audio)
        # 4. 构造 Data URI
        audio_url = f"data:{mime_type};base64,{base64_str}"
    else:
        raise ValueError(f"Invalid audio source: {audio}")
    
    return {
        "type": "audio_url",
        "audio_url": {
            "url": audio_url
        }
    }

def print_content(
        text: Any,
        end: str = '\n',
):
    print(text, end=end)


def print_reasoning(
        text: Any,
        end: str = '\n',
):
    print_formatted_text(FormattedText([
        ('#777777', text),
    ]), end=end)


def print_tool_calls(
        text: Any,
        end: str = '\n',
):
    print_formatted_text(FormattedText([
        ('#77ffff', text),
    ]), end=end)


def read_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def read_base64_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

def read_base64_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")
    
def is_url(string: str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def get_file_extension(file_path: str) -> str:
    """
    获取文件后缀名（包含点号,如 '.jpg')
    如果输入是 URL,尝试从路径部分提取;如果是本地路径,直接提取。
    """
    
    # 如果是 URL,提取其 path 部分;如果是本地路径,直接使用
    parsed = urlparse(file_path)
    path = parsed.path if parsed.scheme else file_path
    
    # splitext 将路径分为 (root, ext)
    _, ext = os.path.splitext(path)
    return ext.lower() # 通常返回小写以便比较,如 '.jpg'

def get_audio_mime_type(ext: str) -> str:
    """根据后缀返回 MIME 类型"""
    mime_map = {
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.m4a': 'audio/mp4',
        '.flac': 'audio/flac',
    }
    return mime_map.get(ext, 'audio/wav')

def get_image_mime_type(ext: str) -> str:
    """根据后缀返回 MIME 类型"""
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
    }
    return mime_map.get(ext, 'image/png')

