import firebase_admin
from firebase_admin import db
from typing import Literal, Union
import threading
import datetime
import copy

def get_data() -> dict :
    if not firebase_admin._apps :
        cred = firebase_admin.credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://tasks-manager-a8070-default-rtdb.firebaseio.com/"})
    data = db.reference("/").get()
    return data

def change_task(name: str, belong_project: str = None, limit_time: str = None, expect_time1: str = None, expect_time2: str = None, expect_point: str = None, task_type: str = None, task_remark: str = None, mode: Literal["add", "edit", "delete"] = "add") -> int :
    '''
    This function is used to add, edit, or delete task.
    Every param is passing with a **string**.

    :param name: It's task's name. Needed in **every** mode.
    :param belong_project: It's what project is task belonging. Needed in **add** and **edit** mode.
    :param limit_time: It's the task's limit time. Option in **add** and **edit** mode.
    :param expect_time1: It's task's start or end time that you expect to do or finish it. Option in **add** and **edit** mode.
    :param expect_time2: It's task's end time that you expect to finish it. Option in **add** and **edit** mode.
    :param expect_point: It's the point that you expect to spend in this task. Needed in **add** and **edit** mode.
    :param task_type: It's the task's type, like homework. Option in **add** and **edit** mode.
    :param task_remark: It's the task's remark to describe the task more detailed. Option in **add** and **edit** mode.
    :param mode: It's the mode that you want to use in this function. Needed in **every** mode. Option: "add", "edit", "delete"
    '''
    if not firebase_admin._apps :
        cred = firebase_admin.credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://tasks-manager-a8070-default-rtdb.firebaseio.com/"})
    ref = db.reference(f"/Tasks/{belong_project}")
    if mode == "add" :
        content = {name: {"expect_point": expect_point,
                          "status": "未開始",
                        "done": "False"}}
        if limit_time != None :
            content[name]["limit_time"] = limit_time
        if expect_time1 != None :
            content[name]["expect_time1"] = expect_time1
        if expect_time2 != None :
            content[name]["expect_time2"] = expect_time2
        if task_type != None :
            content[name]["task_type"] = task_type
        if task_remark != None :
            content[name]["task_remark"] = task_remark
        try :
            ref.update(content)
            return 200
        except :
            raise RuntimeError("Adding task error.")

def change_project(name: str, limit_time: str, project_remark: str, mode: Literal["add", "edit", "delete"] = "add") -> int :
    if not firebase_admin._apps :
        cred = firebase_admin.credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://tasks-manager-a8070-default-rtdb.firebaseio.com/"})
    if mode == "add" or mode == "edit" :
        ref = db.reference("/Tasks")
        try :
            ref.update({name: {"setting": {"limit_time": limit_time, "project_remark": project_remark}}})
            return 200
        except :
            raise RuntimeError("Add Project failed.")
            
def update_data(data: dict) -> int :
    if not firebase_admin._apps :
        cred = firebase_admin.credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://tasks-manager-a8070-default-rtdb.firebaseio.com/"})
    ref = db.reference("/")
    try :
        ref.set(data)
    except :
        raise RuntimeError("Updata failed")
    
def sort_data(old_data: dict) -> dict :
    tasks = copy.deepcopy(old_data)
    done_task = []
    no_done_task = []
    for project in list(tasks.keys()) :
        for task in list(tasks[project].keys()) :
            if task == "setting" :
                continue
            if tasks[project][task]["status"] == "已完成" :
                done_task.append((project, task))
            else :
                expect_diff = float("inf")
                limit_diff = float("inf")

                if tasks[project][task].get("expect_time1") :
                    if datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                        expect_diff = 1000 + (datetime.datetime.now().date() - datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date()).days
                    else :
                        expect_diff = (datetime.datetime.strptime(tasks[project][task]["expect_time1"], "%Y/%m/%d %H:%M").date() - datetime.datetime.now().date()).days

                if tasks[project][task].get("limit_time") :
                    if datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() < datetime.datetime.now().date() :
                        limit_diff = 1000 + (datetime.datetime.now().date() - datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date()).days
                    else :
                        limit_diff = (datetime.datetime.strptime(tasks[project][task]["limit_time"], "%Y/%m/%d %H:%M").date() - datetime.datetime.now().date()).days
                
                no_done_task.append((project, task, expect_diff, limit_diff))

    done_task.sort(key = lambda x: (x[1].lower()))
    no_done_task.sort(key = lambda x: (x[2], x[3], x[1].lower()))

    new_data = {}

    for project in tasks:
        new_data[project] = {}
        if "setting" in tasks[project]:
            new_data[project]["setting"] = copy.deepcopy(tasks[project]["setting"])

    for task in no_done_task :
        new_data[task[0]][task[1]] = old_data[task[0]][task[1]]

    for task in done_task :
        new_data[task[0]][task[1]] = old_data[task[0]][task[1]]
    
    return new_data