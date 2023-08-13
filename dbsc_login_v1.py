from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite

from db import DB

db_connector = SQLite("assets/recycle_tracker.db")
db = DB(db_connector)

class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__()

    def load(self):
        if db.has_session:
            MDApp.get_running_app().load_dashboard_screen()
            # pass
        else:
            self.manager.current = "login"

    def on_login(self, username, password):
        if not db.username_exists(username.text):
            username.helper_text = f"'{username.text}' not found!"
            username.error = True
            return
        user = db.get_user(username.text)
        if user:
            if user['password'] != password.text:
                password.helper_text = "Wrong password!"
                password.error = True
                return
            session = {"username": username.text}
            db.insert("session", session)
            username.text = ""
            password.text = ""
            MDApp.get_running_app().load_dashboard_screen()
            
    def on_signup(self):
        self.manager.current = "signup"