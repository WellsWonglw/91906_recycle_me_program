from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from sqlite import SQLite
from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


class Signup(Screen):
    """
    Signup screen where users can register by providing
    their username and password.

    Attributes:
        No attributes are defined in this class.

    Methods:
        load: Function that loads the signup screen.
        on_signup: handles signup process when the "Signup" button is pressed.
    """

    def __init__(self, **kwargs):
        super(Signup, self).__init__()

    def load(self):
        """
        Load the signup screen.
        Switching current screen to the signup screen.

        Parameters:
            No parameters are required.

        Returns:
            None.
        """
        self.manager.current = "signup"

    def on_signup(self, username, password, re_password):
        """
        Handles user registration process when "Signup" button is pressed.
        Validates the user input, checks if the provided username is available,
        and inserts user information into the database if is valid.

        Parameters:
            username (TextInput): user's desired username.
            password (TextInput): user's desired password.
            re_password (TextInput): user's re-entered password.

        Returns:
            None.
        """
        if username.text == "":
            username.error = True
            return
        
        if len(username.text) > 8 or len(username.text) < 3:
            username.helper_text = f"'{username.text}' must be between 3 and 8 characters!"
            username.error = True
            return
        
        if db.username_exists(username.text):
            username.helper_text = f"'{username.text}' already exists!"
            username.error = True
            return
        
        if len(password.text) != 8:
            password.helper_text = "Password must be have 8 characters!"
            password.error = True
            return
        
        if password.text == "":
            password.error = True
            return

        if password.text != re_password.text:
            re_password.error = True
            return

        user = {"username": username.text, "password": password.text}

        # Inserts the user information into the "user" table in the database
        if db.insert("user", user):
            username.text = ""
            password.text = ""
            re_password.text = ""
            MDApp.get_running_app().load_login_screen()
