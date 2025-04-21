# UI
from PyQt6 import QtWidgets, QtGui, QtCore
import sys
# Google Calendar API
from PyQt6 import QtWidgets
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
# Common
import os
import time
import datetime
import random
# graph
import plotly
# backend
import backend

# UI APP
app = QtWidgets.QApplication(sys.argv)

COLORS = {"top_color": "#007acc",
          "side_color": "#0288d1",
          "main_color": "#e0f2f1",
          "header_color": "#01a1ff",
          "button_color": "#007acc",
          "line_color": "rgba(0, 0, 0, 0.1)",
          "remark_color": "rgba(0, 0, 0, 0.5)",
          "white": "#ffffff",
          "green": "#00796b"}
FONT = QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont("./GenSenRounded2TW-R.otf"))[0]
FONTS = {"h1": QtGui.QFont(FONT, 24, QtGui.QFont.Weight.Bold),
         "h2": QtGui.QFont(FONT, 16),
         "content": QtGui.QFont(FONT, 12),
         "remark": QtGui.QFont(FONT, 8)}

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "./credentials.json"
TOKEN_FILE = "./token.json"

try:
    credentials = None
    # 檢查是否已有憑證
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 如果憑證無效，重新授權
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        
        # 儲存新的憑證
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())

    # 建立 Calendar 服務
    service = build('calendar', 'v3', credentials=credentials)
except Exception as e:
    print(e)

data = backend.get_data()
quotes = data["Quotes"]
tasks = data["Tasks"]
page = "Home"

# 基本元件
class Basic(QtWidgets.QMainWindow) :
    def __init__(self):
        super().__init__()

        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.setWindowTitle("任務管理系統")
        self.setWindowIcon(QtGui.QIcon("./icon.ico"))

        self.width = QtWidgets.QApplication.primaryScreen().geometry().width()
        self.height = QtWidgets.QApplication.primaryScreen().geometry().height()

        self.top = Top(self)
        self.side = Side(self)
        self.main = Main(self)
        self.add = Add(self)

        self.top.show()
        self.side.show()
        self.main.show()

    def resizeEvent(self, event):
        self.width = self.size().width()
        self.height = self.size().height()

        super().resizeEvent(event)

class Top(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.x = 0
        self.y = 0
        self.width = self.parent.width
        self.height = int(self.parent.height * 0.08)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(f"background: {COLORS['top_color']}")

        self.home_frame = QtWidgets.QFrame(self)
        self.home_layout = QtWidgets.QHBoxLayout(self.home_frame)
        self.home_frame_x = int(self.width * 0.001)
        self.home_frame_y = 0
        self.home_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.home_frame.mousePressEvent = lambda event: self.back_home(event)

        self.home_icon = QtWidgets.QLabel(self.home_frame)
        icon = QtGui.QPixmap("./icon.png")
        icon = icon.scaled(int(self.width * 0.04), int(self.width * 0.04), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.home_icon.setPixmap(icon)
        self.home_layout.addWidget(self.home_icon)

        self.home_text = QtWidgets.QLabel(self.home_frame, text = "任務管理系統")
        self.home_text.setStyleSheet(f"color: {COLORS['white']}")
        self.home_text.setFont(FONTS["h1"])
        self.home_layout.addWidget(self.home_text)
        self.home_frame.move(self.home_frame_x, self.home_frame_y)
        self.home_frame.show()

    def back_home(self, event) :
        global page
        page = "Home"

class Side(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.x = 0
        self.y = int(self.parent.height * 0.08)
        self.width = int(self.parent.width * 0.15)
        self.height = int(self.parent.height * 0.92)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setStyleSheet(f"background: {COLORS['side_color']}")

class Main(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        # region: main area
        self.setWidgetResizable(True)
        # 修改：使用更靈活的大小策略
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.parent = parent
        self.x = int(self.parent.width * 0.15)
        self.y = int(self.parent.height * 0.08)
        self._width = int(self.parent.width * 0.85)
        self._height = int(self.parent.height * 0.92)
        
        # 修改：僅設置最小高度而非固定高度
        self.setMinimumHeight(self._height)
        self.setMinimumWidth(self._width)  # 修改：使用最小寬度而非固定寬度
        self.move(self.x, self.y)
        self.setStyleSheet(f'''QScrollBar:vertical {{
                            width: 10px;
                            background: {COLORS["white"]};  /* 背景顏色 */
                            margin: 0px 0px 0px 0px;
                        }}
                        
                        QScrollBar::handle:vertical {{
                            background: {COLORS['line_color']};  /* 滑塊顏色 */
                            min-height: 20px;  /* 最小高度 */
                            border-radius: 50;  /* 圓角 */
                        }}
                        
                        QScrollBar::handle:vertical:hover {{
                            background: rgba(0, 0, 0, 0.3);  /* 懸停時顏色 */
                        }}
                        
                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                            height: 0px;  /* 隱藏箭頭 */
                        }}''')

        # 創建主框架
        self.frame = QtWidgets.QFrame()
        self.frame.setStyleSheet(f'''background: {COLORS['main_color']}''')
        # 修改：添加主布局管理器
        self.main_layout = QtWidgets.QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setWidget(self.frame)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # endregion

        # region: great area
        self.greet_frame = QtWidgets.QFrame()  # 修改：移除父元素參數
        self.greet_frame.setStyleSheet(f'''background: {COLORS['header_color']}''')
        self.greet_layout = QtWidgets.QVBoxLayout(self.greet_frame)
        self.greet_layout.setSpacing(0)
        self.greet_layout.setContentsMargins(0, 20, 0, 20)
        
        self.greet_title = QtWidgets.QLabel(self.greet_frame, text="歡迎來到你的任務管理系統")
        self.greet_title.setStyleSheet(f"color: {COLORS['white']}")
        self.greet_title.setFont(FONTS["h1"])
        self.greet_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.greet_layout.addWidget(self.greet_title)

        self.greet_subtitle = QtWidgets.QLabel(self.greet_frame, text=quotes[random.randint(1, 10)])
        self.greet_subtitle.setStyleSheet(f"color: {COLORS['white']}")
        self.greet_subtitle.setFont(FONTS["h2"])
        self.greet_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.greet_layout.addWidget(self.greet_subtitle)

        self.greet_button = QtWidgets.QPushButton(self.greet_frame, text="新建任務")
        self.greet_button.setFont(FONTS["content"])
        self.greet_button.setStyleSheet(f'''background: {COLORS['button_color']};
                                        color: {COLORS['white']};
                                        padding: 10 50 10 50;
                                        border-radius: 5''')
        self.greet_layout.addWidget(self.greet_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # 修改：設置最小高度而非使用setGeometry
        self.greet_frame.setMinimumHeight(int(self._height * 0.3))
        # 修改：將框架添加到主布局
        self.main_layout.addWidget(self.greet_frame)
        # endregion

        # region: to-do area
        self.to_do_frame = QtWidgets.QFrame()  # 修改：移除父元素參數
        self.to_do_frame.setObjectName("to_do_frame")
        self.to_do_frame.setStyleSheet(f'''#to_do_frame {{
                                       border: none;
                                       border-bottom: 2px solid {COLORS["line_color"]}
        }}''')
        self.to_do_layout = QtWidgets.QHBoxLayout(self.to_do_frame)
        self.to_do_layout.setContentsMargins(0, 20, 0, 20)
        
        self.to_do_title = QtWidgets.QLabel(self.to_do_frame, text="今日代辦事項")
        self.to_do_title.setStyleSheet(f"color: {COLORS['green']}")
        self.to_do_title.setFont(FONTS["h1"])
        self.to_do_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.to_do_layout.addWidget(self.to_do_title)

        self.to_do_task_frame = QtWidgets.QFrame(self.to_do_frame)
        self.to_do_task_layout = QtWidgets.QVBoxLayout(self.to_do_task_frame)
        self.to_do_layout.addWidget(self.to_do_task_frame)
        self.to_do_layout.setContentsMargins(0, 20, 0, 20)

        for task in tasks:
            if task != None:
                task_frame = QtWidgets.QFrame(self.to_do_task_frame)
                task_frame.setObjectName("custom-task-frame")
                task_frame.setStyleSheet(f'''#custom-task-frame {{
                                        border: none;
                                        border-bottom: 2px solid {COLORS['line_color']};
                                        }}''')
                task_layout = QtWidgets.QVBoxLayout(task_frame)
                task_layout.setContentsMargins(0, 0, 0, 0)
                
                task_name = QtWidgets.QLabel(task_frame, text=task)
                task_name.setFont(FONTS["content"])
                task_layout.addWidget(task_name)

                task_status = QtWidgets.QLabel(task_frame, text="今日預計完成")
                task_status.setStyleSheet(f"color: {COLORS['remark_color']}")
                task_status.setFont(FONTS["remark"])
                task_layout.addWidget(task_status)

                task_layout.addSpacing(5)

                self.to_do_task_layout.addWidget(task_frame)

        # 修改：設置最小高度而非固定高度
        self.to_do_frame.setMinimumHeight(self.to_do_frame.sizeHint().height())
        # 修改：將框架添加到主布局
        self.main_layout.addWidget(self.to_do_frame)
        # endregion

        # region: graph area
        self.graph_frame = QtWidgets.QFrame()  # 修改：移除父元素參數
        self.graph_frame.setObjectName("graph_frame")
        self.graph_frame.setStyleSheet(f'''#graph_frame {{
                                       border: none;
                                       border-bottom: 2px solid {COLORS['line_color']}
        }}''')
        self.graph_layout = QtWidgets.QVBoxLayout(self.graph_frame)
        self.graph_layout.setContentsMargins(0, 20, 0, 20)

        self.graph_title = QtWidgets.QLabel(self.graph_frame, text="任務進度與報表")
        self.graph_title.setStyleSheet(f"color: {COLORS['green']}")
        self.graph_title.setFont(FONTS["h1"])
        self.graph_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.graph_layout.addWidget(self.graph_title)

        self.graph_subtitle = QtWidgets.QLabel(self.graph_frame, text="查看你的任務完成度、估耗點與身心值等資料")
        self.graph_subtitle.setFont(FONTS["h2"])
        self.graph_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.graph_layout.addWidget(self.graph_subtitle)

        self.graph_button = QtWidgets.QPushButton(self.graph_frame, text="查看報表")
        self.graph_button.setStyleSheet(f'''background: {COLORS['button_color']};
                                        color: {COLORS["white"]};
                                        padding: 10 50 10 50;
                                        border-radius: 5;''')
        self.graph_button.setFont(FONTS["content"])
        self.graph_layout.addWidget(self.graph_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # 修改：設置最小高度而非使用setGeometry
        self.graph_frame.setMinimumHeight(int(self._height * 0.3))
        # 修改：將框架添加到主布局
        self.main_layout.addWidget(self.graph_frame)
        # endregion

        # region: calendar area
        self.calendar_frame = QtWidgets.QFrame()  # 修改：移除父元素參數
        self.calendar_frame.setObjectName("calendar_frame")
        self.calendar_frame.setStyleSheet(f'''#calendar_frame {{
                                          border: none;
                                          border-bottom: 2px solid {COLORS['line_color']}
        }}''')
        self.calendar_layout = QtWidgets.QVBoxLayout(self.calendar_frame)
        self.calendar_layout.setContentsMargins(0, 20, 0, 20)

        self.calendar_title = QtWidgets.QLabel(self.calendar_frame, text="任務日曆")
        self.calendar_title.setStyleSheet(f"color: {COLORS['green']}")
        self.calendar_title.setFont(FONTS["h1"])
        self.calendar_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.calendar_layout.addWidget(self.calendar_title)

        self.calendar_subtitle = QtWidgets.QLabel(self.calendar_frame, text="查看你規劃的任務與相關日程")
        self.calendar_subtitle.setFont(FONTS["h2"])
        self.calendar_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.calendar_layout.addWidget(self.calendar_subtitle)

        self.calendar_buttom = QtWidgets.QPushButton(self.calendar_frame, text = "查看日曆")
        self.calendar_buttom.setStyleSheet(f'''background: {COLORS['button_color']};
                                           color: {COLORS['white']};
                                           padding: 10 50 10 50;
                                           border-radius: 5;''')
        self.calendar_buttom.setFont(FONTS["content"])
        self.calendar_layout.addWidget(self.calendar_buttom, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)

        self.calendar_frame.setMinimumHeight(int(self._height * 0.3))
        self.main_layout.addWidget(self.calendar_frame)
        # endregion

        self.main_layout.addStretch(1)

        self.home()

    def initialize(self) :
        self.greet_frame.hide()
        self.to_do_frame.hide()
        self.graph_frame.hide()
        self.calendar_frame.hide()

    def home(self):
        self.greet_frame.show()
        self.to_do_frame.show()
        self.graph_frame.show()
        self.calendar_frame.show()

    def graph(self) :
        print("graph")

class Add(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

if __name__ == "__main__" :
    basic = Basic()
    basic.show()
    # basic.showMaximized()
    sys.exit(app.exec())