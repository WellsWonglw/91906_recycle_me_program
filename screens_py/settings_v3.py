from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class Settings(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)


    def load(self):
        """
        Load the "settings" screen.
        Changes current screen to "settings" screen in ScreenManager.
        """
        self.manager.current = "settings"


    def back(self):
        """
        Return back to the "dashboard" screen.
        Changes current screen to the "dashboard" screen in ScreenManager.
        """
        self.manager.current = "dashboard"


    def load_about_screen(self):
        """
        Load the "about_us" screen.
        changes current screen to the "about_us" screen in ScreenManager.
        """
        self.manager.current = "about_us"