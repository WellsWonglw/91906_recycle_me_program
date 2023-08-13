from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior


class MDBoxlayoutClickable(ButtonBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super(MDBoxlayoutClickable, self).__init__(**kwargs)


def dsh_load_dashboard_content(self):
    """
    Layout of the dashboard 
    Clear existing widgets from the 'boxes' container
    """
    self.ids.boxes.clear_widgets()

    # Create a box layout with a clickable behavior
    box = MDBoxlayoutClickable(
        radius = (12, 12, 12, 12),
        md_bg_color = (0, 0, 0, 0),
        padding = 5,
    )
    box.add_widget(
        MDLabel(
            size_hint_x = 0.8,
            halign = 'center',
            markup = True,
            text = "[size=20][b]Welcome to our [color=#00883c][i]Recycle ME[/i][/color] app![/b][/size]"
        )
    )
    self.ids.boxes.add_widget(box)

    # Create another box layout with clickable behavior
    box = MDBoxlayoutClickable(
        line_color = (0, 128/255, 128/255, 1),
        radius = (12, 12, 12, 12),
        md_bg_color = (0, 0, 0, 0),
        padding = 5,
        on_press = self.load_collection_record_screen
    )
    box.add_widget(
        Image(
            size_hint_x = 0.2,
            source = "assets/record2.png"
        )
    )
    box.add_widget(
        MDLabel(
            size_hint_x = 0.8,
            halign = 'left',
            markup = True,
            text = "[size=14][color=#00883c][b]Collection Record:[/b][/color] Track your recycled items and see how you impact the environment.[/size]"
        )
    )
    self.ids.boxes.add_widget(box)

    # Create another box layout with clickable behavior
    box = MDBoxlayoutClickable(
        line_color = (0, 128/255, 128/255, 1),
        radius = (12, 12, 12, 12),
        md_bg_color = (0, 0, 0, 0),
        padding = 5,
        on_press = self.load_pie_chart
    )
    box.add_widget(
        Image(
            size_hint_x = 0.2,
            source = "assets/analytics.png"
        )
    )
    box.add_widget(
        MDLabel(
            size_hint_x = 0.8,
            halign = 'left',
            markup = True,
            text = "[size=14][color=#00883c][b]Statistics:[/b][/color] You can see how many items you have recycled.[/size]"
        )
    )
    self.ids.boxes.add_widget(box)

    # Create another box layout with clickable behavior
    box = MDBoxlayoutClickable(
        line_color = (0, 128/255, 128/255, 1),
        radius = (12, 12, 12, 12),
        md_bg_color = (0, 0, 0, 0),
        padding = 5,
        on_press = self.load_aboutus
    )
    box.add_widget(
        Image(
            size_hint_x = 0.2,
            source = "assets/AboutUs.png"
        )
    )
    box.add_widget(
        MDLabel(
            size_hint_x = 0.8,
            halign = 'left',
            markup = True,
            text = "[size=14][color=#00883c][b]About Us:[/b][/color] We are dedicated to promoting and encouraging sustainable habits by helping you keep track of your recycling efforts. Click me to see more about us.[/size]"
        )
    )
    self.ids.boxes.add_widget(box)

    # Update other UI elements
    self.ids.top_bar.title = "Recycle ME"
    self.ids.top_bar.right_action_items= []
    self.ids.floating_btn.opacity = 1
    self.ids.floating_btn.disabled = False
