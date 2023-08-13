from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class AboutUs(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load(self):
        self.manager.current = "about_us"

    def back(self):
        self.manager.current = "dashboard"