from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
from sqlite import SQLite
from db import DB

from screens_py.settings import Settings
from screens_py.about_us import AboutUs
from dbsc_login import Login
from dbsc_signup import Signup
from dbsc_search import Search
from spsc_additem import AddRecyclableItem
from spsc_camera import CameraScreen
from dbsc_dashboard import Dasboard

######## To Change Window Size & Position ##########
from kivy.core.window import Window
Window.size = (350, 600)
Window.top = 50
Window.left = 200

db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)


class MDBoxlayoutClickable(ButtonBehavior, MDBoxLayout):
    """
    This class represents a custom clickable box layout widget that combines the functionality of ButtonBehavior and MDBoxLayout.
    """

    def __init__(self, **kwargs):
        """
        Constructor method for MDBoxlayoutClickable.

        :param kwargs: Optional keyword arguments to pass to the parent classes' constructors.
        """
        super(MDBoxlayoutClickable, self).__init__(**kwargs)


class ChartType:
    """
    The ChartType class defines constants for different chart types.
    """
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        """
        Get a list of all available chart types.

        :return: A list containing the names of all available chart types as strings.
        """
        return [cls.BAR_CHART, cls.PIE_CHART]


class Dialog():
    """
    The Dialog class represents a dialog window for displaying alerts.

    Attributes:
        __alert_dialog (object): An object representing the alert dialog window.
        __alert_dialog_result: The result of the alert dialog window.
    """

    def __init__(self, **kwargs):
        super(Dialog, self).__init__()
        self.__alert_dialog = None
        self.__alert_dialog_result = None

    @property
    def RESULT_ALERT(self):
        """
        Get the result of the alert dialog.

        Returns:
            The result of the alert dialog.
        """
        return self.__alert_dialog_result

    def show_alert_dialog(self, text="Discard draft?"):
        """
        Function that shows an alert dialog.
        Displays an alert dialog with two buttons.

        Args:
            text (str, optional): The text to be displayed in the alert dialog.
                                  Defaults to "Discard draft?".

        Returns:
        None
        """
        def result(res, caller):
            self.__alert_dialog_result = res
            self.__alert_dialog.dismiss()

        if self.__alert_dialog is None:
            self.__alert_dialog = MDDialog(
                text=text,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=partial(result, "CANCEL")
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=partial(result, "OK")
                    ),
                ],
            )
        self.__alert_dialog.text = text
        self.__alert_dialog.open()


dialog_menu = Dialog()


class DrawerList(ThemableBehavior, MDList):
    """
    Create drawer list with customizable themes and Material Design style.
    """
    pass


class EmptyScreen(Screen):
    """
    Extends functionality of Kivy Screen to provide back method.
    Overridden in subclasses to handle custom back navigation logic.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def back(self, *args, **kwargs):
        self.manager.current = "dashboard"


class StatsButtons(MDBoxLayout):
    """
    Inherits from Kivy MDBoxLayout and provides a custom layout
    designed for displaying statistics button.
    """

    def __init__(self, *args, **kwargs):
        super(StatsButtons, self).__init__(*args, **kwargs)


class WindowManager(ScreenManager):
    """A custom ScreenManager class.
    Extends functionality of Kivy ScreenManager to provide
    for managing multiple screens in application.
    """
    pass


class MainApp(MDApp):
    """
    Main application class that extends MDApp.
    Responsible for managing various screens and building the application.
    """

    # region
    def load_login_screen(self):
        """
        Load login screen by calling 'load()' method of the 'login' screen.
        """
        self.login.load()

    def load_dashboard_screen(self):
        """
        Load dashboard screen by calling 'load()' method of the 'dashboard' screen.
        """
        self.dashboard.load()

    def load_add_recyclable_item_screen(self):
        """
        Load add recyclable item screen by calling 'load()' method of 'add_recyclable_item' screen.
        """
        self.add_recyclable_item.load()

    def load_camera_screen(self):
        """
        Load camera screen by calling the 'load()' method of the 'camera_screen' screen.
        """
        self.camera_screen.load()

    def load_recyclable_items_screen(self):
        """
        Load recyclable items screen by calling 'load_recyclable_items_screen()' method.
        """
        self.dashboard.load_recyclable_items_screen()

    def photo_captured(self, photo_path):
        """
        Captured photo path in 'add_recyclable_item' screen.

        Parameters:
            photo_path (str): The path to the captured photo.
        """
        self.add_recyclable_item.set_captured_photo(photo_path)
    # endregion

    def build(self):
        """
        Build application and return custom ScreenManager instance.

        Returns:
            MDScreenManager: custom ScreenManager instance containing various screens.
        """
        # Set the theme settings
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Create an instance of the custom ScreenManager
        sm = WindowManager()

        # Add screens to the ScreenManager
        self.login = Login(name="login")
        sm.add_widget(self.login)

        self.signup = Signup(name="signup")
        sm.add_widget(self.signup)

        self.settings = Settings(name="settings")
        sm.add_widget(self.settings)

        self.about_us = AboutUs(name="about_us")
        sm.add_widget(self.about_us)

        self.dashboard = Dasboard(name='dashboard')
        sm.add_widget(self.dashboard)

        self.add_recyclable_item = AddRecyclableItem(
            name='add_recyclable_item')
        sm.add_widget(self.add_recyclable_item)

        self.empty_screen = EmptyScreen(name="empty_screen")
        sm.add_widget(self.empty_screen)

        self.camera_screen = CameraScreen(name="camera_screen")
        sm.add_widget(self.camera_screen)

        self.search = Search(name='search')
        sm.add_widget(self.search)

        # Check if a user has signed up and load the appropriate screen
        if not db.has_signed_up:
            self.signup.load()
        else:
            self.login.load()

        # Return the custom ScreenManager instance
        return sm


# Check if the script is being run directly and create an instance of the MainApp
if __name__ == '__main__':
    app = MainApp()
    app.run()
