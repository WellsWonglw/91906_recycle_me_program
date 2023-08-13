from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.behaviors import ButtonBehavior
from sqlite import SQLite
from db import DB
from lib_dashboard import dsh_load_dashboard_content
from lib_statistics import dsb__load_statistics
from lib_items import dsb__load_recyclable_items_content

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


class MDBoxlayoutClickable(ButtonBehavior, MDBoxLayout):
    """
    Combines ButtonBehavior and MDBoxLayout.
    It can be used to create clickable BoxLayout elements.
    """

    def __init__(self, **kwargs):
        super(MDBoxlayoutClickable, self).__init__(**kwargs)


class ChartType:
    """
    ChartType class defines for different chart types.
    """
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        """
        Return list of all available chart types.
        """
        return [cls.BAR_CHART, cls.PIE_CHART]


class Dasboard(Screen):
    """
    Dasboard includes different screens.
    """

    def __init__(self, **kwargs):
        super(Dasboard, self).__init__()
        self.__stats_type_menu = None

    def load_aboutus(self, arg1):
        """
        Load "about_us" screen.
        """
        self.manager.current = "about_us"

    def left_menu_dashboard(self):
        """
        Toggle the navigation drawer state and load different screen.
        """
        self.ids.nav_drawer.set_state("toggle")
        dsh_load_dashboard_content(self)

    def left_menu_settings(self):
        """
        Toggle the navigation drawer state and load settings screen.
        """
        self.ids.nav_drawer.set_state("toggle")
        self.manager.current = "settings"

    def left_menu_statistics(self):
        """
        Toggle the navigation drawer state and load pie chart.
        """
        self.ids.nav_drawer.set_state("toggle")
        dsb__load_statistics(self, ChartType.PIE_CHART)

    def left_menu_recyclable_items(self):
        """
        Toggle the navigation drawer state and load add items screen.
        """
        self.ids.nav_drawer.set_state("toggle")
        dsb__load_recyclable_items_content(self)

    def left_menu_search(self):
        """
        Toggle the navigation drawer state and load search screen.
        """
        self.ids.nav_drawer.set_state("toggle")
        self.manager.current = "search"

    def left_menu_about(self):
        """
        Toggle the navigation drawer state and load about us screen.
        """
        self.ids.nav_drawer.set_state("toggle")
        self.manager.current = "about_us"

    def left_menu_logout(self):
        """
        Delete session, load login screen, and toggle navigation drawer state.
        """
        db.delete("session", "1")
        MDApp.get_running_app().load_login_screen()
        self.ids.nav_drawer.set_state("toggle")

    def load(self):
        """
        Load dashboard content and set the current screen to "dashboard".
        """
        dsh_load_dashboard_content(self)
        self.manager.current = "dashboard"

    def load_collection_record_screen(self, arg1):
        """
        Load dashboard screen.
        """
        dsb__load_recyclable_items_content(self)
        self.manager.current = "dashboard"

    def load_recyclable_items_screen(self):
        """
        Load recyclable items content and set the current screen to "dashboard".
        """
        dsb__load_recyclable_items_content(self)
        self.manager.current = "dashboard"

    def load_pie_chart(self, *args, **kwargs):
        """
        Load statistics with Pie Chart type.
        """
        dsb__load_statistics(self, ChartType.PIE_CHART)

    def load_statistics(self, chart_type, duration, source):
        """
        Load statistics with specified chart type and duration.
        """
        dsb__load_statistics(self, chart_type, duration)

    def on_floating_btn(self):
        """
        Load "add_recyclable_item" screen.
        """
        MDApp.get_running_app().load_add_recyclable_item_screen()

    def magnifier(self):
        """
        Load "search" screen.
        """
        self.manager.current = "search"

    def load_chart(self, chart_type):
        """
        Load statistics with selected chart type.

        Parameters:
            chart_type (str): The selected chart type.
        """
        self.__stats_type_menu.dismiss()
        dsb__load_statistics(self, chart_type)

    def statistics_type_dialog(self, source):
        """
        Create dropdown menu with chart type options.

        Parameters:
            source: source widget calling the dropdown menu.
        """
        items = ChartType.list()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item,
                "height": dp(56),
                "on_release": lambda x=item: self.load_chart(x),
            } for item in items
        ]
        self.__stats_type_menu = MDDropdownMenu(
            caller=source,
            items=menu_items,
            width_mult=4,
        )
        self.__stats_type_menu.open()
