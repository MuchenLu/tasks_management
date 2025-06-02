# app/services/calendar_api.py

from app.utils.config import CALENDAR_TOKEN, SCOPES, CALENDAR_API_KEY
from app.utils.log import write
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def init_google_calendar(main):
    """初始化 Google Calendar API"""
    
    try:
        main.signals.progress.emit(10, "檢查憑證...")
        main.msleep(200)
        
        credentials = None
        
        # 檢查是否已有憑證
        if CALENDAR_TOKEN :
            try:
                credentials = Credentials.from_authorized_user_file(CALENDAR_TOKEN, SCOPES)
                main.signals.progress.emit(25, "載入憑證成功")
                main.msleep(200)
            except Exception as load_error:
                write(f"載入憑證失敗: {load_error}", "error")
                credentials = None
                main.signals.progress.emit(25, "載入憑證失敗，需要重新授權")
                main.msleep(200)

        # 如果憑證無效，重新授權
        if not credentials or not credentials.valid:
            main.signals.progress.emit(35, "準備授權...")
            main.msleep(200)
            
            try:
                # 嘗試刷新 Token
                if credentials and credentials.expired and credentials.refresh_token:
                    main.signals.progress.emit(45, "刷新 Token...")
                    main.msleep(200)
                    credentials.refresh(Request())
                else:
                    # 重新授權流程
                    main.signals.progress.emit(50, "請在瀏覽器中完成授權...")
                    main.msleep(500)  # 授權需要更多時間
                    
                    flow = InstalledAppFlow.from_client_secrets_file(CALENDAR_API_KEY, SCOPES)
                    credentials = flow.run_local_server(
                        port=0, 
                        open_browser=True,
                        prompt='consent',
                    )
                
                # 儲存新的憑證
                main.signals.progress.emit(60, "儲存憑證...")
                main.msleep(200)
                
                with open(CALENDAR_TOKEN, 'w') as token:
                    token.write(credentials.to_json())

            except Exception as auth_error:
                write(f"授權錯誤: {auth_error}", "error")
                service = None
                main.signals.progress.emit(60, "授權失敗")
                main.msleep(200)
                return

        # 建立 Calendar 服務
        if credentials:
            main.signals.progress.emit(65, "連接 Google 服務...")
            main.msleep(200)
            try:
                credentials.refresh(Request())
                service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
                main.signals.progress.emit(70, "Google Calendar 已就緒")
                main.msleep(200)
            except Exception as service_error:
                write(f"建立服務錯誤: {service_error}", "error")
                service = None
                main.signals.progress.emit(70, "無法連接 Google 服務")
                main.msleep(200)
        else:
            service = None
            main.signals.progress.emit(70, "無法連接 Google 服務")
            main.msleep(200)

    except Exception as e:
        write(f"Google Calendar API 初始化發生錯誤: {e}", "error")
        service = None
        main.signals.progress.emit(70, "Google 服務初始化失敗")
        main.msleep(200)