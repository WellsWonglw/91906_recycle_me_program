from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from sqlite import SQLite
from db import DB

# Create a SQLite object for the database connection
db_connector = SQLite("data/recycleme.db")

# Create a DB object using the SQLite connector
db = DB(db_connector)


def dsb__load_recyclable_items_content(self):
    """
    Load recyclable items screen
    """
    self.ids.boxes.clear_widgets()

    # Constants and initializations
    r = 8
    padding_x = 5
    item_height = 100
    recycled_item_types = db.get_recyclable_item_types()
    recycled_item_types = {item['id']: item for item in recycled_item_types}
    recycled_items = db.get_recyclable_items()
    content = [
        (f"[size=14]{item['name']}[/size]", f"{item['photo_path']}", f"[size=14]{recycled_item_types[item['type']]['name']}[/size]",
         f"[size=14]{item['weight']} oz[/size]", f"{recycled_item_types[item['type']]['color']}", (1, 1, 1, 1))
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

    # Loop through each recyclable item and create widgets for display
    for desc, img_path, _type, amt, type_bg_color, type_text_color in content:

        # Create the main box layout to hold item information
        box = MDBoxLayout(
            # md_bg_color = app.theme_cls.primary_color,
            # line_color = (0.3, 0.3, 0.3, 1),
            line_color=(0, 128/255, 128/255, 1),
            orientation="vertical",
            size_hint_y=None,
            height=item_height,
            radius=(r, r, r, r),
            padding=1
        )
        box1 = MDBoxLayout(
            # md_bg_color = (255/255, 255/255, 179/255, 1),
            md_bg_color=(0, 0, 0, 0),
            radius=(r, r, 0, 0),
            size_hint_y=None,
            height=int(item_height*0.7)-2,
            spacing=5
        )
        box1.add_widget(
            MDLabel(
                padding_x=padding_x,
                size_hint_x=0.8,
                halign='left',
                markup=True,
                text=desc,
                theme_text_color="Custom",
                text_color=type_bg_color
            )
        )
        box1.add_widget(
            Image(
                size_hint_x=0.2,
                source=img_path
            )
        )
        box2 = MDBoxLayout(
            radius=(0, 0, r, r),
            size_hint_y=None,
            height=int(item_height*0.3),
            # md_bg_color = MDApp.theme_cls.primary_color,
            md_bg_color=(0, 128/255, 128/255, 1),
            spacing=5
        )
        box2.add_widget(
            MDLabel(
                padding_x=padding_x,
                size_hint_x=0.8,
                halign='left',
                markup=True,
                theme_text_color="Custom",
                text_color="white",
                text=_type
            )
        )
        box2.add_widget(
            MDLabel(
                size_hint_x=0.2,
                halign='left',
                markup=True,
                theme_text_color="Custom",
                text_color="white",
                text=amt
            )
        )
        # Add the sub-layouts to the main box layout
        box.add_widget(box1)
        box.add_widget(box2)
        # Add the main box layout to the grid layout
        grid.add_widget(box)

    # Add the grid layout to the scrollable view
    scroller.add_widget(grid)
    # Add the scrollable view to the "boxes" container
    self.ids.boxes.add_widget(scroller)

    # Update UI elements
    self.ids.top_bar.title = "Collection Record"
    self.ids.top_bar.right_action_items = []
    self.ids.floating_btn.opacity = 1
    self.ids.floating_btn.disabled = False
