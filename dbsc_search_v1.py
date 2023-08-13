from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from functools import partial
from sqlite import SQLite
from db import DB

db_connector = SQLite("assets/recycle_tracker.db")
db = DB(db_connector)


class Search(Screen):

    def pressed(self, value, key):
        self.ids.container.clear_widgets()
        self.ids.search_field.text = value.text

    def on_back(self):
        self.ids.search_field.text = ""
        self.ids.container.clear_widgets()
        self.manager.current = "dashboard"


    def set_search_result(self, text=" "): 
        self.ids.container.clear_widgets()
        for key, value in db.searchables().items():
            if value.startswith(text.casefold()):
                self.ids.container.add_widget(
                    OneLineListItem(text=value, on_press=partial(self.pressed, key=key))
                )
