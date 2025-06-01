# app/main.py

from PyQt6 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

from .ui.main_window import Basic

def main() :
    basic = Basic()
    basic.show()
    sys.exit(app.exec())