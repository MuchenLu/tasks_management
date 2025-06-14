# app/ui/components/side_menu.py

from PyQt6 import QtWidgets, QtCore, QtGui
from app.utils.config import DELETE_PNG
from app.utils.helper import PageManager, DataManager
from app.ui.styles import FONTS, COLORS

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
        
        self.page_manager = PageManager()
        self.data_manager = DataManager()
        self.tasks = self.data_manager.get("tasks")

        self.frame = QtWidgets.QFrame()
        self.frame.setStyleSheet(f'''background: {COLORS['side_color']};''')
        # 修改：添加主布局管理器
        self.main_layout = QtWidgets.QGridLayout(self.frame)
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
        self.tasks = self.data_manager.get("tasks")
        # region: menu
        self.graph = QtWidgets.QLabel(self, text = "儀表板")
        self.graph.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.graph.setFont(FONTS["menu"])
        self.graph.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.graph)
        self.main_layout.addWidget(self.graph, 0, 0, 1, 2)

        self.calendar = QtWidgets.QLabel(self, text = "日曆")
        self.calendar.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.calendar.setFont(FONTS['menu'])
        self.calendar.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.calendar)
        self.main_layout.addWidget(self.calendar, 1, 0, 1, 2)

        self.all = QtWidgets.QLabel(self, text = "全部任務")
        self.all.setStyleSheet(f"color: {COLORS['primary_black']}")
        self.all.setFont(FONTS["menu"])
        self.all.mousePressEvent = lambda event: self.handle_mouseEvent(event, self.all)
        self.main_layout.addWidget(self.all, 2, 0, 1, 2)

        self.row = 3
        for project in list(self.tasks.keys()) :
            menu = QtWidgets.QLabel(self, text = project.replace('"', ""))
            menu.setStyleSheet(f"color: {COLORS['primary_black']}")
            menu.setFont(FONTS["menu"])
            menu.mousePressEvent = lambda event, m = menu: self.handle_mouseEvent(event, m)
            self.main_layout.addWidget(menu, self.row, 0, 1, 1)

            delete_label = QtWidgets.QLabel()
            delete_label.setFixedSize(int(self._width * 0.1), int(self._width * 0.1))
            delete_img = QtGui.QPixmap(DELETE_PNG)
            delete_img = delete_img.scaled(int(self._width * 0.1), int(self._width * 0.1), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            delete_label.setPixmap(delete_img)
            delete_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            delete_label.mousePressEvent = lambda event, p = project: self.parent.main.delete(type = "project", project = p)
            self.main_layout.addWidget(delete_label, self.row, 1, 1, 1, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
            self.row += 1

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
        self.main_layout.addWidget(self.add_project, self.row, 0, 1, 2)

    def switch_page(self, event, label: QtWidgets.QLabel) :
        self.page = label.text()
        self.page_manager.update(self.page)
        label.setFont(FONTS["highlight"])

        self.page_manager.update(self.page)

        if self.page == "日曆" :
            self.parent.main.calendar()
        elif self.page == "儀表板" :
            self.parent.main.graph()
        else :
            pass
            self.parent.main.task()
    
    def handle_mouseEvent(self, event, label) :
        self.initialize(event)
        self.switch_page(event, label)
    
    def func_add_project(self) :
        self.parent.add.add_project()