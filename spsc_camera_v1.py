from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
import time
from logger import logger

class CameraScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load(self):
        self.manager.current = "camera_screen"
        self.ids.camera.play = True

    def back(self):
        self.ids.camera.play = False
        self.manager.current = "add_recyclable_item"

    def capture(self):
        try:
            camera = self.ids.camera
            timestr = time.strftime("%Y%m%d_%H%M%S")
            photo_path = "assets/IMG_{}.png".format(timestr)
            camera.export_to_png(photo_path)
            MDApp.get_running_app().photo_captured(photo_path)
            self.back()
        except Exception as ex:
            logger.exception(ex)