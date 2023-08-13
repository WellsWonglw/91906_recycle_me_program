from kivymd.app import MDApp
from kivy.properties import StringProperty
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


class Dasboard(Screen):
    def __init__(self, **kwargs):
        super(Dasboard, self).__init__()
        self.__stats_type_menu = None

    def load_aboutus(self, arg1):
        self.manager.current = "about_us"

    def load(self):
        dsh_load_dashboard_content(self)
        self.manager.current = "dashboard"

    def load_collection_record_screen(self, arg1):
        dsb__load_recyclable_items_content(self)
        self.manager.current = "dashboard"

    def load_recyclable_items_screen(self):
        dsb__load_recyclable_items_content(self)
        self.manager.current = "dashboard"

    def load_pie_chart(self, *args, **kwargs):
        dsb__load_statistics(self, ChartType.PIE_CHART)

    def load_statistics(self, chart_type, duration, source):
        dsb__load_statistics(self, chart_type, duration)

    def on_floating_btn(self):
        MDApp.get_running_app().load_add_recyclable_item_screen()

