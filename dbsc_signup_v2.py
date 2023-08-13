from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite
from db import DB

db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)


class Signup(Screen):
    def __init__(self, **kwargs):
        super(Signup, self).__init__()

    def load(self):
        self.manager.current = "signup"

    def on_signup(self, username, password, re_password):
        if len(username.text) > 8 or len(username.text) < 3:
            username.helper_text = f"'{username.text}' must be between 3 and 8 characters!"
            username.error = True
            return

        if len(password.text) != 8:
            password.helper_text = "Password must be have 8 characters!"
            password.error = True
            return    

        user = {"username": username.text, "password": password.text}

        # Inserts the user information into the "user" table in the database
        if db.insert("user", user):
            session = {"username": username.text}
            db.insert("session", session)
            username.text = ""
            password.text = ""
            re_password.text = ""
            MDApp.get_running_app().load_login_screen()
