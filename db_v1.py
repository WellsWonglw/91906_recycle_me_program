from kivy.metrics import dp
from sqlite import SQLite
import time
from logger import logger
from datetime import datetime, timedelta

class DB():
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        
    def username_exists(self, username):
        query = f"SELECT * FROM user WHERE username = '{username}'"
        items = self.db_connector.select(query)
        items =  [] if items is None else items
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

    def delete(self, table, where):
        query = f"DELETE FROM {table} WHERE {where}"
        return self.db_connector.execute(query)

    def insert(self, table: str, item: dict):
        item['created_at'] = self.time_now
        qformat	= """INSERT INTO {}({}) VALUES{};"""
        query = qformat.format(
                table, ', '.join(item.keys()),
                f"('{list(item.values())[0]}')" if len(item.values()) == 1 else tuple(f'{v}' for v in item.values())
            )
        return self.db_connector.execute(query)


db_connector = SQLite("assets/recycle_tracker.db")
db = DB(db_connector)