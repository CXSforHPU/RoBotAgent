import os
import sys
from pathlib import Path
from dotenv import (
    load_dotenv,
    find_dotenv
)


# 项目根目录
ROOT_PATH = Path(__file__).parent
load_dotenv(find_dotenv(str(ROOT_PATH / '.env')))

# workspace
WORKSPACE_PATH = ROOT_PATH / "workspace"
if not WORKSPACE_PATH.exists():
    WORKSPACE_PATH.mkdir()

# memory
MEMORY_PATH = WORKSPACE_PATH / "memory"
if not MEMORY_PATH.exists():
    MEMORY_PATH.mkdir()

# skill
SKILLS_PATH = ROOT_PATH / "skills"
if not SKILLS_PATH.exists():
    SKILLS_PATH.mkdir()

# ollama
VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL", None)
VLLM_API_KEY = os.environ.get("VLLM_API_KEY", None)
VLLM_MODEL = os.environ.get("VLLM_MODEL", None)

# ollama
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", None)
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", None)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", None)

# siliconflow
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", None)
SILICONFLOW_BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", None)
SILICONFLOW_MODEL = os.environ.get("SILICONFLOW_MODEL", None)

# QQ
QQ_ID = os.environ.get("QQ_ID", None)
QQ_APP_ID = os.environ.get("QQ_APP_ID", None)
QQ_TOKEN = os.environ.get("QQ_TOKEN", None)
QQ_APP_SECRET = os.environ.get("QQ_APP_SECRET", None)


# Monster Hunter World
MONSTER_HUNTER_WORLD_SERVER_URL = os.environ.get("MONSTER_HUNTER_WORLD_SERVER_URL", None)
MONSTER_HUNTER_WORLD_EXE_PATH = os.environ.get("MONSTER_HUNTER_WORLD_EXE_PATH", None)

# temp dir
TEMP_PATH = ROOT_PATH / "temp"