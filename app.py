# UI
from PyQt6 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets, QtWebEngineCore
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
# multithreading
import threading
# backend
import backend

# UI APP
app = QtWidgets.QApplication(sys.argv)

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
FONT = QtGui.QFontDatabase.applicationFontFamilies(QtGui.QFontDatabase.addApplicationFont("./GenSenRounded2TW-R.otf"))[0]
FONTS = {"h1": QtGui.QFont(FONT, 24, QtGui.QFont.Weight.Bold),
         "h2": QtGui.QFont(FONT, 16),
         "content": QtGui.QFont(FONT, 12),
         "remark": QtGui.QFont(FONT, 8),
         "menu": QtGui.QFont(FONT, 16),
         "highlight": QtGui.QFont(FONT, 18, QtGui.QFont.Weight.Bold)}

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

try:
    credentials = None
    # 檢查是否已有憑證
    if os.path.exists(TOKEN_FILE):
        try:
            credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as load_error:
            print(f"載入憑證失敗: {load_error}")
            credentials = None

    # 如果憑證無效，重新授權
    if not credentials or not credentials.valid:
        try:
            # 嘗試刷新 Token
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                # 重新授權流程
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                credentials = flow.run_local_server(
                    port=0, 
                    open_browser=True,
                    prompt='consent'
                )
            
            # 儲存新的憑證
            with open(TOKEN_FILE, 'w') as token:
                token.write(credentials.to_json())

        except Exception as auth_error:
            print(f"授權過程發生錯誤: {auth_error}")
            raise

    # 強制刷新 Token
    credentials.refresh(Request())
    
    # 建立 Calendar 服務
    service = build('calendar', 'v3', credentials=credentials)

except Exception as e:
    print(f"發生錯誤: {e}")
    service = None

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
        # self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowM\mizeButtonHint | QtCore.Qt.WindowType.WindowCloseButtonHint)

        self._width = QtWidgets.QApplication.primaryScreen().geometry().width()
        self._height = QtWidgets.QApplication.primaryScreen().geometry().height()
        # self.setFixedSize(self._width, self._height)

        self.top = Top(self)
        self.side = Side(self)
        self.add = Add(self)
        self.main = Main(self)
        
        self.circularLoadingWidget = CircularLoadingWidget()

        self.circularLoadingWidget.show()
        self.top.show()
        self.side.show()
        self.main.show()

    def resizeEvent(self, event):
        self._width = self.size().width()
        self._height = self.size().height()

        super().resizeEvent(event)
    
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'circularLoadingWidget') and self.circularLoadingWidget:
            self.circularLoadingWidget.close()
    
    def closeEvent(self, event):
        super().closeEvent(event)
        backend.update_data(data)

    def update(self) :
        global data, tasks
        data = backend.get_data()
        tasks = data["Tasks"]
        self.side.project()
        self.main.task()

class Top(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

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
        icon = QtGui.QPixmap("./icon.png")
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
        global page
        page = "Home"
        self.parent.side.initialize(event)
        self.parent.add.initialize()
        self.parent.main.home()

class Side(QtWidgets.QScrollArea) :
    def __init__(self, parent):
        super().__init__(parent)
        # region: basic settings
        self.setWidgetResizable(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.parent = parent
        self.x = 0
        self.y = int(self.parent._height * 0.1)
        self._width = int(self.parent._width * 0.2)
        self._height = int(self.parent._height * 0.9)
        self.setMinimumHeight(self._height)
        self.setMinimumWidth(self._width)
        self.move(self.x, self.y)
        self.setStyleSheet(f'''QScrollBar:vertical{{
                            width: 0px;
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
        
        self.frame = QtWidgets.QFrame()
        self.frame.setStyleSheet(f'''background: {COLORS['side_color']}''')
        # 修改：添加主布局管理器
        self.main_layout = QtWidgets.QVBoxLayout(self.frame)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 0, 0)
        self.main_layout.setSpacing(20)
        
        self.setWidget(self.frame)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # endregion

        self.project()

    def initialize(self, event) :
        for i in range(self.main_layout.count()) :
            widget = self.main_layout.itemAt(i).widget()
            if widget and not isinstance(widget, QtWidgets.QPushButton) :
                widget.setFont(FONTS["menu"])

    def project(self) :
        for i in range(self.main_layout.count())[::-1] :
            widget = self.main_layout.itemAt(i)
            if widget :
                widget = widget.widget()
                self.main_layout.removeWidget(widget)
                widget.deleteLater()
        # region: menu
        self.graph = QtWidgets.QLabel(self, text = "儀表板")
        self.graph.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.graph.setFont(FONTS["menu"])
        self.graph.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.graph)
        self.main_layout.addWidget(self.graph)

        self.calendar = QtWidgets.QLabel(self, text = "日曆")
        self.calendar.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.calendar.setFont(FONTS['menu'])
        self.calendar.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.calendar)
        self.main_layout.addWidget(self.calendar)

        self.all = QtWidgets.QLabel(self, text = "全部任務")
        self.all.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.all.setFont(FONTS["menu"])
        self.all.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.all)
        self.main_layout.addWidget(self.all)

        self.menu_dict = {}
        for project in list(tasks.keys()) :
            menu = QtWidgets.QLabel(self, text = project.replace('"', ""))
            menu.setStyleSheet(f"color: {COLORS['primary_black']}")
            menu.setFont(FONTS["menu"])
            menu.mousePressEvent = lambda event, m = menu: self.handle_mouseEvent(event, m)
            self.main_layout.addWidget(menu)

        self.add_project = QtWidgets.QPushButton(self, text = "新增專案")
        self.add_project.clicked.connect(self.func_add_project)
        self.add_project.setFont(FONTS["h2"])
        self.add_project.setStyleSheet(f'''QPushButton{{
                                       color: {COLORS['white']};
                                       background: {COLORS['primary_button']};
                                       border-radius: 5px;
                                       margin-right: 20px;
                                       padding: 5 0 5 0}}
                                       QPushButton:hover{{
                                       background: {COLORS['primary_button:hover']}
                                       }}''')
        self.main_layout.addWidget(self.add_project)

    def switch_page(self, event, label: QtWidgets.QLabel) :
        global page
        page = label.text()
        label.setFont(FONTS["highlight"])

        if page == "日曆" :
            self.parent.main.calendar()
        elif page == "儀表板" :
            self.parent.main.graph()
        else :
            self.parent.main.task()

    def handle_mouseEvent(self, event, label) :
        self.initialize(event)
        self.switch_page(event, label)

    def func_add_project(self) :
        self.parent.add.add_project()

class Main(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        global page
        # region: main area
        self.setWidgetResizable(True)
        # 修改：使用更靈活的大小策略
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.parent = parent
        self.x = int(self.parent._width * 0.2)
        self.y = int(self.parent._height * 0.1)
        self._width = int(self.parent._width * 0.8)
        self._height = int(self.parent._height * 0.9)
        
        # 修改：僅設置最小高度而非固定高度
        self.setMinimumHeight(self._height)
        self.setMinimumWidth(self._width)  # 修改：使用最小寬度而非固定寬度
        self.move(self.x, self.y)
        self.setStyleSheet(f'''QScrollBar:vertical {{
                            width: 0px;
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
        self.greet_frame.setStyleSheet(f'''background: {COLORS['header_color']};''')
        self.greet_layout = QtWidgets.QVBoxLayout(self.greet_frame)
        self.greet_layout.setSpacing(0)
        self.greet_layout.setContentsMargins(0, 20, 0, 20)
        
        self.greet_title = QtWidgets.QLabel(self.greet_frame, text="歡迎來到你的任務管理系統")
        self.greet_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.greet_title.setFont(FONTS["h1"])
        self.greet_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.greet_layout.addWidget(self.greet_title)

        self.greet_subtitle = QtWidgets.QLabel(self.greet_frame, text=quotes[random.randint(1, 10)])
        self.greet_subtitle.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.greet_subtitle.setFont(FONTS["h2"])
        self.greet_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.greet_layout.addWidget(self.greet_subtitle)

        self.greet_button = QtWidgets.QPushButton(self.greet_frame, text="新建任務")
        self.greet_button.clicked.connect(self.parent.add.add_task)
        self.greet_button.setFont(FONTS["content"])
        self.greet_button.setStyleSheet(f'''QPushButton{{
                                        background: {COLORS['primary_button']};
                                        color: {COLORS['white']};
                                        padding: 10 50 10 50;
                                        border-radius: 5}}
                                        QPushButton:hover{{
                                        background: {COLORS['primary_button:hover']}
                                        }}''')
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
        self.to_do_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.to_do_title.setFont(FONTS["h1"])
        self.to_do_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.to_do_layout.addWidget(self.to_do_title)

        self.to_do_task_frame = QtWidgets.QFrame(self.to_do_frame)
        self.to_do_task_layout = QtWidgets.QVBoxLayout(self.to_do_task_frame)
        self.to_do_layout.addWidget(self.to_do_task_frame)
        self.to_do_layout.setContentsMargins(0, 20, 0, 20)

        for project in list(tasks.keys()):
            for task in list(tasks[project].keys()) :
                if task != None and task != "setting" :
                    try :
                        if datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                            show = True
                        elif datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                            show = True
                        else :
                            show = False
                    except KeyError :
                        show = False
                    
                    if not show :
                        try :
                            if datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                                show = True
                            else :
                                show = False
                        except KeyError :
                            show = False

                    if show :
                        pass
                    else :
                        continue
                    
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
                    task_name.setStyleSheet(f'''color: {COLORS['secondary_black']};''')
                    task_layout.addWidget(task_name)

                    try :
                        if datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                            task_status = QtWidgets.QLabel(task_frame, text="今日必須完成")
                            task_status.setStyleSheet(f"color: {COLORS['common_black']}")
                            task_status.setFont(FONTS["remark"])
                            task_layout.addWidget(task_status)
                        elif datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                            task_status = QtWidgets.QLabel(task_frame, text="今日過期任務")
                            task_status.setStyleSheet(f"color: {COLORS['red']}")
                            task_status.setFont(FONTS["remark"])
                            task_layout.addWidget(task_status)
                    except KeyError :
                        pass

                    try :
                        if datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                            task_status = QtWidgets.QLabel(task_frame, text="今日預計完成")
                            task_status.setStyleSheet(f"color: {COLORS['common_black']}")
                            task_status.setFont(FONTS["remark"])
                            task_layout.addWidget(task_status)
                    except KeyError :
                        pass

                    task_layout.addSpacing(5)

                    self.to_do_task_layout.addWidget(task_frame)

        self.to_do_frame.setMinimumHeight(self.to_do_frame.sizeHint().height())
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
        self.graph_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.graph_title.setFont(FONTS["h1"])
        self.graph_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.graph_layout.addWidget(self.graph_title)

        self.graph_subtitle = QtWidgets.QLabel(self.graph_frame, text="查看你的任務完成度、估耗點與身心值等資料")
        self.graph_subtitle.setFont(FONTS["h2"])
        self.graph_subtitle.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.graph_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.graph_layout.addWidget(self.graph_subtitle)

        self.graph_button = QtWidgets.QPushButton(self.graph_frame, text="查看報表")
        self.graph_button.setStyleSheet(f'''QPushButton{{
                                        background: {COLORS['primary_button']};
                                        color: {COLORS["white"]};
                                        padding: 10 50 10 50;
                                        border-radius: 5;}}
                                        QPushButton:hover{{
                                        background: {COLORS['primary_button:hover']}
                                        }}''')
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
        self.calendar_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.calendar_title.setFont(FONTS["h1"])
        self.calendar_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.calendar_layout.addWidget(self.calendar_title)

        self.calendar_subtitle = QtWidgets.QLabel(self.calendar_frame, text="查看你規劃的任務與相關日程")
        self.calendar_subtitle.setFont(FONTS["h2"])
        self.calendar_subtitle.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.calendar_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.calendar_layout.addWidget(self.calendar_subtitle)

        self.calendar_buttom = QtWidgets.QPushButton(self.calendar_frame, text = "查看日曆")
        self.calendar_buttom.setStyleSheet(f'''QPushButton{{
                                           background: {COLORS['primary_button']};
                                           color: {COLORS['white']};
                                           padding: 10 50 10 50;
                                           border-radius: 5;}}
                                           QPushButton:hover{{
                                           background: {COLORS['primary_button:hover']}
                                           }}''')
        self.calendar_buttom.setFont(FONTS["content"])
        self.calendar_layout.addWidget(self.calendar_buttom, alignment = QtCore.Qt.AlignmentFlag.AlignCenter)

        self.calendar_frame.setMinimumHeight(int(self._height * 0.3))
        self.main_layout.addWidget(self.calendar_frame)
        # endregion

        # region: graph page
        self.total_graph_frame = QtWidgets.QFrame()
        self.total_graph_frame.setObjectName("total_graph_area")
        self.total_graph_frame.setStyleSheet(f'''#total_graph_area{{
                                            border: none;
                                            border-bottom: 2px solid {COLORS["line_color"]};
        }}''')
        self.total_graph_layout = QtWidgets.QVBoxLayout(self.total_graph_frame)
        self.total_graph_layout.setContentsMargins(0, 20, 0, 20)
        # endregion

        # region: calendar page
        profile_path = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(profile_path, "Calendar_Profile") # 指定並創建目錄
        os.makedirs(profile_path, exist_ok=True) # 確保目錄存在
        if profile_path :
            self.profile = QtWebEngineCore.QWebEngineProfile("PersistentCalendarProfile", self)
            self.profile.setPersistentStoragePath(profile_path)
            self.profile.setPersistentCookiesPolicy(QtWebEngineCore.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
            self.profile.setCachePath(profile_path) # 通常快取也放一起
            self.profile.setHttpCacheType(QtWebEngineCore.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        else :
            self.profile = QtWebEngineCore.QWebEngineProfile(self) # 使用預設 Profile
        self.calendar_page = QtWebEngineWidgets.QWebEngineView()
        self.page = QtWebEngineCore.QWebEnginePage(self.profile, self)
        self.calendar_page.setPage(self.page)
        self.calendar_page.setUrl(QtCore.QUrl("https://calendar.google.com"))
        self.main_layout.addWidget(self.calendar_page)
        self.calendar_page.setFixedSize(self._width, self._height)
        # endregion

        # region: task page
        self.task_page = QtWidgets.QFrame()
        self.task_page.setStyleSheet(f"background: {COLORS['main_color']}")
        self.task_layout = QtWidgets.QGridLayout(self.task_page)
        self.task_layout.setContentsMargins(10, 20, 10, 20)
        self.task_layout.setSpacing(int(0.02*self._width))
        
        self.project_title = QtWidgets.QLabel(text = page)
        self.project_title.setFont(FONTS["h1"])
        self.project_title.setStyleSheet(f'''color: {COLORS['primary_black']}''')
        self.task_layout.addWidget(self.project_title, 0, 0, 1, 2)

        self.add_task_button = QtWidgets.QPushButton(text = "新增")
        self.add_task_button.setFont(FONTS["h2"])
        self.add_task_button.setStyleSheet(f'''QPushButton{{
                                           background: {COLORS['primary_button']};
                                           color: {COLORS["white"]};}}
                                           QPushButton:hover{{
                                           background: {COLORS['primary_button:hover']}
                                           }}''')
        self.add_task_button.setFixedWidth(self.add_task_button.sizeHint().width())
        self.add_task_button.clicked.connect(lambda: self.parent.add.add_task())
        self.task_layout.addWidget(self.add_task_button, 0, 2, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
        # endregion

        self.grid = 1
        self.column = 0

        self.main_layout.addWidget(self.task_page)

        self.main_layout.addStretch(1)

        self.home()

    def initialize(self) :
        self.greet_frame.hide()
        self.to_do_frame.hide()
        self.graph_frame.hide()
        self.calendar_frame.hide()
        self.calendar_page.setVisible(False)
        self.task_page.hide()
        self.task_layout.removeWidget(self.project_title)
        self.task_layout.removeWidget(self.add_task_button)
        while self.task_layout.count() > 0 :
            item = self.task_layout.takeAt(0)
            frame = item.widget()
            if frame and not (isinstance(frame, QtWidgets.QLabel) or isinstance(frame, QtWidgets.QPushButton)) :
                self.task_layout.removeWidget(frame)
                frame.deleteLater()
        self.task_layout.addWidget(self.project_title, 0, 0, 1, 2)
        self.task_layout.addWidget(self.add_task_button, 0, 2, alignment = QtCore.Qt.AlignmentFlag.AlignRight)

    def home(self):
        self.initialize()
        self.greet_frame.show()
        self.to_do_frame.show()
        self.graph_frame.show()
        self.calendar_frame.show()

    def graph(self) :
        self.initialize()

    def calendar(self) :
        self.initialize()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.calendar_page.setVisible(True)
    
    def task(self) :
        self.initialize()
        self.project_title.setText(page)
        self.row = 1
        self.column = 0
        if page == "全部任務" :
            for project in list(tasks.keys()) :
                for task in list(tasks[project].keys()) :
                    if task == "setting" :
                        continue
                    task_frame = QtWidgets.QFrame()
                    task_frame.setStyleSheet(f'''background: {COLORS["white"]};
                                             border-radius: 5''')
                    task_frame.setFixedSize(int(self._width*0.3), int(self._height*0.2))
                    shadow = QtWidgets.QGraphicsDropShadowEffect()
                    shadow.setBlurRadius(4)
                    shadow.setColor(QtGui.QColor(COLORS["shadow"]))
                    shadow.setOffset(2, 2)
                    task_frame.setGraphicsEffect(shadow)
                    task_layout = QtWidgets.QGridLayout(task_frame)

                    task_title = QtWidgets.QLabel(f'{project}: {task}')
                    task_title.setFont(FONTS["content"])
                    task_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
                    task_layout.addWidget(task_title, 0, 0)

                    if tasks[project][task].get("limit_time") :
                        task_limit_time = QtWidgets.QLabel(f'截止時間: {tasks[project][task].get("limit_time")}')
                        task_limit_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                            task_limit_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_limit_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_limit_time, 1, 0)
                    
                    match (tasks[project][task].get("expect_time1"), tasks[project][task].get("expect_time2")) :
                        case (None, None) :
                            pass
                        case (_, None) :
                            task_expect_time = QtWidgets.QLabel(f'預計完成時間: {tasks[project][task].get("expect_time1")}')
                            task_expect_time.setFont(FONTS["remark"])
                            if datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                            else :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                            task_layout.addWidget(task_expect_time, 2, 0)
                        case (_, _) :
                            task_expect_time = QtWidgets.QLabel(f'預計完成時間: {tasks[project][task].get("expect_time1")}~{tasks[project][task].get("expect_time2")}')
                            task_expect_time.setFont(FONTS["remark"])
                            if datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                            else :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                            task_layout.addWidget(task_expect_time, 2, 0)
                        
                    if tasks[project][task].get("task_remark") :
                        task_remark = QtWidgets.QLabel(f'{tasks[project][task].get("task_remark")}')
                        task_remark.setFont(FONTS["remark"])
                        task_remark.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_remark, 1, 0)
                    
                    task_status = QtWidgets.QLabel(text = f"{tasks[project][task]['status']}")
                    task_status.setFont(FONTS["remark"])
                    task_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    match tasks[project][task].get("status") :
                        case "未開始" :
                            task_status.setStyleSheet(f'''color: {COLORS['common_black']};
                            background: {COLORS['undo']};''')
                        case "進行中" :
                            task_status.setStyleSheet(f'''color: {COLORS['white']};
                            background: {COLORS['doing']}''')
                        case "已完成" :
                            task_status.setStyleSheet(f'''color: {COLORS['white']};
                            background: {COLORS['done']}''')
                    task_status.mousePressEvent = lambda event, l = task_status, t = task_title.text().split(" ")[-1], p = project: self.change_status(event, label = l, task = t, project = p, now_status = f"{l.text()}")
                    task_layout.addWidget(task_status, 3, 0)

                    self.task_layout.addWidget(task_frame, self.row, self.column)
                    if self.column == 2 :
                        self.row += 1
                        self.column = 0
                    else :
                        self.column += 1
        else :
            for task in list(tasks[page].keys()) :
                if task == "setting" :
                    continue
                task_frame = QtWidgets.QFrame()
                task_frame.setStyleSheet(f'''background: {COLORS["white"]};
                                            border-radius: 5''')
                task_frame.setFixedSize(int(self._width*0.3), int(self._height*0.2))
                shadow = QtWidgets.QGraphicsDropShadowEffect()
                shadow.setBlurRadius(4)
                shadow.setColor(QtGui.QColor(COLORS["shadow"]))
                shadow.setOffset(2, 2)
                task_frame.setGraphicsEffect(shadow)
                task_layout = QtWidgets.QGridLayout(task_frame)

                task_title = QtWidgets.QLabel(f'{task}')
                task_title.setFont(FONTS["content"])
                task_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
                task_layout.addWidget(task_title, 0, 0)

                if tasks[page][task].get("limit_time") :
                    task_limit_time = QtWidgets.QLabel(f'截止時間: {tasks[page][task].get("limit_time")}')
                    task_limit_time.setFont(FONTS["remark"])
                    if datetime.datetime.strptime(tasks[page][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                        task_limit_time.setStyleSheet(f'''color: {COLORS['red']}''')
                    else :
                        task_limit_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                    task_layout.addWidget(task_limit_time, 1, 0)
                
                match (tasks[page][task].get("expect_time1"), tasks[page][task].get("expect_time2")) :
                    case (None, None) :
                        pass
                    case (_, None) :
                        task_expect_time = QtWidgets.QLabel(f'預計完成時間: {tasks[page][task].get("expect_time1")}')
                        task_expect_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(tasks[page][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_expect_time, 2, 0)
                    case (_, _) :
                        task_expect_time = QtWidgets.QLabel(f'預計完成時間: {tasks[page][task].get("expect_time1")}~{tasks[page][task].get("expect_time2")}')
                        task_expect_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(tasks[page][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_expect_time, 2, 0)

                if tasks[page][task].get("task_remark") :
                    task_remark = QtWidgets.QLabel(f'{tasks[page][task].get("task_remark")}')
                    task_remark.setFont(FONTS["remark"])
                    task_remark.setStyleSheet(f'''color: {COLORS['common_black']}''')
                    task_layout.addWidget(task_remark, 1, 0)

                task_status = QtWidgets.QLabel(text = f"{tasks[page][task]['status']}")
                task_status.setFont(FONTS["remark"])
                task_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                match tasks[page][task].get("status") :
                    case "未開始" :
                        task_status.setStyleSheet(f'''color: {COLORS['common_black']};
                        background: {COLORS['undo']}''')
                    case "進行中" :
                        task_status.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    case "已完成" :
                        task_status.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['done']}''')
                task_status.mousePressEvent = lambda event, l = task_status, t = task_title.text().split(" ")[-1], p = page: self.change_status(event, label = l, task = t, project = p, now_status = f"{l.text()}")
                task_layout.addWidget(task_status, 3, 0)

                self.task_layout.addWidget(task_frame, self.row, self.column)
                if self.column == 2 :
                    self.row += 1
                    self.column = 0
                else :
                    self.column += 1

        self.task_page.show()
    
    def change_status(self, event, label: QtWidgets.QLabel, task: str, project: str, now_status: str) :
        global tasks
        match now_status :
            case "未開始" :
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    label.setText("進行中")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    tasks[project][task]["status"] = "進行中"
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    pass
            case "進行中" :
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    label.setText("已完成")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['done']}''')
                    tasks[project][task]["status"] = "已完成"
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    label.setText("未開始")
                    label.setStyleSheet(f'''color: {COLORS['common_black']};
                        background: {COLORS['undo']}''')
                    tasks[project][task]["status"] = "未開始"
            case "已完成":
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    pass
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    label.setText("進行中")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    tasks[project][task]["status"] = "進行中"

class Add(QtWidgets.QFrame) :
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self._width = self.parent._width
        self._height = int(self.parent._height * 0.9)
        self._x = 0
        self._y = int(self.parent._height * 0.1)
        self.setGeometry(self._x, self._y, self._width, self._height)
        self.setStyleSheet(f"background: {COLORS['main_color']}")

        # region: add task
        self.add_task_frame = QtWidgets.QFrame(self)
        self.add_task_frame.setStyleSheet(f'''background: {COLORS["main_color"]};''')
        self.add_task_layout = QtWidgets.QGridLayout(self)
        self.add_task_layout.setSpacing(10)
        self.add_task_frame.setLayout(self.add_task_layout)
        self.add_task_frame.setGeometry(int(0.25*self._width), int(0.13*self.parent._height), int(0.5*self._width), int(0.6*self._height))

        self.add_task_title = QtWidgets.QLabel(self, text = "新增任務")
        self.add_task_title.setFont(FONTS["h1"])
        self.add_task_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.add_task_title.adjustSize()
        self.add_task_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.add_task_title.move(int(0.5*self.parent._width - 0.5*self.add_task_title.width()), int(0.05*self.parent._height))
        
        self.task_name_line = QtWidgets.QLabel(text = "任務名稱")
        self.task_name_line.setFont(FONTS['h2'])
        self.task_name_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_name_line, 0, 0, 1, 3)

        self.task_name_input = QtWidgets.QLineEdit()
        self.task_name_input.setFont(FONTS["content"])
        self.task_name_input.setStyleSheet(f'''color: {COLORS['common_black']};
                                           background: {COLORS["white"]};
                                           border-radius: 5;
                                           padding-left: 5px''')
        self.add_task_layout.addWidget(self.task_name_input, 1, 0, 1, 3)

        self.task_belong_project_line = QtWidgets.QLabel(text = "所屬專案")
        self.task_belong_project_line.setFont(FONTS["h2"])
        self.task_belong_project_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_belong_project_line, 0, 3, 1, 3)

        self.task_belong_project_input = QtWidgets.QComboBox()
        self.task_belong_project_input.addItems(list(tasks.keys()))
        self.task_belong_project_input.setFont(FONTS["content"])
        self.task_belong_project_input.setStyleSheet(f'''QComboBox{{background: {COLORS["white"]};
                                                     color: {COLORS['common_black']};
                                                     border-radius: 5;
                                                     padding-left: 5px;}}
                                                     QComboBox::drop-down{{
                                                     border-radius: 5;
                                                     }}''')
        self.add_task_layout.addWidget(self.task_belong_project_input, 1, 3, 1, 3)

        self.task_end_time_line = QtWidgets.QLabel(text = "截止時間")
        self.task_end_time_line.setFont(FONTS["h2"])
        self.task_end_time_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_end_time_line, 2, 0, 1, 3)

        self.task_end_time_check = QtWidgets.QCheckBox()
        self.task_end_time_check.setChecked(True)
        self.task_end_time_check.stateChanged.connect(lambda state: self.handle_check(state, self.task_end_time_date, self.task_end_time_time))
        self.task_end_time_check.setFont(FONTS["content"])
        self.task_end_time_check.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_end_time_check, 3, 0, 1, 1)

        self.task_end_time_date = QtWidgets.QDateEdit()
        self.task_end_time_date.setButtonSymbols(QtWidgets.QDateEdit.ButtonSymbols.NoButtons)
        self.task_end_time_date.setDisplayFormat("yyyy/MM/dd")
        self.task_end_time_date.setDate(QtCore.QDate.currentDate())
        self.task_end_time_date.setFont(FONTS["content"])
        self.task_end_time_date.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_end_time_date, 3, 1, 1, 1)

        self.task_end_time_time = QtWidgets.QTimeEdit()
        self.task_end_time_time.setButtonSymbols(QtWidgets.QTimeEdit.ButtonSymbols.NoButtons)
        self.task_end_time_time.setDisplayFormat("hh:mm")
        self.task_end_time_time.setTime(QtCore.QTime(23, 59))
        self.task_end_time_time.setFont(FONTS["content"])
        self.task_end_time_time.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_end_time_time, 3, 2, 1, 1)

        self.task_expect_time_line = QtWidgets.QLabel(text = "預計完成時間")
        self.task_expect_time_line.setFont(FONTS["h2"])
        self.task_expect_time_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_line, 2, 3, 1, 3)

        self.task_expect_time_check1 = QtWidgets.QCheckBox()
        self.task_expect_time_check1.setChecked(True)
        self.task_expect_time_check1.stateChanged.connect(lambda state: self.handle_check(state, self.task_expect_time_date1, self.task_expect_time_time1))
        self.task_expect_time_check1.setFont(FONTS["content"])
        self.task_expect_time_check1.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_check1, 3, 3, 1, 1)

        self.task_expect_time_date1 = QtWidgets.QDateEdit()
        self.task_expect_time_date1.setButtonSymbols(QtWidgets.QDateEdit.ButtonSymbols.NoButtons)
        self.task_expect_time_date1.setDisplayFormat("yyyy/MM/dd")
        self.task_expect_time_date1.setDate(QtCore.QDate.currentDate())
        self.task_expect_time_date1.setFont(FONTS["content"])
        self.task_expect_time_date1.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_date1, 3, 4, 1, 1)

        self.task_expect_time_time1 = QtWidgets.QTimeEdit()
        self.task_expect_time_time1.setButtonSymbols(QtWidgets.QTimeEdit.ButtonSymbols.NoButtons)
        self.task_expect_time_time1.setDisplayFormat("hh:mm")
        self.task_expect_time_time1.setTime(QtCore.QTime(23, 59))
        self.task_expect_time_time1.setFont(FONTS["content"])
        self.task_expect_time_time1.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_time1, 3, 5, 1, 1)

        self.task_expect_time_check2 = QtWidgets.QCheckBox()
        self.task_expect_time_check2.setChecked(False)
        self.task_expect_time_check2.stateChanged.connect(lambda state: self.handle_check(state, self.task_expect_time_date2, self.task_expect_time_time2))
        self.task_expect_time_check2.setFont(FONTS["content"])
        self.task_expect_time_check2.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_check2, 4, 3, 1, 1)

        self.task_expect_time_date2 = QtWidgets.QDateEdit()
        self.task_expect_time_date2.setButtonSymbols(QtWidgets.QDateEdit.ButtonSymbols.NoButtons)
        self.task_expect_time_date2.setDisplayFormat("yyyy/MM/dd")
        self.task_expect_time_date2.setDate(QtCore.QDate())
        self.task_expect_time_date2.setEnabled(False)
        self.task_expect_time_date2.setFont(FONTS["content"])
        self.task_expect_time_date2.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_date2, 4, 4, 1, 1)

        self.task_expect_time_time2 = QtWidgets.QTimeEdit()
        self.task_expect_time_time2.setButtonSymbols(QtWidgets.QTimeEdit.ButtonSymbols.NoButtons)
        self.task_expect_time_time2.setDisplayFormat("hh:mm")
        self.task_expect_time_time2.setTime(QtCore.QTime())
        self.task_expect_time_time2.setEnabled(False)
        self.task_expect_time_time2.setFont(FONTS["content"])
        self.task_expect_time_time2.setStyleSheet(f"color: {COLORS['common_black']}")
        self.add_task_layout.addWidget(self.task_expect_time_time2, 4, 5, 1, 1)

        self.task_expect_point_line = QtWidgets.QLabel(text = "估點")
        self.task_expect_point_line.setFont(FONTS["h2"])
        self.task_expect_point_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_expect_point_line, 5, 0, 1, 3)

        self.task_expect_point_input = QtWidgets.QLineEdit()
        self.task_expect_point_input.setFont(FONTS["content"])
        self.task_expect_point_input.setStyleSheet(f'''color: {COLORS['common_black']};
                                           background: {COLORS["white"]};
                                           border-radius: 5;
                                           padding-left: 5px''')
        self.add_task_layout.addWidget(self.task_expect_point_input, 6, 0, 1, 3)

        self.task_type_line = QtWidgets.QLabel(text = "任務類型")
        self.task_type_line.setFont(FONTS["h2"])
        self.task_type_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_type_line, 5, 3, 1, 3)

        self.task_type_input = QtWidgets.QComboBox()
        self.task_type_input.addItems(["學校功課", "報告製作", "考試", "專案製作"])
        self.task_type_input.currentTextChanged.connect(self.handle_other)
        self.task_type_input.setFont(FONTS["content"])
        self.task_type_input.setStyleSheet(f'''QComboBox{{background: {COLORS["white"]};
                                                     color: {COLORS['common_black']};
                                                     border-radius: 5;
                                                     padding-left: 5px;}}
                                                     QComboBox::drop-down{{
                                                     border-radius: 5;
                                                     }}''')
        self.add_task_layout.addWidget(self.task_type_input, 6, 3, 1, 2)

        self.task_type_other_input = QtWidgets.QLineEdit()
        self.task_type_other_input.setFont(FONTS["content"])
        self.task_type_other_input.setStyleSheet(f'''background: {COLORS["white"]};
                                                     color: {COLORS['common_black']};
                                                     border-radius: 5;
                                                     padding-left: 5px;
                                                     ''')
        self.add_task_layout.addWidget(self.task_type_other_input, 6, 5, 1, 1)
        self.task_type_other_input.setVisible(False)

        self.task_remark_line = QtWidgets.QLabel(text = "備註")
        self.task_remark_line.setFont(FONTS["h2"])
        self.task_remark_line.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.add_task_layout.addWidget(self.task_remark_line, 7, 0, 1, 3)

        self.task_remark_input = QtWidgets.QTextEdit()
        self.task_remark_input.setFont(FONTS["content"])
        self.task_remark_input.setStyleSheet(f'''color: {COLORS['common_black']};
                                           background: {COLORS["white"]};
                                           border-radius: 5;
                                           padding-left: 5px''')
        self.add_task_layout.addWidget(self.task_remark_input, 8, 0, 2, 6)

        self.check_task_button = QtWidgets.QPushButton(self, text = "確認")
        self.check_task_button.clicked.connect(lambda: self.check(type = "task"))
        self.check_task_button.setFont(FONTS["h2"])
        self.check_task_button.setStyleSheet(f'''QPushButton{{
                                             color: {COLORS['white']};
                                             background: {COLORS['secondary_button']};
                                             border-radius: 5px;
                                             padding: 5 10 5 10}}
                                             QPushButton:hover{{
                                             background: {COLORS['secondary_button:hover']}
                                             }}''')
        self.check_task_button.adjustSize()
        self.check_task_button.move(int(0.7*self._width - 0.5*self.check_task_button.width()), int(0.8*self._height - 0.5*self.check_task_button.height()))

        self.add_task_layout.addWidget(self.task_remark_input, 8, 0, 2, 6)

        self.cancel_task_button = QtWidgets.QPushButton(self, text = "取消")
        self.cancel_task_button.clicked.connect(self.initialize)
        self.cancel_task_button.setFont(FONTS["h2"])
        self.cancel_task_button.setStyleSheet(f'''QPushButton{{
                                              color: {COLORS['white']};
                                             background: {COLORS['cancel_button']};
                                             border-radius: 5px;
                                             padding: 5 10 5 10}}
                                             QPushButton:hover{{
                                             background: {COLORS['cancel_button:hover']}
                                             }}''')
        self.cancel_task_button.adjustSize()
        self.cancel_task_button.move(int(0.3*self._width - 0.5*self.cancel_task_button.width()), int(0.8*self._height - 0.5*self.cancel_task_button.height()))
        # endregion

        # region: add peoject
        self.add_project_title = QtWidgets.QLabel(self, text = "新增專案")
        self.add_project_title.setFont(FONTS["h1"])
        self.add_project_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.add_project_title.adjustSize()
        self.add_project_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.add_project_title.move(int(0.5*self.parent._width - 0.5*self.add_project_title.width()), int(0.1*self.parent._height))

        self.add_project_frame = QtWidgets.QFrame(self)
        self.add_project_frame.setStyleSheet(f'''background: {COLORS["main_color"]};''')
        self.add_project_layout = QtWidgets.QGridLayout(self)
        self.add_project_layout.setSpacing(10)
        self.add_project_frame.setLayout(self.add_project_layout)
        self.add_project_frame.setGeometry(int(0.25*self._width), int(0.2*self.parent._height), int(0.5*self._width), int(0.6*self._height))

        self.project_name_title = QtWidgets.QLabel(text = "專案名稱")
        self.project_name_title.setFont(FONTS["h2"])
        self.project_name_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.add_project_layout.addWidget(self.project_name_title, 0, 0, 1, 2)

        self.project_name_input = QtWidgets.QLineEdit()
        self.project_name_input.setFont(FONTS["content"])
        self.project_name_input.setStyleSheet(f'''background: {COLORS["white"]};
                                              color: {COLORS['common_black']};
                                              border-radius: 5px;
                                              padding-left: 5px;''')
        self.add_project_layout.addWidget(self.project_name_input, 1, 0, 1, 2)

        self.project_end_time_title = QtWidgets.QLabel(text = "截止時間")
        self.project_end_time_title.setFont(FONTS["h2"])
        self.project_end_time_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.add_project_layout.addWidget(self.project_end_time_title, 0, 2, 1, 2)

        self.project_end_time_date = QtWidgets.QDateEdit()
        self.project_end_time_date.setFont(FONTS["content"])
        self.project_end_time_date.setDate(QtCore.QDate.currentDate())
        self.project_end_time_date.setDisplayFormat("yyyy/MM/dd")
        self.project_end_time_date.setStyleSheet(f'''color: {COLORS['common_black']};''')
        self.add_project_layout.addWidget(self.project_end_time_date, 1, 2, 1, 1)

        self.project_end_time_time = QtWidgets.QTimeEdit()
        self.project_end_time_time.setFont(FONTS["content"])
        self.project_end_time_time.setTime(QtCore.QTime(23, 59))
        self.project_end_time_time.setDisplayFormat("hh:mm")
        self.project_end_time_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
        self.add_project_layout.addWidget(self.project_end_time_time, 1, 3, 1, 1)

        self.project_remark_line = QtWidgets.QLabel(text = "備註")
        self.project_remark_line.setFont(FONTS["h2"])
        self.project_remark_line.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.add_project_layout.addWidget(self.project_remark_line, 2, 0, 1, 4)

        self.project_remark_input = QtWidgets.QTextEdit()
        self.project_remark_input.setFont(FONTS["content"])
        self.project_remark_input.setStyleSheet(f'''background: {COLORS["white"]};
                                                color: {COLORS['common_black']};
                                                border-radius: 5px;''')
        self.add_project_layout.addWidget(self.project_remark_input, 3, 0, 1, 4)

        self.check_project_button = QtWidgets.QPushButton(self, text = "確認")
        self.check_project_button.clicked.connect(lambda: self.check(type = "project"))
        self.check_project_button.setFont(FONTS["h2"])
        self.check_project_button.setStyleSheet(f'''QPushButton{{
                                                color: {COLORS['white']};
                                                background: {COLORS["secondary_button"]};
                                                border-radius: 5px;
                                                padding: 5 10 5 10}}
                                                QPushButton:hover{{
                                                background: {COLORS['secondary_button:hover']}
                                                }}''')
        self.check_project_button.adjustSize()
        self.check_project_button.move(int(0.9*self._width), int(0.5*self._height - 0.5*self.check_project_button.height()))

        self.cancel_project_button = QtWidgets.QPushButton(self, text = "取消")
        self.cancel_project_button.clicked.connect(self.initialize)
        self.cancel_project_button.setFont(FONTS["h2"])
        self.cancel_project_button.setStyleSheet(f'''QPushButton{{
                                                 color: {COLORS['white']};
                                                 background: {COLORS['cancel_button']};
                                                 border-radius: 5px;
                                                 padding: 5 10 5 10}}
                                                 QPushButton:hover{{
                                                 background: {COLORS['cancel_button:hover']}
                                                 }}''')
        self.cancel_project_button.adjustSize()
        self.cancel_project_button.move(int(0.1*self._width), int(0.5*self._height - 0.5*self.cancel_task_button.height()))
        # endregion

        self.hide()
    
    def initialize(self) :
        self.hide()
        self.add_project_title.hide()
        self.add_project_frame.hide()
        self.add_task_title.hide()
        self.check_task_button.hide()
        self.add_task_frame.hide()
        self.cancel_task_button.hide()
        self.check_project_button.hide()
        self.cancel_project_button.hide()
        self.task_name_input.setText("")
        self.task_end_time_check.setChecked(True)
        self.task_end_time_date.setDate(QtCore.QDate.currentDate())
        self.task_end_time_time.setTime(QtCore.QTime(23, 59))
        self.task_expect_time_check1.setChecked(True)
        self.task_expect_time_date1.setDate(QtCore.QDate.currentDate())
        self.task_expect_time_time1.setTime(QtCore.QTime(23, 59))
        self.task_expect_time_check2.setChecked(False)
        self.task_expect_time_date2.setDate(QtCore.QDate.currentDate())
        self.task_expect_time_time2.setTime(QtCore.QTime(23, 59))
        self.task_expect_point_input.setText("")
        self.task_remark_input.setText("")
        self.project_name_input.setText("")
        self.project_end_time_date.setDate(QtCore.QDate.currentDate())
        self.project_end_time_time.setTime(QtCore.QTime(23, 59))
        self.project_remark_input.setText("")

    def add_task(self) :
        self.initialize()
        self.add_task_frame.show()
        self.add_task_title.show()
        self.check_task_button.show()
        self.cancel_task_button.show()
        self.show()
        self.raise_()

    def add_project(self) :
        self.initialize()
        self.show()
        self.add_project_title.show()
        self.add_project_frame.show()
        self.check_project_button.show()
        self.cancel_project_button.show()
        self.raise_()

    def handle_check(self, state, dateedit: QtWidgets.QDateEdit, timeedit: QtWidgets.QTimeEdit) :
        if not(state == 2) :
            dateedit.setDate(QtCore.QDate())
            dateedit.setEnabled(False)
            timeedit.setTime(QtCore.QTime())
            timeedit.setEnabled(False)
        else :
            dateedit.setDate(QtCore.QDate.currentDate())
            dateedit.setEnabled(True)
            timeedit.setTime(QtCore.QTime(23, 59))
            timeedit.setEnabled(True)

    def handle_other(self) :
        if self.task_type_input.currentText() == "" :
            self.task_type_other_input.setText("")
            self.task_type_other_input.setVisible(True)
        else :
            self.task_type_other_input.setText("")
            self.task_type_other_input.setVisible(False)

    def check(self, type: str) :
        if type == "task" :
            # regoin:取得資料
            name = self.task_name_input.text()
            belong_project = self.task_belong_project_input.currentText()
            limit_time = None
            if self.task_end_time_check.isChecked() :
                limit_time = f"{self.task_end_time_date.text()} {self.task_end_time_time.text()}"
            expect_time1 = None
            if self.task_expect_time_check1.isChecked() :
                expect_time1 = f"{self.task_expect_time_date1.text()} {self.task_expect_time_time1.text()}"
            expect_time2 = None
            if self.task_expect_time_check2.isChecked() :
                expect_time2 = f"{self.task_expect_time_date2.text()} {self.task_expect_time_date2.text()}"
            expect_point = self.task_expect_point_input.text()
            if self.task_type_input.currentText() != "" :
                task_type = self.task_type_input.currentText()
            else :
                task_type = self.task_type_other_input.text()
            task_remark = self.task_remark_input.toPlainText()
            status = backend.change_task(name, belong_project, limit_time, expect_time1, expect_time2, expect_point, task_type, task_remark, mode = "add")
            # endregion
            # 刪除輸入框內容
            if status == 200 :
                self.initialize()
                self.parent.update()
        elif type == "project" :
            name = self.project_name_input.text()
            limit_time = f"{self.project_end_time_date.text()} {self.project_end_time_time.text()}"
            remark = self.project_remark_input.toPlainText()
            status = backend.change_project(name, limit_time, remark, mode = "add")
            if status == 200 :
                self.task_belong_project_input.addItem(name)
                self.initialize()
                self.parent.update()
    
    def warning(self) :
        print("warning")

class CircularLoadingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 設定基本屬性
        self.setFixedSize(200, 200)
        self.angle = 0
        
        # 建立計時器
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(30)  # 每30ms更新一次

        self.show()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # 建立漸層顏色
        gradient = QtGui.QLinearGradient(0, 0, 200, 200)
        gradient.setColorAt(0, QtGui.QColor(50, 150, 255))
        gradient.setColorAt(1, QtGui.QColor(100, 200, 255))
        
        # 設定畫筆
        pen = QtGui.QPen(gradient, 15)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
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

def wait() :
    circularLoadingWidget = CircularLoadingWidget()
    circularLoadingWidget.show()

if __name__ == "__main__" :
    basic = Basic()
    basic.show()
    # basic.showMaximized()
    sys.exit(app.exec())