import sqlite3
from typing import Iterable
from logger import logger

class SQLite():
    def __init__(self, db_file) -> None:
        super().__init__()
        self.db_file = db_file

    # Function that establishes a connection to the SQLite database.
    def connect(self):
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute('PRAGMA synchronous=0')
            return conn, conn.cursor()
        except Exception as ex:
            logger.exception(ex)
            return None, None
    
    # Function that closes the connection and cursor objects.
    def close(self, conn, cursor):
        try:
            cursor.close()
        except Exception as ex:
            logger.exception(ex)
        try:
            conn.close()
        except Exception as ex:
            logger.exception(ex)

    # Function that rolls back a transaction on the given connection.
    def rollback(self, conn):
        try:
            conn.rollback()
        except Exception as ex:
            logger.exception(ex)

    # Function that executes the given script on the SQLite database. (insert, update and delete)
    def execute(self, query: str, is_script=False):
        try:
            conn, cursor = self.connect()
            if is_script:
                cursor.executescript(query)
            else:
                logger.info(f"query: {query}")
                cursor.execute(query)
            conn.commit()
            result = True
        except Exception as ex:
            logger.exception(ex)
            self.rollback(conn)
            result = False
        finally:
            self.close(conn, cursor)
        return result

    # Function that executes a select query on the SQLite database. (search or find record)
    def select(self, query: str) -> Iterable[dict]:
        try:
            conn, cursor = self.connect()
            q_result = cursor.execute(query)
            cols = [item[0] for item in q_result.description]
            rows = q_result.fetchall()
            return [{key:val for key, val in zip(cols, row)} for row in rows]
        except Exception as ex:
            logger.exception(ex)
        finally:
           self.close(conn, cursor)