# app/ui/components/top_bar.py

from PyQt6 import QtWidgets, QtCore, QtGui
from app.ui.styles import COLORS, FONTS
from app.utils.config import ICON_PNG
from app.utils.helper import PageManager

class Top(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

        self.page_manager = PageManager()
        self.parent = parent
        self.x = 0
        self.y = 0
        self._width = self.parent._width
        self._height = int(self.parent._height * 0.1)
        self.setGeometry(self.x, self.y, self._width, self._height)
        self.setStyleSheet(f"background: {COLORS['top_color']}")

        self.home_frame = QtWidgets.QFrame(self)
        self.home_layout = QtWidgets.QHBoxLayout(self.home_frame)
        self.home_frame_x = int(self._width * 0.001)
        self.home_frame_y = 0
        self.home_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.home_frame.mousePressEvent = lambda event: self.back_home(event)

        self.home_icon = QtWidgets.QLabel(self.home_frame)
        icon = QtGui.QPixmap(ICON_PNG)
        icon = icon.scaled(int(self._width * 0.05), int(self._width * 0.05), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.home_icon.setPixmap(icon)
        self.home_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.home_layout.addWidget(self.home_icon)

        self.home_text = QtWidgets.QLabel(self.home_frame, text = "任務管理系統")
        self.home_text.setStyleSheet(f"color: {COLORS['white']}")
        self.home_text.setFont(FONTS["h1"])
        self.home_layout.addWidget(self.home_text)
        self.home_frame.move(self.home_frame_x, self.home_frame_y)
        self.home_frame.mousePressEvent = lambda event: self.back_home(event)
        self.home_frame.show()
    
    def back_home(self, event) :
        self.page_manager.update("Home")
        self.parent.side.initialize(event)
        self.parent.add.initialize()
        self.parent.main.home()