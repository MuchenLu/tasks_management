# app/services/scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import time
import os
from app.utils.config import ONO_URL, ONO_USER_NAME, ONO_USER_PASSWORD, HEADER, GOOGLE_API_KEY, GOOGLE_CLASSROOM_SCOPES, CLASSROOM_TOKEN, PROJECT_ROOT

chrome_options = Options()
user_agent = HEADER
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def get_ono() :
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_options)
    driver.implicitly_wait(5)
    driver.get(ONO_URL)

    # 登入
    driver.find_element(By.XPATH, "/html/body/div/div[1]/div[5]").click()
    driver.find_element(By.XPATH, "//*[@id='standard-basic']").send_keys(ONO_USER_NAME)
    driver.find_element(By.XPATH, "//*[@id='standard-password-input']").send_keys(ONO_USER_PASSWORD)
    driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/form/div/div/div[6]/div[1]/button/span[1]").click()

    time.sleep(10)
    # 取得
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/a"))
    tasks_name_elements = driver.find_elements(By.CSS_SELECTOR, "span[tipsy='todoData.title']")
    tasks_name = [element.text for element in tasks_name_elements]
    tasks_end_time_elements = driver.find_elements(By.CSS_SELECTOR, "span[ng-if='todoData.end_time']")
    tasks_end_time = [element.text.replace("截止日期:", "") for element in tasks_end_time_elements]

    return tasks_name, tasks_end_time

def get_classroom() :
    creds = None
    if CLASSROOM_TOKEN :
        creds = Credentials.from_authorized_user_file(CLASSROOM_TOKEN, GOOGLE_CLASSROOM_SCOPES)
    if creds and creds.expired and creds.refresh_token :
        creds.refresh(Request())
    if not creds or not creds.valid :
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_API_KEY, GOOGLE_CLASSROOM_SCOPES)
        creds = flow.run_local_server(port = 0)

        LOCAL_CLASSROOM_TOKEN = os.path.join(PROJECT_ROOT, os.getenv("CLASSROOM_TOKEN"))
        with open(LOCAL_CLASSROOM_TOKEN, "w") as file :
            file.write(creds.to_json())
    service = build("classroom", "v1", credentials = creds)
    courses = service.courses().list(studentId='me').execute()

    total_todos = []
    for course in courses.get("courses", []) :
        if course["courseState"] == "ACTIVE" :
            try :
                todos = service.courses().courseWork().list(courseId = course["id"], courseWorkStates='PUBLISHED').execute()
                for todo in todos["courseWork"] :
                    if not (datetime.datetime.strptime(f"{todo['dueDate']['year']}/{todo['dueDate']['month']}/{todo['dueDate']['day']}", "%Y/%m/%d") < datetime.datetime.now()) :
                        total_todos.append(todo)
            except Exception as e :
                pass
    
    return total_todos