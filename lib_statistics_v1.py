from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from functools import partial
from kivymd.uix.button import MDRectangleFlatButton
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKPieChart
from sqlite import SQLite

from db import DB

db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)


class ChartType:
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        return [cls.BAR_CHART, cls.PIE_CHART]


def dsb__get_chart(self, chart_type, duration):
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
            bars_color=(255/255, 106/255, 68/255, 255/255),
            size_hint_y=0.8,
            bg_color=(3/255, 13/255, 59/255, 255/255)
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
                items=[items_dict]
            )
            return chart
        except Exception as ex:
            print(ex)
            return None


def dsb__load_statistics(self, chart_type, duration="TOTAL"):
    self.ids.boxes.clear_widgets()
    chart = dsb__get_chart(self, chart_type, duration)
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
    self.ids.top_bar.right_action_items = [
        ["dots-vertical", lambda x: self.statistics_type_dialog(x)]]
    self.ids.floating_btn.opacity = 0
    self.ids.floating_btn.disabled = True
