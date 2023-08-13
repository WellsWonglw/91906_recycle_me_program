from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from functools import partial
from sqlite import SQLite
from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


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


class AddRecyclableItem(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get recyclable item types from the database
        types = db.get_recyclable_item_types()

        # Create a list of menu items for the dropdown menu
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item["name"],
                "height": dp(56),
                "on_release": lambda x=item: self.set_item(x),
            } for item in types
        ]

        # Create a dropdown menu with the menu items
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
        message = ""
        loged_in_user = db.loged_in_user
        if te_item_name.text == "":
            message = "NoDialog"
            te_item_name.error = True
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
