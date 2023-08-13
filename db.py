from kivy.metrics import dp
from sqlite import SQLite
import time
from logger import logger
from datetime import datetime, timedelta


class DB():
    def __init__(self, db_connector) -> None:
        """
        Initialize the DB class.

        Parameters:
            db_connector: Used for connecting to the database.
        """
        self.db_connector = db_connector

    def searchables(self):
        """
        Function that returns dictionary of the searchable items.

        Returns:
            dict: A dictionary where keys are integers and values items.
        """
        data = {
            1: "facebook",
            2: "advertisement",
            3: "important contact",
            4: "laws & acts",
            5: "feedback",
            6: "speed limit",
            7: "caution helps",
            8: "downloadable forms"
        }
        return data

    @property
    def time_now(self):
        """
        Returns current date and time in format "YYYY-MM-DD HH:MM:SS".

        Returns:
            str: Current date and time.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def has_signed_up(self):
        """
        Property that checks if a user has signed up.

        Returns:
            bool: True if the user has signed up, False otherwise.
        """
        user = self.active_user()
        return False if not user else True

    @property
    def has_session(self):
        """
        Property that checks if there is an active session.

        Returns:
            bool: True if there is an active session, False otherwise.
        """
        session = self.active_session()
        return False if not session else True

    @property
    def loged_in_user(self):
        """
        Property that gets the logged-in user.

        Returns:
            dict: User information as a dictionary or None if no active session.
        """
        session = self.active_session()
        if not session:
            return None
        return self.get_user(session['username'])

    def get_stats_weekly(self):
        """
        Gets the weekly statistics.
        Returns:
            List[Dict["type": str, "total_weight": float]]
        """
        week_end = datetime.now()
        week_start = (week_end - timedelta(days=6)).strftime("%Y-%m-%d")
        week_end = week_end.strftime("%Y-%m-%d")
        query = f"SELECT recyclable_item_type.name as type, sum(recyclable_item.weight) as total_weight FROM recyclable_item join recyclable_item_type on recyclable_item.type = recyclable_item_type.id  WHERE date(recyclable_item.created_at) BETWEEN '{week_start}' AND '{week_end}' GROUP BY type"
        stats = self.db_connector.select(query)
        stats = [] if stats is None else stats
        return stats

    def get_stats_monthly(self):
        """
        Gets the monthly statistics.
        Returns:
            List[Dict["type": str, "total_weight": float]]
        """
        current_month = datetime.now().strftime("%m")
        query = f"SELECT recyclable_item_type.name as type, sum(recyclable_item.weight) as total_weight FROM recyclable_item join recyclable_item_type on recyclable_item.type = recyclable_item_type.id  WHERE strftime('%m', recyclable_item.created_at) = '{current_month}' GROUP BY type"
        stats = self.db_connector.select(query)
        stats = [] if stats is None else stats
        return stats

    def get_stats_yearly(self):
        """
        Gets the yearly statistics.
        Returns:
            List[Dict["type": str, "total_weight": float]]
        """
        current_year = datetime.now().strftime("%Y")
        query = f"SELECT recyclable_item_type.name as type, sum(recyclable_item.weight) as total_weight FROM recyclable_item join recyclable_item_type on recyclable_item.type = recyclable_item_type.id  WHERE strftime('%Y', recyclable_item.created_at) = '{current_year}' GROUP BY type"
        stats = self.db_connector.select(query)
        stats = [] if stats is None else stats
        return stats

    def get_stats_all(self):
        """
        Gets all statistics.
        Returns:
            List[Dict["type": str, "total_weight": float]]
        """
        query = "SELECT recyclable_item_type.name as type, sum(recyclable_item.weight) as total_weight FROM recyclable_item join recyclable_item_type on recyclable_item.type = recyclable_item_type.id GROUP BY type"
        stats = self.db_connector.select(query)
        stats = [] if stats is None else stats
        return stats

    def get_stats(self, duration, pie_chart=False):
        if duration == "WEEK":
            stats = self.get_stats_weekly()
        elif duration == "MONTH":
            stats = self.get_stats_monthly()
        elif duration == "YEAR":
            stats = self.get_stats_yearly()
        elif duration == "TOTAL":
            stats = self.get_stats_all()
        else:
            raise Exception("Invalid stats duration: ", duration)

        if not pie_chart:
            return stats

        total_weight_sum = sum([item['total_weight'] for item in stats])
        for stat in stats:
            stat["percentage"] = round(
                (stat['total_weight'] / total_weight_sum)*100)
        return stats

    def username_exists(self, username):
        """
        Function that check if a username exists in the user table    
        """
        query = f"SELECT * FROM user WHERE username = '{username}'"
        items = self.db_connector.select(query)
        items = [] if items is None else items
        return False if not items else True

    def get_recyclable_item_types(self):
        """
        Function that retrieve all recyclable item types from the recyclable_item_type table
        """
        query = "SELECT * FROM recyclable_item_type"
        items = self.db_connector.select(query)
        return [] if items is None else items

    def get_recyclable_items(self):
        """
        Retrieve recyclable items associated with the logged-in user
        """
        loged_in_user = self.loged_in_user
        if not loged_in_user:
            return []
        query = f"SELECT * FROM recyclable_item WHERE user_id = {loged_in_user['id']}"
        items = self.db_connector.select(query)
        return [] if items is None else items

    def get_user(self, username):
        """
        Function that retrieve a user based on their username
        """
        query = f"SELECT * FROM user WHERE username = '{username}'"
        items = self.db_connector.select(query)
        return None if not items else items[0]

    def active_user(self):
        """
        Function that retrieve all active users
        """
        query = "SELECT * FROM user"
        items = self.db_connector.select(query)
        return [] if not items else items[0]

    def active_session(self):
        """
        Function that retrieve all active sessions
        """
        query = "SELECT * FROM session"
        items = self.db_connector.select(query)
        return [] if not items else items[0]

    def delete(self, table, where):
        """
        Function that delete records from a table based on a given condition
        """
        query = f"DELETE FROM {table} WHERE {where}"
        return self.db_connector.execute(query)

    def insert(self, table: str, item: dict):
        """
        Insert a new item into a table
        """
        item['created_at'] = self.time_now
        qformat = """INSERT INTO {}({}) VALUES{};"""

        query = qformat.format(
            table, ', '.join(item.keys()),
            f"('{list(item.values())[0]}')" if len(
                item.values()) == 1 else tuple(f'{v}' for v in item.values())
        )
        return self.db_connector.execute(query)


db_connector = SQLite("data/recycleme.db")
db = DB(db_connector)
