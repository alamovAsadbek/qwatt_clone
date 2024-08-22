import psycopg2

from main_files.database.config import config
from main_files.decorator.decorator_func import log_decorator


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        print(config())

    def __enter__(self):
        self.connection = psycopg2.connect(**config())
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.connection.rollback()
        else:
            self.connection.commit()

        if self.connection is not None:
            self.connection.close()

        if self.cursor is not None:
            self.cursor.close()

    @log_decorator
    def execute(self, query, params=None):
        """execute the query(INSERT, UPDATE, DELETE)"""
        self.cursor.execute(query, params)
        self.connection.commit()

    @log_decorator
    def fetchall(self, query, params=None):
        """fetch many row from the database"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    @log_decorator
    def fetchone(self, query, params=None):
        """fetch only one row from the database"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()


@log_decorator
def execute_query(query, params=None, fetch=None):
    try:
        with Database() as db:
            if fetch == "all":
                return db.fetchall(query, params)
            elif fetch == "one":
                return db.fetchone(query, params)
            else:
                db.execute(query, params)
    except Exception as e:
        print(f"Exception occurred while executing: {e}")
