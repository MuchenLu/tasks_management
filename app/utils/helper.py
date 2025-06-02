# app/utils/helper.py

from typing import Literal
from app.services import database

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
    
    def update(self, new_data: dict) :
        self.data = new_data
        self.tasks = self.data["Tasks"]
        self.quotes = self.data["Quotes"]

    def get(self, part = Literal["data", "tasks", "quotes"]) :
        if part == "data" :
            return self.data
        elif part == "tasks" :
            return self.tasks
        elif part == "quotes" :
            return self.quotes