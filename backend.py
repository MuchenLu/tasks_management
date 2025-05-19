import firebase_admin
from firebase_admin import db
from typing import Literal, Union
import threading

def get_data() -> dict :
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
            ref.set(content)
            return 200
        except :
            raise RuntimeError("Adding task error.")