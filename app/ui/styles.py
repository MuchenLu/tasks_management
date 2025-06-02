# app/ui/styles.py

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt6 import QtGui, QtWidgets
from app.utils.config import FONT_FILE
from app.utils.log import write

COLORS = {"top_color": "#8095bd",
          "side_color": "#d2dde8",
          "main_color": "#f1f1f1",
          "header_color": "#e9eff6",
          "primary_button": "#8095bd",
          "primary_button:hover": "#6f84ad",
          "secondary_button": "#6ca57c",
          "secondary_button:hover": "#5c926c",
          "cancel_button": "#e57373",
          "cancel_button:hover": "#d9534f",
          "red_button_color":    "#D32f2f",
          "line_color": "#c7cfd9",
          "remark_color": "rgba(0, 0, 0, 0.5)",
          "white": "#ffffff",
          "primary_black": "#2b2b2b",
          "secondary_black": "#3a3a3a",
          "common_black": "#4a4a4a",
          "green": "#00796b",
          "red": "#d9534f",
          "shadow": "0, 0, 0, 25",
          "undo": "#d2dde8",
          "doing": "#5a7acb",
          "done": "#6ca57c"}

def get_font_family():
    """取得應用程式字體名稱"""
    try :
        return QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont(FONT_FILE))[0]
    except Exception as e :
        write(f"字體不存在，錯誤訊息: {e}", "error")
        return "Ariel"

FONT_FAMILY = get_font_family()

FONTS = {"h1": QtGui.QFont(FONT_FAMILY, 24, QtGui.QFont.Weight.Bold),
         "h2": QtGui.QFont(FONT_FAMILY, 16),
         "content": QtGui.QFont(FONT_FAMILY, 12),
         "remark": QtGui.QFont(FONT_FAMILY, 8),
         "menu": QtGui.QFont(FONT_FAMILY, 16),
         "highlight": QtGui.QFont(FONT_FAMILY, 18, QtGui.QFont.Weight.Bold)}