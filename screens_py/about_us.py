from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class AboutUs(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)


    def load(self):
        """
        Load "about_us" screen.
        Responsible for changing current screen to the "about_us" screen.
        """
        self.manager.current = "about_us"


    def back(self):
        """
        Return back to the "dashboard" screen.
        Responsible for changing current screen to the "dashboard" screen.
        """
        self.manager.current = "dashboard"