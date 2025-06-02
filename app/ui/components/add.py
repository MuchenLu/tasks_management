# app/ui/components/add.py

from PyQt6 import QtWidgets, QtCore, QtGui
from app.services import database
from app.ui.styles import COLORS, FONTS
from app.utils.helper import DataManager

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

        self.data_manager = DataManager()
        self.tasks = self.data_manager.get("tasks")

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
        self.task_belong_project_input.addItems(list(self.tasks.keys()))
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
        global service
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
                expect_time2 = f"{self.task_expect_time_date2.text()} {self.task_expect_time_time2.text()}"
            expect_point = self.task_expect_point_input.text()
            if self.task_type_input.currentText() != "" :
                task_type = self.task_type_input.currentText()
            else :
                task_type = self.task_type_other_input.text()
            task_remark = self.task_remark_input.toPlainText()
            status = database.change_task(name, belong_project, limit_time, expect_time1, expect_time2, expect_point, task_type, task_remark, mode = "add")
            if expect_time1 :
                event = {"summary": name}
                if expect_time1.split(" ")[-1] == "00:00" and expect_time2.split(" ")[-1] == "23:59" :
                    if expect_time2 :
                        event["start"] = {"date": expect_time1.split(" ")[0].replace("/", "-"), "timeZone": "Asia/Taipei"}
                        event["end"] = {"date": expect_time2.split(" ")[0].replace("/", "-"), "timeZone": "Asia/Taipei"}
                        event["reminders"] = {"useDefault": False, "overrides": [{"method": "popup", "minutes": 0}]}
                else :
                    if expect_time2 :
                        event["start"] = {"dateTime": expect_time1.replace("/", "-").replace(" ", "T") + ":00+08:00", "timeZone": "Asia/Taipei"}
                        event["end"] = {"dateTime": expect_time2.replace("/", "-").replace(" ", "T") + ":00+08:00", "timeZone": "Asia/Taipei"}
                        event["reminders"] = {"useDefault": False, "overrides": [{"method": "popup", "minutes": 0}]}
                service.events().insert(calendarId='fee7be29e65c66988de345605e0fb06c5fe84da49c99c1e07062cfb10825bc6f@group.calendar.google.com', body=event).execute()
            # endregion
            # 刪除輸入框內容
            if status == 200 :
                self.initialize()
                self.parent.update()
        elif type == "project" :
            name = self.project_name_input.text()
            limit_time = f"{self.project_end_time_date.text()} {self.project_end_time_time.text()}"
            remark = self.project_remark_input.toPlainText()
            status = database.change_project(name, limit_time, remark, mode = "add")
            if status == 200 :
                self.task_belong_project_input.addItem(name)
                self.initialize()
                self.parent.update()
    
    def warning(self) :
        print("warning")
