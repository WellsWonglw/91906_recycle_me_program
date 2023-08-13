from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

class Settings(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load(self):
        self.manager.current = "settings"

    def back(self):
        self.manager.current = "dashboard"
    
    def load_about_screen(self):
        self.manager.current = "about_us"