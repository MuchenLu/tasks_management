# app/ui/componenets/loading.py

from PyQt6 import QtWidgets, QtCore, QtGui
from app.ui.styles import COLORS, FONTS

class CircularLoadingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 設定基本屬性
        self.setFixedSize(200, 300)
        self.setWindowTitle("載入中")
        
        # 進度參數
        self.progress = 0
        self.progress_text = "準備中..."
        
        # 建立垂直佈局
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 建立繪圖區域
        self.drawingArea = QtWidgets.QWidget(self)
        self.drawingArea.setFixedSize(200, 200)
        layout.addWidget(self.drawingArea, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # 建立標籤
        self.label = QtWidgets.QLabel("UI建構中，請稍等...")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(FONTS["content"])
        layout.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # 進度標籤
        self.progress_label = QtWidgets.QLabel("0%")
        self.progress_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setFont(FONTS["content"])
        layout.addWidget(self.progress_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # 設定視窗屬性
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 置中顯示
        self.center_on_screen()
    
    def center_on_screen(self):
        """將視窗置中顯示在螢幕上"""
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def update_progress(self, percent, text):
        """更新進度資訊"""
        self.progress = max(0, min(100, percent))  # 確保進度在 0-100 之間
        self.progress_text = text
        self.progress_label.setText(f"{self.progress}% - {text}")
        self.update()  # 重繪視窗
        
        # 強制處理事件，確保 UI 更新
        QtWidgets.QApplication.processEvents()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # 繪製半透明背景
        painter.setBrush(QtGui.QColor(240, 240, 240, 200))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        # 設定畫筆
        pen = QtGui.QPen()
        pen.setWidth(12)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        
        # 繪製靜態灰色環
        pen.setColor(QtGui.QColor(200, 200, 200, 150))
        painter.setPen(pen)
        painter.drawArc(50, 50, 100, 100, 0, 360 * 16)
        
        # 繪製進度環
        pen.setColor(QtGui.QColor(COLORS["primary_button"]))
        painter.setPen(pen)
        # 繪製進度弧，從90度開始（頂部），順時針方向
        start_angle = 90 * 16  # 起始角度（頂部）
        span_angle = int(-self.progress * 3.6 * 16)  # 進度對應的角度（負值表示順時針），轉換為整數
        painter.drawArc(50, 50, 100, 100, start_angle, span_angle)
        
        # 繪製進度文字
        painter.setPen(QtGui.QColor(COLORS["primary_black"]))
        painter.setFont(FONTS["h1"])
        painter.drawText(50, 50, 100, 100, QtCore.Qt.AlignmentFlag.AlignCenter, f"{self.progress}%")

    def mousePressEvent(self, event):
        """允許拖動視窗"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            
    def mouseMoveEvent(self, event):
        """處理視窗拖動"""
        if hasattr(self, 'dragPos'):
            newPos = event.globalPosition().toPoint() - self.dragPos
            self.move(self.x() + newPos.x(), self.y() + newPos.y())
            self.dragPos = event.globalPosition().toPoint()