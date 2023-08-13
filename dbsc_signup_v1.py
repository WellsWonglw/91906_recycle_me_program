from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite
from db import DB

db_connector = SQLite("assets/recycle_tracker.db")
db = DB(db_connector)

class Signup(Screen):
    def __init__(self, **kwargs):
        super(Signup, self).__init__()

    def load(self):
        self.manager.current = "signup"
    
    def on_signup(self, username, password, re_password):
        user = {"username": username.text, "password": password.text}
        if db.insert("user", user):
            session = {"username": username.text}
            db.insert("session", session)
            username.text = ""
            password.text = ""
            re_password.text = ""
            MDApp.get_running_app().load_login_screen()
