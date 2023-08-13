from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from functools import partial
from sqlite import SQLite
from db import DB

db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)

# Search class represents the screen for searching items.
class Search(Screen):

    # Function to handle when an item in the search results is pressed
    def pressed(self, value, key):
        """
        Function to handle when an item in the search results is pressed.

        Args:
            value (str): The text value of the selected item.
            key (str): The key corresponding to the selected item.
        """
        self.ids.container.clear_widgets()
        self.ids.search_field.text = value.text

    # Function that going back to the dashboard screen
    def on_back(self):
        """
        Function to navigate back to the dashboard screen.
        Clears the search field and container widgets, 
        then switches to the dashboard screen.
        """
        self.ids.search_field.text = ""
        self.ids.container.clear_widgets()
        self.manager.current = "dashboard"

    # Function that set the search result
    def set_search_result(self, text=" "):
        """
        Set the search results based on the provided text.

        Args:
            text : the text to search for (default is an empty string).
        """
        self.ids.container.clear_widgets()
        for key, value in db.searchables().items():
            if value.startswith(text.casefold()):
                self.ids.container.add_widget(
                    OneLineListItem(text=value, on_press=partial(
                        self.pressed, key=key))
                )
