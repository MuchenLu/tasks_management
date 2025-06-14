# app/ui/components/expect_point.py

from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from app.ui.styles import FONTS, COLORS

class Form(QtWidgets.QWidget) :
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.reload = False
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |  # 無邊框
            QtCore.Qt.WindowType.Window  # 保持是一個窗口
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self._width = int(screen.width() * 0.5)
        self._height = int(screen.height() * 0.8)

        self.setGeometry(int(screen.width() * 0.5 - self._width * 0.5), int(screen.height() * 0.5 - self._height * 0.5), self._width, self._height)

        self.top_frame = QtWidgets.QFrame(self)
        self.top_frame.setStyleSheet(f'''background: {COLORS["top_color"]};
                                     border-top-left-radius: 12px;
                                     border-top-right-radius: 12px;''')
        self.top_frame.setGeometry(0, 0, self._width, int(self._height * 0.1))
        self.top_title = QtWidgets.QLabel(self.top_frame, text = "估點量表")
        self.top_title.setFont(FONTS["h2"])
        self.top_title.setStyleSheet(f'''color: {COLORS["white"]}''')
        self.top_title.resize(self._width, int(self._height * 0.1))
        self.top_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.body_frame = QtWidgets.QFrame(self)
        self.body_frame.setStyleSheet(f'''background: {COLORS["main_color"]};''')
        self.body_frame.setGeometry(0, int(self._height * 0.1), self._width, int(self._height * 0.8))
        self.body_layout = QtWidgets.QGridLayout(self.body_frame)

        # style
        slider = """QSlider::groove:horizontal {
                    border: 1px solid #d2dde8;
                    height: 5px;
                    background: #f1f1f1;
                    border-radius: 3px;
                }

                QSlider::sub-page:horizontal {
                    background: #8095bd;
                    border: 1px solid #8095bd;
                    height: 6px;
                    border-radius: 3px;
                }

                QSlider::add-page:horizontal {
                    background: #d2dde8;
                    border: 1px solid #d2dde8;
                    height: 6px;
                    border-radius: 3px;
                }

                QSlider::handle:horizontal {
                    background: #ffffff;
                    border: 2px solid #8095bd;
                    width: 16px;
                    height: 10px;
                    margin: -6px 0; /* centers the handle */
                    border-radius: 8px;
                }

                QSlider::handle:horizontal:hover {
                    background: #e0e7f0;
                    border: 2px solid #6f84ad;
                }
                """

        # Question
        self.question1_label = QtWidgets.QLabel(text = "這個任務的內容或步驟有多複雜？")
        self.question1_label.setFont(FONTS["content"])
        self.question1_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question1_label, 0, 0)

        self.question1_0 = QtWidgets.QLabel(text = "0")
        self.question1_0.setFont(FONTS["remark"])
        self.question1_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question1_0, 0, 1)

        self.question1_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question1_slider.setMinimum(0)
        self.question1_slider.setMaximum(5)
        self.question1_slider.setSingleStep(1)
        self.question1_slider.setStyleSheet(slider)
        self.question1_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question1_slider, 0, 2)

        self.question1_5 = QtWidgets.QLabel(text = "5")
        self.question1_5.setFont(FONTS["remark"])
        self.question1_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question1_5, 0, 3)

        # 問題2
        self.question2_label = QtWidgets.QLabel(text = "完成這個任務需要多少我目前不具備的知識或技能？")
        self.question2_label.setFont(FONTS["content"])
        self.question2_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question2_label, 1, 0)

        self.question2_0 = QtWidgets.QLabel(text = "0")
        self.question2_0.setFont(FONTS["remark"])
        self.question2_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question2_0, 1, 1)

        self.question2_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question2_slider.setMinimum(0)
        self.question2_slider.setMaximum(5)
        self.question2_slider.setSingleStep(1)
        self.question2_slider.setStyleSheet(slider)
        self.question2_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question2_slider, 1, 2)

        self.question2_5 = QtWidgets.QLabel(text = "5")
        self.question2_5.setFont(FONTS["remark"])
        self.question2_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question2_5, 1, 3)

        # 問題3
        self.question3_label = QtWidgets.QLabel(text = "我對完成這個任務的興趣有多高？")
        self.question3_label.setFont(FONTS["content"])
        self.question3_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question3_label, 2, 0)

        self.question3_0 = QtWidgets.QLabel(text = "0")
        self.question3_0.setFont(FONTS["remark"])
        self.question3_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question3_0, 2, 1)

        self.question3_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question3_slider.setMinimum(0)
        self.question3_slider.setMaximum(5)
        self.question3_slider.setSingleStep(1)
        self.question3_slider.setStyleSheet(slider)
        self.question3_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question3_slider, 2, 2)

        self.question3_5 = QtWidgets.QLabel(text = "5")
        self.question3_5.setFont(FONTS["remark"])
        self.question3_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question3_5, 2, 3)

        # 問題4
        self.question4_label = QtWidgets.QLabel(text = "我預期完成這個任務的困難程度有多高？")
        self.question4_label.setFont(FONTS["content"])
        self.question4_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question4_label, 3, 0)

        self.question4_0 = QtWidgets.QLabel(text = "0")
        self.question4_0.setFont(FONTS["remark"])
        self.question4_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question4_0, 3, 1)

        self.question4_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question4_slider.setMinimum(0)
        self.question4_slider.setMaximum(5)
        self.question4_slider.setSingleStep(1)
        self.question4_slider.setStyleSheet(slider)
        self.question4_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question4_slider, 3, 2)

        self.question4_5 = QtWidgets.QLabel(text = "5")
        self.question4_5.setFont(FONTS["remark"])
        self.question4_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question4_5, 3, 3)

        # 問題5
        self.question5_label = QtWidgets.QLabel(text = "這個任務的結果或過程有多不確定或潛在風險有多高？")
        self.question5_label.setFont(FONTS["content"])
        self.question5_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question5_label, 4, 0)

        self.question5_0 = QtWidgets.QLabel(text = "0")
        self.question5_0.setFont(FONTS["remark"])
        self.question5_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question5_0, 4, 1)

        self.question5_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question5_slider.setMinimum(0)
        self.question5_slider.setMaximum(5)
        self.question5_slider.setSingleStep(1)
        self.question5_slider.setStyleSheet(slider)
        self.question5_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question5_slider, 4, 2)

        self.question5_5 = QtWidgets.QLabel(text = "5")
        self.question5_5.setFont(FONTS["remark"])
        self.question5_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question5_5, 4, 3)

        # 問題6
        self.question6_label = QtWidgets.QLabel(text = "完成這個任務的時程壓力或重要性有多高？")
        self.question6_label.setFont(FONTS["content"])
        self.question6_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question6_label, 5, 0)

        self.question6_0 = QtWidgets.QLabel(text = "0")
        self.question6_0.setFont(FONTS["remark"])
        self.question6_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question6_0, 5, 1)

        self.question6_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question6_slider.setMinimum(0)
        self.question6_slider.setMaximum(5)
        self.question6_slider.setSingleStep(1)
        self.question6_slider.setStyleSheet(slider)
        self.question6_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question6_slider, 5, 2)

        self.question6_5 = QtWidgets.QLabel(text = "5")
        self.question6_5.setFont(FONTS["remark"])
        self.question6_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question6_5, 5, 3)

        # 問題7
        self.question7_label = QtWidgets.QLabel(text = "完成這個任務需要多少與他人協調或依賴外部因素？")
        self.question7_label.setFont(FONTS["content"])
        self.question7_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question7_label, 6, 0)

        self.question7_0 = QtWidgets.QLabel(text = "0")
        self.question7_0.setFont(FONTS["remark"])
        self.question7_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question7_0, 6, 1)

        self.question7_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question7_slider.setMinimum(0)
        self.question7_slider.setMaximum(5)
        self.question7_slider.setSingleStep(1)
        self.question7_slider.setStyleSheet(slider)
        self.question7_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question7_slider, 6, 2)

        self.question7_5 = QtWidgets.QLabel(text = "5")
        self.question7_5.setFont(FONTS["remark"])
        self.question7_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question7_5, 6, 3)

        # 問題8
        self.question8_label = QtWidgets.QLabel(text = "我預期完成這個任務會花費多少時間？")
        self.question8_label.setFont(FONTS["content"])
        self.question8_label.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question8_label, 7, 0)

        self.question8_0 = QtWidgets.QLabel(text = "0")
        self.question8_0.setFont(FONTS["remark"])
        self.question8_0.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question8_0, 7, 1)

        self.question8_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.question8_slider.setMinimum(0)
        self.question8_slider.setMaximum(5)
        self.question8_slider.setSingleStep(1)
        self.question8_slider.setStyleSheet(slider)
        self.question8_slider.setFixedHeight(20)
        self.body_layout.addWidget(self.question8_slider, 7, 2)

        self.question8_5 = QtWidgets.QLabel(text = "5")
        self.question8_5.setFont(FONTS["remark"])
        self.question8_5.setStyleSheet(f'''color: {COLORS["primary_black"]}''')
        self.body_layout.addWidget(self.question8_5, 7, 3)

        self.tail_frame = QtWidgets.QFrame(self)
        self.tail_frame.setStyleSheet(f'''background: {COLORS["main_color"]};
                                      border-bottom-right-radius: 12px;
                                      border-bottom-left-radius: 12px''')
        self.tail_frame.setGeometry(0, int(self._height * 0.9), self._width, int(self._height * 0.1))
        self.tail_layout = QtWidgets.QHBoxLayout(self.tail_frame)

        self.check_button = QtWidgets.QPushButton(self, text = "確認")
        self.check_button.clicked.connect(self.check)
        self.check_button.setFont(FONTS["h2"])
        self.check_button.setStyleSheet(f'''QPushButton{{
                                                color: {COLORS['white']};
                                                background: {COLORS["secondary_button"]};
                                                border-radius: 5px;
                                                padding: 5 10 5 10}}
                                                QPushButton:hover{{
                                                background: {COLORS['secondary_button:hover']}
                                                }}''')
        self.check_button.adjustSize()

        self.cancel_button = QtWidgets.QPushButton(self, text = "取消")
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setFont(FONTS["h2"])
        self.cancel_button.setStyleSheet(f'''QPushButton{{
                                                 color: {COLORS['white']};
                                                 background: {COLORS['cancel_button']};
                                                 border-radius: 5px;
                                                 padding: 5 10 5 10}}
                                                 QPushButton:hover{{
                                                 background: {COLORS['cancel_button:hover']}
                                                 }}''')
        self.cancel_button.adjustSize()
        self.tail_layout.addWidget(self.cancel_button)
        self.tail_layout.addWidget(self.check_button)
    
    def initialize(self) :
        self.question1_slider.setValue(0)
        self.question1_slider.setValue(0)
        self.question2_slider.setValue(0)
        self.question3_slider.setValue(0)
        self.question4_slider.setValue(0)
        self.question5_slider.setValue(0)
        self.question6_slider.setValue(0)
        self.question7_slider.setValue(0)
        self.question8_slider.setValue(0)
    
    def check(self) -> int :
        question1_value = self.question1_slider.value()
        question1_value = self.question1_slider.value()
        question2_value = self.question2_slider.value()
        question3_value = self.question3_slider.value()
        question4_value = self.question4_slider.value()
        question5_value = self.question5_slider.value()
        question6_value = self.question6_slider.value()
        question7_value = self.question7_slider.value()
        question8_value = self.question8_slider.value()
        self.point = min(20, round((question1_value + question2_value + (5 - question3_value) + question4_value + question5_value + question6_value + question7_value + question8_value) / 2) + 1)
        self.reload = True
        self.hide()

    def cancel(self) :
        self.reload = True
        self.hide()