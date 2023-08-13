from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
from sqlite import SQLite
from kivymd.uix.button import MDRectangleFlatButton
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKPieChart
from db import DB

from screens_py.settings import Settings
from screens_py.about_us import AboutUs
from dbsc_login import Login
from dbsc_signup import Signup
from dbsc_search import Search
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
    def __init__(self, **kwargs):
        super(MDBoxlayoutClickable, self).__init__(**kwargs)


class ChartType:
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        return [cls.BAR_CHART, cls.PIE_CHART]


class Dialog():
    def __init__(self, **kwargs):
        super(Dialog, self).__init__()
        self.__alert_dialog = None
        self.__alert_dialog_result = None

    @property
    def RESULT_ALERT(self):
        return self.__alert_dialog_result

    def show_alert_dialog(self, text="Discard draft?"):
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
    pass


class AddRecyclableItem(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        types = db.get_recyclable_item_types()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item["name"],
                "height": dp(56),
                "on_release": lambda x=item: self.set_item(x),
            } for item in types
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, item):
        self.__new_item['type'] = item['id']
        self.ids.drop_item.set_item(item["name"])
        self.menu.dismiss()

    def set_captured_photo(self, photo_path):
        self.__new_item['photo_path'] = photo_path

    def load(self):
        self.manager.current = "add_recyclable_item"
        self.__new_item = {}

    def back(self):
        self.manager.current = "dashboard"

    def clear(self, te_item_name, te_weight):
        self.__new_item.clear()
        te_item_name.text = ""
        te_weight.text = ""
        self.ids.drop_item.set_item("Recyclable Type")

    def __validate_input(self, te_item_name, te_weight):
        def validate_weight():
            try:
                weight = float(te_weight.text)
                if weight > 0 and weight < 99999:
                    return True
                else:
                    te_weight.helper_text = "Weight value should be grater than 0 and less than 99999!"
                    return False
            except:
                return False

        message = ""
        loged_in_user = db.loged_in_user
        if te_item_name.text == "":
            message = "NoDialog"
            te_item_name.error = True
        elif not validate_weight():
            message = "NoDialog"
            te_weight.error = True
        elif "type" not in self.__new_item:
            message = "Recyclable item type is not selected!"
        elif "photo_path" not in self.__new_item:
            message = "Photo not taken!"
        elif loged_in_user is None:
            message = "No user is loged in!"

        if message != "":
            if message != "NoDialog":
                dialog_menu.show_alert_dialog(message)
            return False
        self.__new_item['name'] = te_item_name.text
        self.__new_item['user_id'] = loged_in_user['id']
        self.__new_item['weight'] = round(float(te_weight.text), 2)
        return True

    def on_save(self, te_item_name, te_weight):
        if self.__validate_input(te_item_name, te_weight):
            if db.insert("recyclable_item", self.__new_item):
                self.clear(te_item_name, te_weight)
                MDApp.get_running_app().load_recyclable_items_screen()
            else:
                dialog_menu.show_alert_dialog("Failed to save item!")

    def show_camera_screen(self):
        MDApp.get_running_app().load_camera_screen()


class RecyclableItems(Screen):
    def __init__(self, **kwargs):
        super(RecyclableItems, self).__init__()


class EmptyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def back(self, *args, **kwargs):
        self.manager.current = "dashboard"


class StatsButtons(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(StatsButtons, self).__init__(*args, **kwargs)


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    # region
    def load_login_screen(self):
        self.login.load()

    def load_dashboard_screen(self):
        self.dashboard.load()

    def load_add_recyclable_item_screen(self):
        self.add_recyclable_item.load()

    def load_camera_screen(self):
        self.camera_screen.load()

    def load_recyclable_items_screen(self):
        self.dashboard.load_recyclable_items_screen()

    def photo_captured(self, photo_path):
        self.add_recyclable_item.set_captured_photo(photo_path)
    # endregion

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        sm = WindowManager()
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

        if not db.has_signed_up:
            self.signup.load()
        else:
            self.login.load()

        return sm


if __name__ == '__main__':
    app = MainApp()
    app.run()
