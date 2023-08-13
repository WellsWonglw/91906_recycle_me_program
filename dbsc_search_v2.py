from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from functools import partial
from sqlite import SQLite
from db import DB

db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)

# Define the Search screen class


class Search(Screen):

    # Function to handle when an item in the search results is pressed
    def pressed(self, value, key):
        self.ids.container.clear_widgets()
        self.ids.search_field.text = value.text

    # Function that going back to the dashboard screen
    def on_back(self):
        self.ids.search_field.text = ""
        self.ids.container.clear_widgets()
        self.manager.current = "dashboard"

    # Function that set the search result
    def set_search_result(self, text=" "):
        self.ids.container.clear_widgets()
        for key, value in db.searchables().items():
            if value.startswith(text.casefold()):
                self.ids.container.add_widget(
                    OneLineListItem(text=value, on_press=partial(
                        self.pressed, key=key))
                )
