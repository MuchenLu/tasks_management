import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDateTimeEdit, QLabel, QPushButton
from PyQt6.QtCore import QDateTime, QDate, QTime

class DateTimePickerExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('日期時間選擇器範例')
        self.setGeometry(100, 100, 300, 200)

        # 創建中心部件和佈局
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 創建日期時間選擇器
        self.datetime_edit = QDateTimeEdit(self)
        
        # 設置一些常用屬性
        self.datetime_edit.setCalendarPopup(True)  # 啟用彈出日曆
        
        # 設置當前日期時間
        current_datetime = QDateTime.currentDateTime()
        self.datetime_edit.setDateTime(current_datetime)
        
        # 可選：設置日期範圍
        min_date = QDate(2000, 1, 1)
        max_date = QDate(2050, 12, 31)
        self.datetime_edit.setMinimumDate(min_date)
        self.datetime_edit.setMaximumDate(max_date)
        
        # 設置顯示格式
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        # 標籤顯示選擇的日期時間
        self.label = QLabel('選擇的日期時間：', self)

        # 確認按鈕
        self.confirm_btn = QPushButton('確認選擇', self)
        self.confirm_btn.clicked.connect(self.show_selected_datetime)

        # 添加控件到佈局
        layout.addWidget(self.label)
        layout.addWidget(self.datetime_edit)
        layout.addWidget(self.confirm_btn)

    def show_selected_datetime(self):
        # 獲取選擇的日期時間
        selected_datetime = self.datetime_edit.dateTime()
        
        # 格式化顯示
        formatted_datetime = selected_datetime.toString("yyyy-MM-dd HH:mm:ss")
        self.label.setText(f'選擇的日期時間：{formatted_datetime}')

def main():
    app = QApplication(sys.argv)
    window = DateTimePickerExample()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
