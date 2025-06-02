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

# Google Calendar API 權限設定
SCOPES = [f"{os.getenv('SCOPES', '')}"]

# 檔案路徑
CONFIG_DIR = os.path.join(PROJECT_ROOT, os.getenv("CONFIG_DIR", ""))
DATA_DIR = os.path.join(PROJECT_ROOT, os.getenv("DATA_DIR", ""))
STATIC_DIR = os.path.join(PROJECT_ROOT, os.getenv("STATIC_DIR", ""))
LOG_DIR = os.path.join(PROJECT_ROOT, os.getenv("LOG_DIR", ""))

# Google API 檔案
CALENDAR_API_KEY = os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_API_KEY", ""))
CALENDAR_TOKEN = os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_TOKEN", ""))
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

check_list = [SCOPES, LOG_DIR, CALENDAR_API_KEY, CALENDAR_TOKEN, DATABASE_KEY, FONT_FILE, ICON_ICO, ICON_PNG, DELETE_PNG, EDIT_PNG, CALENDAR_PROFILE_DIR]

for item in check_list :
    if item == PROJECT_ROOT :
        if item == CALENDAR_TOKEN :
            write(f"{item=}不存在，需請求".split("=")[1], "warning")
            item = None
        else :
            write(f"{item=}不存在".split("=")[1], "error")
            item = None
write("設定完成", "info")