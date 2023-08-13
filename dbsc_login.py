from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite

from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


class Login(Screen):
    """
    Handling user login and session management.
    """

    def __init__(self, **kwargs):
        """
        Initializes the Login Screen.

        Args:
            **kwargs: Keyword arguments to be passed to the parent class.
        """
        super(Login, self).__init__()

    def load(self):
        """
        Checks if active session and navigates to appropriate screen.

        Returns:
            None
        """
        if db.has_session:
            MDApp.get_running_app().load_dashboard_screen()
            return
            # pass
        else:
            self.manager.current = "login"

        # self.manager.current = "login"
        # MDApp.get_running_app().load_dashboard_screen()

    def on_login(self, username, password):
        """
        Validates entered username and password for user login.

        Args:
            username (TextInput): containing the entered username.
            password (TextInput): containing the entered password.

        Returns:
            None
        """
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

    def on_signup(self):
        """
        Switches to the signup screen.

        Note:
            Called when user clicks on the signup button.

        Returns:
            None
        """
        self.manager.current = "signup"
