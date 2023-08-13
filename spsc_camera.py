from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
import time
from logger import logger

class CameraScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)


    def load(self):
        """
        Function to load the CameraScreen and start the camera preview.

        This function sets the current screen to "camera_screen" and 
        starts the camera preview.
        """
        self.manager.current = "camera_screen"
        self.ids.camera.play = True


    def back(self):
        """
        Function to navigate back to the "add_recyclable_item" screen.

        This function stops the camera preview and 
        switches the current screen to "add_recyclable_item".
        """
        self.ids.camera.play = False
        self.manager.current = "add_recyclable_item"


    def capture(self):
        """
        Function to capture a photo using the camera.
        Saves it to the assets directory with a timestamp.

        Raises:
            Exception: If any error occurs during the photo capture process.
        """
        try:
            camera = self.ids.camera
            timestr = time.strftime("%Y%m%d_%H%M%S")
            photo_path = "assets/IMG_{}.png".format(timestr)
            camera.export_to_png(photo_path)
            MDApp.get_running_app().photo_captured(photo_path)
            self.back()
        except Exception as ex:
            logger.exception(ex)