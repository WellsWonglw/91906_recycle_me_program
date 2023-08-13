import sqlite3
from typing import Iterable
from logger import logger


class SQLite:
    def __init__(self, db_file) -> None:
        """
        Initializes the SQLite object with the specified database file.

        Parameters:
            db_file (str): The path to the SQLite database file.

        Returns:
            None
        """
        super().__init__()
        self.db_file = db_file


    # Function that establishes a connection to the SQLite database.
    def connect(self):
        """
        Establishes a connection to the SQLite database.
        If the connection is successful, it returns the connection and cursor.

        Returns:
            tuple: A tuple containing the SQLite database connection and cursor.
        """
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute("PRAGMA synchronous = 0")
            return conn, conn.cursor()
        except Exception as ex:
            logger.exception(ex)
            return None, None


    # Function that closes the connection and cursor objects.
    def close(self, conn, cursor):
        """
        Closes the SQLite database connection and cursor.

        Parameters:
            conn: sqlite3.Connection or None
                The SQLite database connection object. If None, it will be ignored.
            cursor: sqlite3.Cursor or None
                The SQLite cursor object. If None, it will be ignored.

        Returns:
            None
        """
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
        """
        Rollbacks the current transaction in the SQLite database.

        Parameters:
            conn: sqlite3.Connection or None
                The SQLite database connection object. If None, the rollback operation will be ignored.

        Returns:
            None
        """
        try:
            conn.rollback()
        except Exception as ex:
            logger.exception(ex)


    # Function that executes the given script on the SQLite database. (insert, update and delete)
    def execute(self, query: str, is_script=False):
        """
        Function that executes the given script on the SQLite database.
        (insert, update and delete)

        Returns:
            The result of execution will be returned.
        """
        try:
            conn, cursor = self.connect()
            if is_script:
                cursor.executescript(query)
            else:
                logger.info("query: {query}")
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
        """
        Execute a SQL query and return the result as a list of dictionaries.
        This method connects to a database, executes the given SQL query.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            A list of dictionaries representing the query result,
            where the keys are the column names.
        """
        conn, cursor = self.connect()        
        try:
            q_result = cursor.execute(query)
            cols = [item[0] for item in q_result.description]
            rows = q_result.fetchall()
            return [{key: val for key, val in zip(cols, row)} for row in rows]
        except Exception as ex:
            logger.exception(ex)
        finally:
            self.close(conn, cursor)
