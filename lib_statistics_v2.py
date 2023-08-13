from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from functools import partial
from kivymd.uix.button import MDRectangleFlatButton
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKPieChart
from sqlite import SQLite
from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


class ChartType:
    """
    ChartType class defines constants for different chart types.
    """
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        return [cls.BAR_CHART, cls.PIE_CHART]


def dsb__get_chart(self, chart_type, duration):
    """
    Get the appropriate chart based on chart_type and duration.
    """
    # Determine if the chart type is a Pie Chart
    pie_chart = True if chart_type == ChartType.PIE_CHART else False

    if chart_type == ChartType.BAR_CHART:
        # Fetch statistics data from the database for Bar Chart
        stats = db.get_stats(duration, pie_chart)
        if not stats:
            return None

        # Extract the data for x-axis labels and y-axis values
        x_labels = [stat['type'] for stat in stats]
        y_value = [stat['total_weight'] for stat in stats]

        # Create an AKBarChart instance with the fetched data
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
        # Fetch statistics data from the database for Pie Chart
        stats = db.get_stats(duration, pie_chart=True)
        if not stats:
            print("no stats available for pie chart!")
            return None

        # Calculate the percentage for each item in the Pie Chart
        items_dict = {stat['type']: stat['percentage'] for stat in stats}
        sum_of_stats = sum(items_dict.values())

        if sum_of_stats != 100:
            items_dict[list(items_dict)[0]] += 100 - sum_of_stats
        sum_of_stats = sum(items_dict.values())

        if sum_of_stats != 100:
            items_dict[list(items_dict)[0]] += 100 - sum_of_stats
            print("sum of stats({sum_of_stats}) is not 100: ", items_dict)
            return None

        try:
            # Create an AKPieChart instance with the calculated percentages
            chart = AKPieChart(
                items=[items_dict]
            )
            return chart
        except Exception as ex:
            print(ex)
            return None


def dsb__load_statistics(self, chart_type, duration="TOTAL"):
    """
    Load the statistics and update the UI.
    """
    # Clear any existing widgets from the boxes layout
    self.ids.boxes.clear_widgets()

    # Get the appropriate chart based on the chart_type and duration
    chart = dsb__get_chart(self, chart_type, duration)

    # Create a box layout for the statistics buttons
    stats_btns_box = MDBoxLayout(
        orientation="horizontal",
        spacing=5,
        padding=5,
        size_hint_y=0.2
    )

    # Create buttons for different duration and add them to box layout
    for button_text in ["WEEK", "MONTH", "YEAR", "TOTAL"]:
        btn = MDRectangleFlatButton(
            text=button_text,
            on_release=partial(self.load_statistics, chart_type, button_text)
        )
        stats_btns_box.add_widget(btn)

    # Add the chart and the statistics buttons box to the boxes layout
    if chart:
        self.ids.boxes.add_widget(chart)
    self.ids.boxes.add_widget(stats_btns_box)

    # Update the title and action items of the top bar
    self.ids.top_bar.title = "Statistics({duration.capitalize()})"
    self.ids.top_bar.right_action_items = [
        ["dots-vertical", lambda x: self.statistics_type_dialog(x)]]

    # Hide and disable the floating button
    self.ids.floating_btn.opacity = 0
    self.ids.floating_btn.disabled = True
