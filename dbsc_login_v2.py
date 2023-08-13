from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite

from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__()

    # Function that check if there is an active session
    def load(self):
        if db.has_session:
            MDApp.get_running_app().load_dashboard_screen()
            # pass
        else:
            self.manager.current = "login"

    # Function that check the username and the password
    def on_login(self, username, password):
        if username.text == "":
            username.error = True
            return
        if password.text == "":
            password.error = True
            return
        # Check if the username exists in the database
        if not db.username_exists(username.text):
            username.helper_text = f"'{username.text}' not found!"
            username.error = True
            return
        # Retrieve the user data from the database
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

    # Function that switch to the signup screen
    def on_signup(self):
        self.manager.current = "signup"
