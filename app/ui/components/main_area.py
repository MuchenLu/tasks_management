# app/ui/components/main_area.py

import random
import datetime
import os
import time
from PyQt6 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets, QtWebEngineCore
from app.services import database, scraper
from app.utils.config import EDIT_PNG, DELETE_PNG, CALENDAR_PROFILE_DIR, PROJECT_ROOT
from app.ui.styles import FONTS, COLORS
from app.utils.helper import DataManager, PageManager

class Main(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
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

        self.page_manager = PageManager()
        self.data_manager = DataManager()

        self.quotes = self.data_manager.get("quotes")
        self.tasks = self.data_manager.get("tasks")

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

        self.greet_subtitle = QtWidgets.QLabel(self.greet_frame, text=self.quotes[random.randint(1, 10)])
        self.greet_subtitle.setStyleSheet(f"color: {COLORS['secondary_black']}")
        self.greet_subtitle.setFont(FONTS["h2"])
        self.greet_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.greet_layout.addWidget(self.greet_subtitle)

        self.greet_button = QtWidgets.QPushButton(self.greet_frame, text="新建任務")
        # self.greet_button.clicked.connect(self.parent.add.add_task)
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

        # region: auto add task
        self.auto_add_frame = QtWidgets.QFrame()  # 修改：移除父元素參數
        self.auto_add_frame.setObjectName("auto_add_frame")
        self.auto_add_frame.setStyleSheet(f'''#auto_add_frame {{
                                       border: none;
                                       border-bottom: 2px solid {COLORS['line_color']}
        }}''')
        self.auto_add_layout = QtWidgets.QVBoxLayout(self.auto_add_frame)
        self.auto_add_layout.setContentsMargins(0, 20, 0, 20)

        self.auto_add_title = QtWidgets.QLabel(self.auto_add_frame, text="自動添加任務")
        self.auto_add_title.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.auto_add_title.setFont(FONTS["h1"])
        self.auto_add_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.auto_add_layout.addWidget(self.auto_add_title)

        self.auto_add_subtitle = QtWidgets.QLabel(self.auto_add_frame, text="自動從ONO和Google Classroom中擷取代辦清單")
        self.auto_add_subtitle.setFont(FONTS["h2"])
        self.auto_add_subtitle.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
        self.auto_add_subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.auto_add_layout.addWidget(self.auto_add_subtitle)

        self.auto_add_button = QtWidgets.QPushButton(self.auto_add_frame, text="自動添加")
        self.auto_add_button.setStyleSheet(f'''QPushButton{{
                                        background: {COLORS['primary_button']};
                                        color: {COLORS["white"]};
                                        padding: 10 50 10 50;
                                        border-radius: 5;}}
                                        QPushButton:hover{{
                                        background: {COLORS['primary_button:hover']}
                                        }}''')
        self.auto_add_button.setFont(FONTS["content"])
        self.auto_add_button.clicked.connect(lambda: self.auto_add_task())
        self.auto_add_layout.addWidget(self.auto_add_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # 修改：設置最小高度而非使用setGeometry
        self.auto_add_frame.setMinimumHeight(int(self._height * 0.3))
        # 修改：將框架添加到主布局
        self.main_layout.addWidget(self.auto_add_frame)
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

        for project in list(self.tasks.keys()):
            for task in list(self.tasks[project].keys()) :
                if task != None and task != "setting" :
                    try :
                        if datetime.datetime.strptime(self.tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                            show = True
                        elif datetime.datetime.strptime(self.tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                            show = True
                        else :
                            show = False
                    except KeyError :
                        show = False
                    
                    if not show :
                        try :
                            if datetime.datetime.strptime(self.tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
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

                    solve = False
                    try :
                        if datetime.datetime.strptime(self.tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
                            task_status = QtWidgets.QLabel(task_frame, text="今日必須完成")
                            task_status.setStyleSheet(f"color: {COLORS['common_black']}")
                            task_status.setFont(FONTS["remark"])
                            task_layout.addWidget(task_status)
                            solve = True
                        elif datetime.datetime.strptime(self.tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                            task_status = QtWidgets.QLabel(task_frame, text="今日過期任務")
                            task_status.setStyleSheet(f"color: {COLORS['red']}")
                            task_status.setFont(FONTS["remark"])
                            task_layout.addWidget(task_status)
                            solve = True
                    except KeyError :
                        pass
                    
                    if not solve :
                        try :
                            if datetime.datetime.strptime(self.tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() == datetime.datetime.now().date() :
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
        if CALENDAR_PROFILE_DIR :
            self.profile = QtWebEngineCore.QWebEngineProfile("PersistentCalendarProfile", self)
            self.profile.setPersistentStoragePath(CALENDAR_PROFILE_DIR)
            self.profile.setPersistentCookiesPolicy(QtWebEngineCore.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
            self.profile.setCachePath(CALENDAR_PROFILE_DIR) # 通常快取也放一起
            self.profile.setHttpCacheType(QtWebEngineCore.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        else :
            self.profile = QtWebEngineCore.QWebEngineProfile("PersistentCalendarProfile", self)
            self.profile.setPersistentStoragePath(os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_PROFILE_DIR", "")))
            self.profile.setPersistentCookiesPolicy(
                QtWebEngineCore.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
            )
            self.profile.setCachePath(os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_PROFILE_DIR", "")))
            self.profile.setHttpCacheType(
                QtWebEngineCore.QWebEngineProfile.HttpCacheType.DiskHttpCache
            )
        self.calendar_page = QtWebEngineWidgets.QWebEngineView()
        self.web_page = QtWebEngineCore.QWebEnginePage(self.profile, self)
        self.calendar_page.setPage(self.web_page)
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
        
        self.page = self.page_manager.get()
        self.project_title = QtWidgets.QLabel(text = self.page)
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
        self.auto_add_frame.hide()
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
        self.auto_add_frame.show()
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
        self.page = self.page_manager.get()
        self.tasks = self.data_manager.get("tasks")
        self.project_title.setText(self.page)
        self.row = 1
        self.column = 0
        if self.page == "全部任務" :
            for project in list(self.tasks.keys()) :
                for task in list(self.tasks[project].keys()) :
                    if task == "setting" :
                        continue
                    task_frame = QtWidgets.QFrame()
                    task_frame.setStyleSheet(f'''background: {COLORS["white"]};
                                             border-radius: 5;''')
                    task_frame.setFixedSize(int(self._width*0.3), int(self._height*0.2))
                    shadow = QtWidgets.QGraphicsDropShadowEffect()
                    shadow.setBlurRadius(4)
                    shadow.setColor(QtGui.QColor(COLORS["shadow"]))
                    shadow.setOffset(2, 2)
                    task_frame.setGraphicsEffect(shadow)
                    task_layout = QtWidgets.QGridLayout(task_frame)

                    task_title = QtWidgets.QLabel(f'{project}: {task}')
                    task_title.setWordWrap(True)
                    task_title.setFont(FONTS["content"])
                    task_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
                    task_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
                    task_layout.addWidget(task_title, 0, 0)

                    edit_label = QtWidgets.QLabel()
                    edit_label.setFixedSize(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1))
                    edit_img = QtGui.QPixmap(EDIT_PNG)
                    edit_img = edit_img.scaled(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                    edit_label.setPixmap(edit_img)
                    edit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                    task_layout.addWidget(edit_label, 0, 1, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
                    
                    delete_label = QtWidgets.QLabel()
                    delete_label.setFixedSize(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1))
                    delete_img = QtGui.QPixmap(DELETE_PNG)
                    delete_img = delete_img.scaled(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                    delete_label.setPixmap(delete_img)
                    delete_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                    delete_label.mousePressEvent = lambda event, n = task, p = project: self.delete(type = "task", task = n, project = p)
                    task_layout.addWidget(delete_label, 0, 2, alignment = QtCore.Qt.AlignmentFlag.AlignRight)

                    if self.tasks[project][task].get("limit_time") :
                        task_limit_time = QtWidgets.QLabel(f'截止時間: {self.tasks[project][task].get("limit_time")}')
                        task_limit_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(self.tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[project][task]["status"] != "已完成" :
                            task_limit_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_limit_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_limit_time, 1, 0, 1, 3)
                    
                    match (self.tasks[project][task].get("expect_time1"), self.tasks[project][task].get("expect_time2")) :
                        case (None, None) :
                            pass
                        case (_, None) :
                            task_expect_time = QtWidgets.QLabel(f'預計完成時間: {self.tasks[project][task].get("expect_time1")}')
                            task_expect_time.setFont(FONTS["remark"])
                            if datetime.datetime.strptime(self.tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[project][task]["status"] != "已完成" :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                            else :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                            task_layout.addWidget(task_expect_time, 2, 0, 1, 3)
                        case (_, _) :
                            task_expect_time = QtWidgets.QLabel(f'預計完成時間: {self.tasks[project][task].get("expect_time1")}~{self.tasks[project][task].get("expect_time2")}')
                            task_expect_time.setFont(FONTS["remark"])
                            if datetime.datetime.strptime(self.tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[project][task]["status"] != "已完成" :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                            else :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                            task_layout.addWidget(task_expect_time, 2, 0, 1, 3)
                        
                    if self.tasks[project][task].get("task_remark") :
                        task_remark = QtWidgets.QLabel(f'{self.tasks[project][task].get("task_remark")}')
                        task_remark.setWordWrap(True)
                        task_remark.setFont(FONTS["remark"])
                        task_remark.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_remark, 1, 0, 1, 3)
                    
                    task_status = QtWidgets.QLabel(text = f"{self.tasks[project][task]['status']}")
                    task_status.setFont(FONTS["remark"])
                    task_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    match self.tasks[project][task].get("status") :
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
                    task_layout.addWidget(task_status, 3, 0, 1, 3)

                    self.task_layout.addWidget(task_frame, self.row, self.column)
                    if self.column == 2 :
                        self.row += 1
                        self.column = 0
                    else :
                        self.column += 1
        elif self.page == "Home" :
            pass
        else :
            for task in list(self.tasks[self.page].keys()) :
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
                task_title.setWordWrap(True)
                task_title.setFont(FONTS["content"])
                task_title.setStyleSheet(f'''color: {COLORS['secondary_black']}''')
                task_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
                task_layout.addWidget(task_title, 0, 0, 1, 1)

                edit_label = QtWidgets.QLabel()
                edit_label.setFixedSize(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1))
                edit_img = QtGui.QPixmap(EDIT_PNG)
                edit_img = edit_img.scaled(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                edit_label.setPixmap(edit_img)
                edit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                task_layout.addWidget(edit_label, 0, 1, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
                
                delete_label = QtWidgets.QLabel()
                delete_label.setFixedSize(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1))
                delete_img = QtGui.QPixmap(DELETE_PNG)
                delete_img = delete_img.scaled(int(task_frame.width() * 0.1), int(task_frame.width() * 0.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                delete_label.setPixmap(delete_img)
                delete_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                delete_label.mousePressEvent = lambda event, n = task, p = self.page: self.delete(type = "task", task = n, project = p)
                task_layout.addWidget(delete_label, 0, 2, alignment = QtCore.Qt.AlignmentFlag.AlignRight)

                if self.tasks[self.page][task].get("limit_time") :
                    task_limit_time = QtWidgets.QLabel(f'截止時間: {self.tasks[self.page][task].get("limit_time")}')
                    task_limit_time.setFont(FONTS["remark"])
                    if datetime.datetime.strptime(self.tasks[self.page][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[self.page][task]["status"] != "已完成" :
                        task_limit_time.setStyleSheet(f'''color: {COLORS['red']}''')
                    else :
                        task_limit_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                    task_layout.addWidget(task_limit_time, 1, 0, 1, 3)
                
                match (self.tasks[self.page][task].get("expect_time1"), self.tasks[self.page][task].get("expect_time2")) :
                    case (None, None) :
                        pass
                    case (_, None) :
                        task_expect_time = QtWidgets.QLabel(f'預計完成時間: {self.tasks[self.page][task].get("expect_time1")}')
                        task_expect_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(self.tasks[self.page][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[self.page][task]["status"] != "已完成" :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_expect_time, 2, 0, 1, 3)
                    case (_, _) :
                        task_expect_time = QtWidgets.QLabel(f'預計完成時間: {self.tasks[self.page][task].get("expect_time1")}~{self.tasks[self.page][task].get("expect_time2")}')
                        task_expect_time.setFont(FONTS["remark"])
                        if datetime.datetime.strptime(self.tasks[self.page][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() and self.tasks[self.page][task]["status"] != "已完成" :
                                task_expect_time.setStyleSheet(f'''color: {COLORS['red']}''')
                        else :
                            task_expect_time.setStyleSheet(f'''color: {COLORS['common_black']}''')
                        task_layout.addWidget(task_expect_time, 2, 0, 1, 3)

                if self.tasks[self.page][task].get("task_remark") :
                    task_remark = QtWidgets.QLabel(f'{self.tasks[self.page][task].get("task_remark")}')
                    task_remark.setWordWrap(True)
                    task_remark.setFont(FONTS["remark"])
                    task_remark.setStyleSheet(f'''color: {COLORS['common_black']}''')
                    task_layout.addWidget(task_remark, 3, 0, 1, 3)

                task_status = QtWidgets.QLabel(text = f"{self.tasks[self.page][task]['status']}")
                task_status.setMaximumHeight(int(0.3*task_frame.height()))
                task_status.setFont(FONTS["remark"])
                task_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                match self.tasks[self.page][task].get("status") :
                    case "未開始" :
                        task_status.setStyleSheet(f'''color: {COLORS['common_black']};
                        background: {COLORS['undo']}''')
                    case "進行中" :
                        task_status.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    case "已完成" :
                        task_status.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['done']}''')
                task_status.mousePressEvent = lambda event, l = task_status, t = task_title.text().split(" ")[-1], p = self.page: self.change_status(event, label = l, task = t, project = p, now_status = f"{l.text()}")
                task_layout.addWidget(task_status, 4, 0, 1, 3)

                self.task_layout.addWidget(task_frame, self.row, self.column)
                if self.column == 2 :
                    self.row += 1
                    self.column = 0
                else :
                    self.column += 1

        self.task_page.show()
    
    def delete(self, type, task = None, project = None) :
        if type == "task" :
            reply = QtWidgets.QMessageBox.question(self.parent, "刪除確認", f"即將刪除 {task} 任務，是否確認？", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes :
                database.change_task(name = task, belong_project = project, mode = "delete")
                self.parent.update()
        if type == "project" :
            reply = QtWidgets.QMessageBox.question(self.parent, "刪除確認", f"即將刪除 {project} 專案，並連同任務一起刪除，是否確認？", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes :
                database.change_project(name = project, mode = "delete")
                self.parent.update()

    def change_status(self, event, label: QtWidgets.QLabel, task: str, project: str, now_status: str) :
        match now_status :
            case "未開始" :
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    label.setText("進行中")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    self.tasks[project][task]["status"] = "進行中"
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    pass
            case "進行中" :
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    label.setText("已完成")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['done']}''')
                    self.tasks[project][task]["status"] = "已完成"
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    label.setText("未開始")
                    label.setStyleSheet(f'''color: {COLORS['common_black']};
                        background: {COLORS['undo']}''')
                    self.tasks[project][task]["status"] = "未開始"
            case "已完成":
                if event.button() == QtCore.Qt.MouseButton.LeftButton :
                    pass
                elif event.button() == QtCore.Qt.MouseButton.RightButton :
                    label.setText("進行中")
                    label.setStyleSheet(f'''color: {COLORS['white']};
                        background: {COLORS['doing']}''')
                    self.tasks[project][task]["status"] = "進行中"

    def auto_add_task(self) :
        tasks_name, tasks_end_time = scraper.get_ono()
        todos = scraper.get_classroom()

        for task in range(len(tasks_name)) :
            self.parent.add.add_task()
            self.parent.add.task_name_input.setText(tasks_name[task])
            self.parent.add.task_end_time_date.setDate(QtCore.QDate.fromString(tasks_end_time[task].split(" ")[0], "yyyy.MM.dd"))
            self.parent.add.task_end_time_time.setTime(QtCore.QTime.fromString(tasks_end_time[task].split(" ")[1], "HH:mm"))
            while not self.parent.add.auto_signal and self.parent :
                QtCore.QCoreApplication.processEvents()
                time.sleep(0.01)
        
        for todo in todos :
            self.parent.add.add_task()
            self.parent.add.task_name_input.setText(todo["title"])
            self.parent.add.task_end_time_date.setDate(QtCore.QDate(todo["dueDate"]["year"], todo["dueDate"]["month"], todo["dueDate"]["day"]))
            self.parent.add.task_end_time_time.setTime(QtCore.QTime(todo["dueTime"]["hours"], todo["dueTime"]["minutes"]))
            while not self.parent.add.auto_signal and self.parent :
                QtCore.QCoreApplication.processEvents()
                time.sleep(0.01)