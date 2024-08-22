from psycopg2 import sql

from main_files.database.db_setting import Database
from main_files.decorator.decorator_func import log_decorator


class User:
    def __init__(self):
        self.__database = Database()

    @log_decorator
    def create_rent_table(self):
        query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS RENTALS (
        ID SERIAL PRIMARY KEY,
        PRODUCT_ID SERIAL UNIQUE,
        USER_EMAIL VARCHAR(255) NOT NULL,
        RENT_PRODUCT VARCHAR(255) NOT NULL,
        RENT_TIME DEFAULT CURRENT_TIMESTAMP,
        STATUS BOOLEN NOT NULL DEFAULT FALSE,
        );
        ''')
        with self.__database as cursor:
            cursor.execute(query)
        return True

    # rent a bike
    @log_decorator
    def rent_bicycle(self):
        self.create_rent_table()

