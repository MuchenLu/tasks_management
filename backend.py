import firebase_admin
from firebase_admin import db
import threading

def get_data() -> dict :
    cred = firebase_admin.credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://tasks-manager-a8070-default-rtdb.firebaseio.com/"})
    data = db.reference("/").get()
    return data