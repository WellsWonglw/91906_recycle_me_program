from kivy.metrics import dp
from sqlite import SQLite
import time
from logger import logger
from datetime import datetime, timedelta


class DB():
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector

    def searchables(self):
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
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def has_signed_up(self):
        user = self.active_user()
        return False if not user else True

    @property
    def has_session(self):
        session = self.active_session()
        return False if not session else True

    @property
    def loged_in_user(self):
        session = self.active_session()
        if not session:
            return None
        return self.get_user(session['username'])

    def get_stats_weekly(self):
        """
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
        query = f"SELECT * FROM user WHERE username = '{username}'"
        items = self.db_connector.select(query)
        items = [] if items is None else items
        return False if not items else True

    def get_recyclable_item_types(self):
        query = "SELECT * FROM recyclable_item_type"
        items = self.db_connector.select(query)
        return [] if items is None else items

    def get_recyclable_items(self):
        loged_in_user = self.loged_in_user
        if not loged_in_user:
            return []
        query = f"SELECT * FROM recyclable_item WHERE user_id = {loged_in_user['id']}"
        items = self.db_connector.select(query)
        return [] if items is None else items

    def get_user(self, username):
        query = f"SELECT * FROM user WHERE username = '{username}'"
        items = self.db_connector.select(query)
        return None if not items else items[0]

    def active_user(self):
        query = "SELECT * FROM user"
        items = self.db_connector.select(query)
        return [] if not items else items[0]

    def active_session(self):
        query = "SELECT * FROM session"
        items = self.db_connector.select(query)
        return [] if not items else items[0]

    def delete(self, table, where):
        query = f"DELETE FROM {table} WHERE {where}"
        return self.db_connector.execute(query)

    def insert(self, table: str, item: dict):
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
