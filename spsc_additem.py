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
    """Represents a dialog window for displaying alerts."""

    def __init__(self, **kwargs):
        """
        Initialize a new Dialog object.

        Parameters:
            kwargs: Additional keyword arguments (unused).
        """
        super(Dialog, self).__init__()
        self.__alert_dialog = None
        self.__alert_dialog_result = None

    @property
    def RESULT_ALERT(self):
        """
        Get the result of the alert dialog.

        Returns:
            str: The result of the alert dialog.
        """
        return self.__alert_dialog_result

    def show_alert_dialog(self, text="Discard draft?"):
        """
        Show an alert dialog with the specified text.

        Parameters:
            text to display in the alert dialog.
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


class AddRecyclableItem(Screen):
    """Screen class for adding a recyclable item."""

    def __init__(self, **kwargs):
        """Initialize the AddRecyclableItem screen.

        Keyword Arguments:
        **kwargs -- Additional keyword arguments
        """
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
        """Set the selected item's type and update the dropdown text.

        Arguments:
        item -- selected recyclable item type
        """
        self.__new_item['type'] = item['id']
        self.ids.drop_item.set_item(item["name"])
        self.menu.dismiss()

    def set_captured_photo(self, photo_path):
        """Set the photo path of the captured photo for the new item.

        Arguments:
        photo_path -- The file path of the captured photo
        """
        self.__new_item['photo_path'] = photo_path

    def load(self):
        """Load "add_recyclable_item" screen and initialize new item."""
        self.manager.current = "add_recyclable_item"
        self.__new_item = {}

    def back(self):
        """Return back to the "dashboard" screen."""
        self.manager.current = "dashboard"

    def clear(self, te_item_name, te_weight):
        """Clear new_item dictionary and reset text inputs and dropdown.

        Arguments:
        te_item_name -- text input for the recyclable item name
        te_weight -- text input for the item's weight
        """
        self.__new_item.clear()
        te_item_name.text = ""
        te_weight.text = ""
        self.ids.drop_item.set_item("Recyclable Type")

    def __validate_input(self, te_item_name, te_weight):
        """Validate the user inputs for the new item.

        Arguments:
        te_item_name -- The text input for the recyclable item name
        te_weight -- The text input for the item's weight

        Returns:
        True if the inputs are valid, False otherwise
        """

        # Function that validate the weight input
        def validate_weight():
            try:
                weight = float(te_weight.text)
                if weight > 0 and weight < 1410:
                    return True
                else:
                    te_weight.helper_text = "Weight value should be grater than 0 and less than 1410!"
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
        """Save the new item if the inputs are valid.

        Arguments:
        te_item_name -- The text input for the recyclable item name
        te_weight -- The text input for the item's weight
        """
        if self.__validate_input(te_item_name, te_weight):
            if db.insert("recyclable_item", self.__new_item):
                self.clear(te_item_name, te_weight)
                MDApp.get_running_app().load_recyclable_items_screen()
            else:
                dialog_menu.show_alert_dialog("Failed to save item!")

    def show_camera_screen(self):
        """Show the camera screen to capture a photo of the item."""
        MDApp.get_running_app().load_camera_screen()
