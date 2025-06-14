# app/utils/config.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.utils.log import write

write("開始執行...", "info")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, PROJECT_ROOT)

load_dotenv(os.path.join(PROJECT_ROOT, "settings", ".env"))

# Google Calendar & Classroom API 權限設定
GOOGLE_CALENDAR_SCOPES = [f"{os.getenv('GOOGLE_CALENDAR_SCOPES', '')}"]
GOOGLE_CLASSROOM_SCOPES = [f"{os.getenv('GOOGLE_CLASSROOM_SCOPES1', '')}", f"{os.getenv('GOOGLE_CLASSROOM_SCOPES2', '')}", f"{os.getenv('GOOGLE_CLASSROOM_SCOPES3', '')}"]

# 檔案路徑
CONFIG_DIR = os.path.join(PROJECT_ROOT, os.getenv("CONFIG_DIR", ""))
DATA_DIR = os.path.join(PROJECT_ROOT, os.getenv("DATA_DIR", ""))
STATIC_DIR = os.path.join(PROJECT_ROOT, os.getenv("STATIC_DIR", ""))
LOG_DIR = os.path.join(PROJECT_ROOT, os.getenv("LOG_DIR", ""))

# Google API 檔案
GOOGLE_API_KEY = os.path.join(PROJECT_ROOT, os.getenv("GOOGLE_API_KEY", ""))
CALENDAR_TOKEN = os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_TOKEN", ""))
CLASSROOM_TOKEN = os.path.join(PROJECT_ROOT, os.getenv("CLASSROOM_TOKEN", ""))
DATABASE_KEY = os.path.join(PROJECT_ROOT, os.getenv("DATABASE_KEY", ""))

# 靜態資源檔
FONT_FILE = os.path.join(PROJECT_ROOT, os.getenv("FONT_FILE", ""))
ICON_ICO = os.path.join(PROJECT_ROOT, os.getenv("ICON_ICO", ""))
ICON_PNG = os.path.join(PROJECT_ROOT, os.getenv("ICON_PNG", ""))
DELETE_PNG = os.path.join(PROJECT_ROOT, os.getenv("DELETE_PNG", ""))
EDIT_PNG = os.path.join(PROJECT_ROOT, os.getenv("EDIT_PNG", ""))

# Google Caledar 快取資料夾
CALENDAR_PROFILE_DIR = os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_PROFILE_DIR", ""))

# Realtime Database 設定
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Google Calendar ID
CALENDAR_ID = os.getenv("CALENDAR_ID", "")

# 爬蟲設定
HEADER = os.getenv("HEADER", "")

# ONO 相關設定
ONO_URL = os.getenv("ONO_URL", "")
ONO_USER_NAME = os.getenv("ONO_USER_NAME", "")
ONO_USER_PASSWORD = os.getenv("ONO_USER_PASSWORD", "")

# Google Classroom 相關設定
GOOGLE_CLASSROOM_URL = os.getenv("GOOGLE_CLASSROOM_URL", "")
GOOGLE_CLASSROOM_USER_EMAIL = os.getenv("GOOGLE_CLASSROOM_USER_EMAIL", "")
GOOGLE_CLASSROOM_USER_PASSWORD = os.getenv("GOOGLE_CLASSROOM_USER_PASSWORD", "")

def check_and_update_constants():
    check_list = [
        (LOG_DIR, 'LOG_DIR'),
        (GOOGLE_API_KEY, 'GOOGLE_API_KEY'),
        (CALENDAR_TOKEN, 'CALENDAR_TOKEN'),
        (CLASSROOM_TOKEN, 'CLASSROOM_TOKEN'),
        (DATABASE_KEY, 'DATABASE_KEY'),
        (FONT_FILE, 'FONT_FILE'),
        (ICON_ICO, 'ICON_ICO'),
        (ICON_PNG, 'ICON_PNG'),
        (DELETE_PNG, 'DELETE_PNG'),
        (EDIT_PNG, 'EDIT_PNG'),
        (CALENDAR_PROFILE_DIR, 'CALENDAR_PROFILE_DIR')
    ]

    for item, name in check_list:
        if item == PROJECT_ROOT or not os.path.exists(item):
            if item == CALENDAR_TOKEN:
                write(f"{name}不存在，需請求", "warning")
                globals()[name] = None
            else:
                write(f"{name}不存在", "error")
                globals()[name] = None

# 調用函數
check_and_update_constants()