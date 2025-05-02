import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QLabel, 
    QDialog
)
from PyQt6.QtGui import (
    QPainter, 
    QPen, 
    QColor, 
    QLinearGradient
)
from PyQt6.QtCore import (
    Qt, 
    QTimer, 
    QThread,
    pyqtSignal
)

class CircularLoadingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 設定基本屬性
        self.setFixedSize(200, 200)
        self.angle = 0
        
        # 建立計時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(30)  # 每30ms更新一次
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 建立漸層顏色
        gradient = QLinearGradient(0, 0, 200, 200)
        gradient.setColorAt(0, QColor(50, 150, 255))
        gradient.setColorAt(1, QColor(100, 200, 255))
        
        # 設定畫筆
        pen = QPen(gradient, 15)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # 繪製環形
        painter.drawArc(
            25, 25, 150, 150,  # 調整位置和大小
            self.angle * 16,   # 起始角度
            120 * 16           # 弧長
        )
    
    def update_loading(self):
        self.angle = (self.angle + 5) % 360
        self.update()

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 設定對話框屬性
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.CustomizeWindowHint
        )
        self.setModal(True)
        
        # 建立佈局
        layout = QVBoxLayout()
        
        # 建立載入動畫
        loading_widget = CircularLoadingWidget()
        layout.addWidget(loading_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 載入標籤
        label = QLabel("載入中...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        self.setLayout(layout)
        
        # 設定大小
        self.setFixedSize(300, 250)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 顯示載入對話框
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()
        
        # 模擬初始化過程
        QTimer.singleShot(2000, self.initialize_main_window)
    
    def initialize_main_window(self):
        # 設定視窗標題和大小
        self.setWindowTitle("主介面")
        self.setFixedSize(400, 500)
        
        # 建立中央元件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 建立垂直佈局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加一些元件
        label = QLabel("歡迎使用")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # 關閉載入對話框
        self.loading_dialog.close()
        
        # 顯示主視窗
        self.show()

def main():
    # 建立應用程式
    app = QApplication(sys.argv)
    
    # 建立主視窗
    window = MainWindow()
    
    # 執行應用程式
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
