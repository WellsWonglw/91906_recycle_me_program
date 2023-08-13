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

######## To Change Window Size & Position ##########
from kivy.core.window import Window
Window.size = (350, 600)
Window.top = 50
Window.left = 200

db_connector = SQLite("assets/recycle_tracker.db")
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
                #"icon": "git",
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

class Dasboard(Screen):
    def __init__(self, **kwargs):
        super(Dasboard, self).__init__()
        self.__stats_type_menu = None

    def __load_recyclable_items_content(self):
        self.ids.boxes.clear_widgets()
        r = 8
        padding_x = 5
        item_height = 100
        recycled_item_types = db.get_recyclable_item_types()
        recycled_item_types = {item['id']: item for item in recycled_item_types}
        recycled_items = db.get_recyclable_items()
        content = [
            (f"[size=14]{item['name']}[/size]", f"{item['photo_path']}", f"[size=14]{recycled_item_types[item['type']]['name']}[/size]", f"[size=14]{item['weight']} oz[/size]", f"{recycled_item_types[item['type']]['color']}", (1, 1, 1, 1))
            for item in recycled_items
        ]
        scroller = ScrollView(
            bar_width=0
        )
        grid = MDGridLayout(
            spacing=3,
            adaptive_height=True,
            cols=1
        )
        for desc, img_path, _type, amt, type_bg_color, type_text_color in content:
            box = MDBoxLayout(
                orientation= "vertical",
                size_hint_y=None,
                height=item_height, 
                radius= (r, r, r, r),
                md_bg_color= (0.1, 0.1, 0.1, 0.1),
                padding=1
            )
            box1 = MDBoxLayout(
                md_bg_color= "white",
                radius= (r, r, 0, 0),
                size_hint_y= None,
                height=int(item_height*0.7)-2,
                spacing= 5
            )
            box1.add_widget(
                MDLabel(
                    padding_x=padding_x,
                    size_hint_x= 0.8,
                    halign= 'left',
                    markup= True,
                    text= desc
                )
            )
            box1.add_widget(
                Image(
                    size_hint_x= 0.2,
                    source= img_path
                )
            )
            box2 = MDBoxLayout(
                md_bg_color= type_bg_color,
                radius= (0, 0, r, r),
                size_hint_y= None,
                height=int(item_height*0.3),
                spacing= 5
            )
            box2.add_widget(
                MDLabel(
                    padding_x=padding_x,
                    size_hint_x= 0.8,
                    halign= 'left',
                    markup= True,
                    theme_text_color= "Custom",
                    text_color= type_text_color,
                    text= _type
                )
            )
            box2.add_widget(
                MDLabel(
                    size_hint_x= 0.2,
                    halign= 'left',
                    markup= True,
                    theme_text_color= "Custom",
                    text_color= type_text_color,
                    text= amt
                )
            )
            box.add_widget(box1)
            box.add_widget(box2)
            grid.add_widget(box)
        scroller.add_widget(grid)
        self.ids.boxes.add_widget(scroller)
        self.ids.top_bar.title = "Recyclable Items"
        self.ids.top_bar.right_action_items= [["magnify", lambda x: self.magnifier()]]
        self.ids.floating_btn.opacity = 1
        self.ids.floating_btn.disabled = False

    def __get_chart(self, chart_type, duration):
        pie_chart = True if chart_type == ChartType.PIE_CHART else False
        if chart_type == ChartType.BAR_CHART:
            stats = db.get_stats(duration, pie_chart)
            if not stats:
                return None
            x_labels = [stat['type'] for stat in stats]
            y_value = [stat['total_weight'] for stat in stats]
            chart = AKBarChart(
                labels=True,
                anim=False,
                label_size=15,
                bars_radius=0,
                bars_color=(0.21, 0.24, 0.25, 1),
                size_hint_y=0.8,
                bg_color=(0.1, 0.3, 0.9, 1)
            )
            chart.x_values = list(range(len(x_labels)))
            chart.y_values = y_value
            chart.x_labels = x_labels
            return chart
        elif chart_type == ChartType.PIE_CHART:
            stats = db.get_stats(duration, pie_chart=True)
            if not stats:
                print("no stats availabe for pie chart!")
                return None
            items_dict = {stat['type']: stat['percentage'] for stat in stats}
            sum_of_stats = sum(items_dict.values())
            if sum_of_stats != 100:
                items_dict[list(items_dict)[0]] += 100 - sum_of_stats
            sum_of_stats = sum(items_dict.values())
            if sum_of_stats != 100:
                items_dict[list(items_dict)[0]] += 100 - sum_of_stats
                print(f"sum of stats({sum_of_stats}) is not 100: ", items_dict)
                return None
            
            try:
                chart = AKPieChart(
                    items= [items_dict]
                )
                return chart
            except Exception as ex:
                print(ex)
                return None
            
    def __load_statistics(self, chart_type, duration="TOTAL"):
        self.ids.boxes.clear_widgets()
        chart = self.__get_chart(chart_type, duration)
        stats_btns_box = MDBoxLayout(
            orientation="horizontal",
            spacing=5,
            padding=5,
            size_hint_y=0.2
        )
        for button_text in ["WEEK", "MONTH", "YEAR", "TOTAL"]:
            btn = MDRectangleFlatButton(
                text=button_text,
                on_release=partial(self.load_statistics, chart_type, button_text)
            )
            stats_btns_box.add_widget(btn)
        if chart:
            self.ids.boxes.add_widget(chart)
        self.ids.boxes.add_widget(stats_btns_box)
        self.ids.top_bar.title = f"Statistics({duration.capitalize()})" 
        self.ids.top_bar.right_action_items= [["dots-vertical", lambda x: self.statistics_type_dialog(x)]]
        self.ids.floating_btn.opacity = 0
        self.ids.floating_btn.disabled = True

    def __load_dashboard_content(self):
        self.ids.boxes.clear_widgets()
        dashboard_content = [
            ("assets/question_mark.png", "[size=14]Do you collect a lot of plastic shopping bags from the grocery stores ? You can usually bring them back to the same store for recycling.[/size]"),
            ("assets/analytics.png", "[size=14]Total recycled: 10.93oz. You are most likely to recycle Glass.[/size]"),
            ("assets/light.png", "[size=14]Your recycling saved 0.45 kWh of energy.[/size]"),
            ("assets/trees.png", "[size=14]Less trees need to be cut down when more paper products are recycled. Recycle Tracker will try to estimate amount of trees you have saved over time.[/size]")
        ]
        for icon_source, text in dashboard_content:
            box = MDBoxlayoutClickable(
                line_color= (0.3, 0.3, 0.3, 1),
                radius= (12, 12, 12, 12),
                md_bg_color= "white",
                padding= 5,
                on_press= self.load_empty_screen

            )
            box.add_widget(
                Image(
                    size_hint_x= 0.2,
                    source= icon_source
                )
            )
            box.add_widget(
                MDLabel(
                    size_hint_x= 0.8,
                    halign= 'left',
                    markup= True,
                    text= text
                )
            )
            self.ids.boxes.add_widget(box)
        self.ids.top_bar.title = "Recycle Me"
        self.ids.top_bar.right_action_items= []
        self.ids.floating_btn.opacity = 1
        self.ids.floating_btn.disabled = False

    def left_menu_dashboard(self):
        self.ids.nav_drawer.set_state("toggle")
        self.__load_dashboard_content()
    
    def left_menu_settings(self):
        self.ids.nav_drawer.set_state("toggle")
        self.manager.current = "settings"

    def left_menu_statistics(self):         
        self.ids.nav_drawer.set_state("toggle")
        self.__load_statistics(ChartType.PIE_CHART)

    def left_menu_recyclable_items(self):
        self.ids.nav_drawer.set_state("toggle")
        self.__load_recyclable_items_content()

    def left_menu_about(self):
        self.ids.nav_drawer.set_state("toggle")
        self.manager.current = "about_us"

    def left_menu_logout(self):
        db.delete("session", "1")
        MDApp.get_running_app().load_login_screen()
        self.ids.nav_drawer.set_state("toggle")

    def load(self):
        self.__load_dashboard_content()
        self.manager.current = "dashboard"

    def load_recyclable_items_screen(self):
        self.__load_recyclable_items_content()
        self.manager.current = "dashboard"

    def load_empty_screen(self, *args, **kwargs):
        self.__load_statistics(ChartType.PIE_CHART)
    
    def load_statistics(self, chart_type, duration, source):
        self.__load_statistics(chart_type, duration)

    def on_floating_btn(self):
        MDApp.get_running_app().load_add_recyclable_item_screen()
    
    def magnifier(self):
        self.manager.current = "search"

    def load_chart(self, chart_type):
        self.__stats_type_menu.dismiss()
        self.__load_statistics(chart_type)

    def statistics_type_dialog(self, source):
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

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    #region
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
    #endregion

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        sm              = WindowManager()
        self.login      = Login(name="login")
        sm.add_widget   (self.login)
        self.signup     = Signup(name="signup")
        sm.add_widget   (self.signup)
        self.settings   = Settings(name="settings")
        sm.add_widget   (self.settings)
        self.about_us   = AboutUs(name="about_us")
        sm.add_widget   (self.about_us)
        self.dashboard      = Dasboard(name='dashboard')
        sm.add_widget       (self.dashboard)
        self.add_recyclable_item = AddRecyclableItem(name='add_recyclable_item')
        sm.add_widget       (self.add_recyclable_item)
        self.empty_screen   = EmptyScreen(name="empty_screen")
        sm.add_widget       (self.empty_screen)
        self.camera_screen  = CameraScreen(name="camera_screen")
        sm.add_widget       (self.camera_screen)
        self.search  = Search(name='search')
        sm.add_widget   (self.search)
        
        if not db.has_signed_up:
            self.signup.load()
        else:
            self.login.load()
        
        return sm

if __name__ == '__main__':
    app = MainApp()
    app.run()
