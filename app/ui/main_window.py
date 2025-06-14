# app/ui/main.py

from PyQt6 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import sys
from app.services import database
from app.ui.styles import COLORS, FONTS
from app.utils.helper import DataManager
from app.utils.config import ICON_ICO
from app.utils.log import write
from .components.top_bar import Top
from .components.side_menu import Side
from .components.main_area import Main
from .components.add import Add

class Basic(QtWidgets.QWidget) :
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.setWindowTitle("任務管理系統")
        
        # 檢查圖示檔案是否存在
        if ICON_ICO :
            self.setWindowIcon(QtGui.QIcon(ICON_ICO))
        
        self._width = QtWidgets.QApplication.primaryScreen().geometry().width()
        self._height = QtWidgets.QApplication.primaryScreen().geometry().height()
        
        self.data_manager = DataManager()

        write("建立 Top 元件...", "info")
        self.top = Top(self)
        write("建立 Side 元件", "info")
        self.side = Side(self)
        write("建立 Main 元件", "info")
        self.main = Main(self)
        write("建立 Add 元件", "info")
        self.add = Add(self)

        self.top.show()
        self.side.show()
        self.main.show()

    def closeEvent(self, event):
        super().closeEvent(event)
        try:
            self.data = self.data_manager.get("data")
            database.update_data(self.data)
        except:
            pass

    def update(self):
        # try:
            self.data = database.get_data()
            self.data_manager.update(self.data, "data")
            self.tasks = database.sort_data(self.data["Tasks"])
            self.data_manager.update(self.tasks, "tasks")
            if self.side :
                self.side.project()
            if self.main:
                self.main.task()
        # except Exception as e:
        #     print(f"更新失敗: {e}")