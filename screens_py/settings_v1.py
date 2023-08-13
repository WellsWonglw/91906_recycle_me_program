from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import MDList
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
from sqlite import SQLite
import time
from logger import logger
from datetime import datetime, timedelta
from kivymd.uix.button import MDRectangleFlatButton
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKPieChart

class Settings(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load(self):
        self.manager.current = "settings"

    def back(self):
        self.manager.current = "dashboard"
    
    def load_about_screen(self):
        self.manager.current = "about_us"