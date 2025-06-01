# app/ui/main.py

from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from app.ui.styles import COLORS, FONTS

class Basic(QtWidgets.QWidget) :
    def __init__(self):
        super().__init__()