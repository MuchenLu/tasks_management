# app/utils/helper.py

from typing import Literal
from app.services import database
import datetime

class PageManager :
    _instance = None
    def __new__(cls):
        if not cls._instance :
            cls._instance = super().__new__(cls)
            cls._page = ""
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "page") :
            self.page = "Home"
    
    def update(self, new_page: str) :
        self.page = new_page

    def get(self) :
        return self.page

class DataManager :
    _instance = None
    def __new__(cls) :
        if not cls._instance :
            cls._instance = super().__new__(cls)
            cls.data = {}
            cls.tasks = {}
            cls.quotes = {}
        return cls._instance
    
    def __init__(self):
        if not self.data :
            self.data = database.get_data()
            self.tasks = self.data["Tasks"]
            self.quotes = self.data["Quotes"]
            self.tasktype = self.data["TaskType"]
    
    def update(self, new_data: dict, part = Literal["data", "tasks", "quotes", "tasktype"]) :
        if part == "data" :
            self.data = new_data
            self.tasks = self.data["Tasks"]
            self.quotes = self.data["Quotes"]
            self.tasktype = self.data["TaskType"]
        elif part == "tasks" :
            self.tasks = new_data
            self.data["Tasks"] = self.tasks
        elif part == "Quotes" :
            temp_quotes = list(self.quotes.values())
            temp_quotes.append(new_data)
            self.quotes = dict(enumerate(temp_quotes))
            self.data["Quotes"] = self.quotes
        elif part == "TaskType" :
            temp_quotes = list(self.quotes.values())
            temp_quotes.append(new_data)
            self.quotes = dict(enumerate(temp_quotes))
            self.data["Quotes"] = self.quotes

    def get(self, part = Literal["data", "tasks", "quotes", "tasktype"]) :
        if part == "data" :
            return self.data
        elif part == "tasks" :
            return self.tasks
        elif part == "quotes" :
            return self.quotes
        elif part == "tasktype" :
            return self.tasktype

def check_task_format(name: str, task_type: str, expect_point: str = None, end_time: str = None, expect_time1: str = None, expect_time2: str = None, remark: str = None) :
    # region: check type
    message = ""
    n = 1
    if len(name) == 0 :
        message += f"{n}. 任務名稱不可為空\n"
        n += 1
    elif len(name) > 15 :
        message += f"{n}. 任務名稱過長，請小於15個字元\n"
        n += 1
    if end_time :
        if datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M") < datetime.datetime.now() :
            message += f"{n}. 任務截止時間不可早於現在時間\n"
            n += 1
    if expect_time1 :
        if datetime.datetime.strptime(expect_time1, "%Y/%m/%d %H:%M") < datetime.datetime.now() :
            message += f"{n}. 任務預期完成時間不可早於現在時間\n"
            n += 1
        if datetime.datetime.strptime(expect_time1, "%Y/%m/%d %H:%M") > datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M") :
            message += f"{n}. 任務預計完成時間必須早於任務截止時間\n"
            n += 1
    if not expect_time1 and expect_time2 :
        message += f"{n}. 任務預期完成時間開始與截止時間需同時勾選\n"
        n += 1
    elif expect_time2 :
        if datetime.datetime.strptime(expect_time2, "%Y/%m/%d %H:%M") < datetime.datetime.strptime(expect_time1, "%Y/%m/%d %H:%M") :
            message += f"{n}. 任務預計完成結束時間不可早於任務預計完成開始時間\n"
            n += 1
    if task_type == "" :
        message += f"{n}. 任務類型不可為空\n"
        n += 1
    
    if message != "" :
        raise Exception(message)