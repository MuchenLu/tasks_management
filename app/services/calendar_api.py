# app/services/calendar_api.py

from app.utils.config import CALENDAR_TOKEN, GOOGLE_CALENDAR_SCOPES, GOOGLE_API_KEY, PROJECT_ROOT, CALENDAR_ID
from app.utils.log import write
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

def init_google_calendar(main):
    global service
    """初始化 Google Calendar API"""
    
    try:
        main.signals.progress.emit(10, "檢查憑證...")
        main.msleep(200)
        
        credentials = None
        
        # 檢查是否已有憑證
        if CALENDAR_TOKEN :
            try:
                credentials = Credentials.from_authorized_user_file(CALENDAR_TOKEN, GOOGLE_CALENDAR_SCOPES)
                main.signals.progress.emit(25, "載入憑證成功")
                main.msleep(200)
            except Exception as load_error:
                write(f"載入憑證失敗: {load_error}", "error")
                credentials = None
                main.signals.progress.emit(25, "載入憑證失敗，需要重新授權")
                main.msleep(200)

        # 如果憑證無效，重新授權
        # 如果憑證無效，重新授權
        if not credentials or not credentials.valid:
            main.signals.progress.emit(35, "準備授權...")
            main.msleep(200)

            try:
                # 嘗試刷新 Token
                if credentials and credentials.expired :
                    main.signals.progress.emit(45, "刷新 Token...")
                    main.msleep(200)
                    try :
                        credentials.refresh(Request())
                    except Exception as e :
                        write(f"Google Calendar 憑證刷新錯誤: {e}")
                        # *** 修正：刷新失敗時，將 credentials 設為 None ***
                        credentials = None # <-- 加入這一行
                        # 這樣在內層 try/except 結束後，外層的 if credentials and credentials.expired 就不成立了
                        # 程式就會進入下方的 else 區塊進行完整重新授權
                # else 區塊會處理 credentials 一開始就是 None 或 invalid 的情況，
                # 以及上面 refresh 失敗後被設為 None 的情況
                if not credentials or not credentials.valid: # <-- 可以加一個額外檢查，確保進入完整授權
                    main.signals.progress.emit(50, "請在瀏覽器中完成授權...")
                    main.msleep(500)
                    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_API_KEY, GOOGLE_CALENDAR_SCOPES)
                    credentials = flow.run_local_server(
                        port=0,
                        open_browser=True,
                        prompt='consent',
                    )


                # 儲存新的憑證 (只有在成功取得新 credentials 後才執行)
                if credentials and credentials.valid: # <-- 儲存前檢查 credentials 是否有效
                    main.signals.progress.emit(60, "儲存憑證...")
                    main.msleep(200)

                    LOCAL_CALENDAR_TOKEN = os.path.join(PROJECT_ROOT, os.getenv("CALENDAR_TOKEN", ""))
                    with open(LOCAL_CALENDAR_TOKEN, 'w') as token:
                        token.write(credentials.to_json())
                else:
                    # 如果重新授權失敗，也要記錄並處理
                    write("重新授權失敗，未能取得有效憑證", "error")
                    service = None
                    main.signals.progress.emit(60, "授權失敗")
                    main.msleep(200)
                    return # 重新授權失敗則直接返回

            except Exception as auth_error:
                write(f"授權過程發生未預期錯誤: {auth_error}", "error") # 修改錯誤訊息以區分
                service = None
                main.signals.progress.emit(60, "授權失敗")
                main.msleep(200)
                return

        # 建立 Calendar 服務 (只有在上面的流程成功取得有效 credentials 後才執行)
        if credentials and credentials.valid: # <-- 建立服務前再次檢查 credentials 是否有效
            main.signals.progress.emit(65, "連接 Google 服務...")
            main.msleep(200)
            try:
                # 這裡通常不需要再次 refresh，因為上面的流程已經確保 credentials 是有效或剛取得的
                # 如果您堅持要加，請確保其錯誤處理不會阻止 service 變數被設定
                # credentials.refresh(Request()) # 考慮移除此行或調整其錯誤處理

                service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
                main.signals.progress.emit(70, "Google Calendar 已就緒")
                main.msleep(200)
            except Exception as service_error:
                write(f"建立 Google Calendar 服務錯誤: {service_error}", "error") # 修改錯誤訊息
                service = None
                main.signals.progress.emit(70, "無法連接 Google 服務")
                main.msleep(200)
        else:
            # 如果 credentials 無效（例如上面重新授權失敗），則 service 保持 None
            service = None
            main.signals.progress.emit(70, "Google 服務初始化失敗 (憑證無效)") # 修改訊息
            main.msleep(200)

        # 最外層的 except 捕獲其他未處理的錯誤
    except Exception as e:
        write(f"Google Calendar API 初始化發生未預期錯誤: {e}", "error") # 修改訊息
        service = None
        main.signals.progress.emit(70, "Google 服務初始化失敗")
        main.msleep(200)



def add_event(name, expect_time1: str, expect_time2: str) :
    global service
    if expect_time1.split(" ")[1] == "00:00" and expect_time2.split(" ")[1] == "23:59" :
        event = {"summary": name,
                "start": {"date": expect_time1.split(" ")[0].replace("/", "-"),
                        "timeZone": "Asia/Taipei"},
                "end": {"date": expect_time2.split(" ")[0].replace("/", "-"),
                        "timeZone": "Asia/Taipei"},
                "reminders": {"useDefault": False,
                                "overrides": [{"method": "popup", "minutes": 0}]},
                "colorId": "9"}
    else :
        event = {"summary": name,
                    "start": {"dateTime": expect_time1.replace("/", "-").replace(" ", "T") + ":00+08:00", "timeZone": "Asia/Taipei"},
                    "end": {"dateTime": expect_time2.replace("/", "-").replace(" ", "T") + ":00+08:00", "timeZone": "Asia/Taipei"},
                    "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 0}]},
                "colorId": "9"}
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()