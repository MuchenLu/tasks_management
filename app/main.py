# app/main.py

from PyQt6 import QtWidgets, QtCore, QtWebEngineWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

from .services import database, calendar_api
from .ui.main_window import Basic
from .ui.components.loading import CircularLoadingWidget
from .utils.helper import PageManager
from .utils.log import write

class Signals(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int, str)

class InitThread(QtCore.QThread):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
    
    def run(self):
        global data, tasks, service
        
        try:
            # 報告進度：開始初始化
            self.signals.progress.emit(0, "準備初始化...")
            self.msleep(200)
            
            # 初始化 Google Calendar API
            write("初始化 Google Calendar API...", "info")
            calendar_api.init_google_calendar(self)
            
            # 載入應用程式資料
            self.signals.progress.emit(75, "載入應用程式資料...")
            self.msleep(200)
            
            data = database.get_data()
            self.signals.progress.emit(80, "處理引用資料...")
            self.msleep(200)
            
            quotes = data["Quotes"]
            self.signals.progress.emit(85, "處理任務資料...")
            self.msleep(200)
            
            tasks = database.sort_data(data["Tasks"])
            self.signals.progress.emit(90, "資料載入完成")
            self.msleep(200)
            
            # 不要在這裡創建UI，改為發送信號讓主執行緒創建
            self.signals.progress.emit(95, "準備建構使用者介面...")
            self.msleep(200)
            
            # 完成資料初始化
            self.signals.progress.emit(100, "資料初始化完成")
            self.msleep(300)
            
            # 發送完成信號，但不傳遞window物件
            self.signals.finished.emit(None)
            
        except Exception as e:
            print(f"初始化過程發生錯誤: {e}")
            # 即使出錯也要發送完成信號
            self.signals.finished.emit(None)

def main():
    # 建立信號對象
    signals = Signals()
    
    # 顯示載入動畫
    loading = CircularLoadingWidget()
    loading.show()
    
    # 連接信號
    signals.finished.connect(lambda _: create_main_window(loading))
    signals.progress.connect(loading.update_progress)
    
    # 啟動初始化線程
    init_thread = InitThread(signals)
    init_thread.start()
    
    # 執行應用程式
    return app.exec()

def create_main_window(loading_widget):
    """在主執行緒中創建主視窗"""
    try:
        # 更新進度
        loading_widget.update_progress(95, "建構使用者介面...")
        QtWidgets.QApplication.processEvents()
        
        # 分階段創建UI元件以顯示詳細進度
        loading_widget.update_progress(96, "初始化主視窗...")
        QtWidgets.QApplication.processEvents()
        
        # 創建主視窗
        window = Basic()
        
        loading_widget.update_progress(97, "載入字體資源...")
        QtWidgets.QApplication.processEvents()
        
        loading_widget.update_progress(98, "初始化介面元件...")
        QtWidgets.QApplication.processEvents()
        
        loading_widget.update_progress(99, "完成介面建構...")
        QtWidgets.QApplication.processEvents()
        
        loading_widget.update_progress(100, "啟動完成！")
        QtWidgets.QApplication.processEvents()
        
        # 延遲一下讓用戶看到完成狀態
        QtCore.QTimer.singleShot(500, lambda: finalize_window(window, loading_widget))
        
    except Exception as e:
        print(f"創建主視窗時發生錯誤: {e}")
        loading_widget.update_progress(100, "啟動完成（部分功能可能受限）")
        QtWidgets.QApplication.processEvents()
        
        # 創建基本視窗
        try:
            window = QtWidgets.QMainWindow()
            window.setWindowTitle("任務管理系統")
            window.show()
        except:
            pass
        finally:
            loading_widget.close()

def finalize_window(window, loading_widget):
    """最終化視窗顯示"""
    try:
        # 關閉載入動畫
        loading_widget.close()
        
        # 顯示主視窗元件
        if hasattr(window, 'show_components'):
            window.show_components()
        
        # 顯示主視窗
        window.show()
        window.raise_()
        window.activateWindow()
        
    except Exception as e:
        print(f"最終化視窗時發生錯誤: {e}")
        if hasattr(window, 'show'):
            window.show()

def complete(window, loading_widget):
    """完成初始化後的處理"""
    try:
        # 延遲一下確保載入動畫完成
        QtCore.QTimer.singleShot(200, lambda: finalize_window(window, loading_widget))
    except Exception as e:
        print(f"完成初始化時發生錯誤: {e}")
        loading_widget.close()
        window.show()