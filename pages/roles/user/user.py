from datetime import datetime

from psycopg2 import sql

from main_files.database.db_setting import Database, get_active_user, execute_query
from main_files.decorator.decorator_func import log_decorator


class User:
    def __init__(self):
        self.__database = Database()
        self.__date_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    @log_decorator
    def rent_products(self, product_name: str):
        self.create_rent_table()
        active_user = get_active_user()
        query = sql.SQL('''
        INSERT INTO RENTALS (USER_EMAIL, RENT_PRODUCT)
        VALUES (%s, %s);
        ''')
        params = (active_user['email'], product_name)
        with self.__database as cursor:
            cursor.execute(query, params)

    @log_decorator
    def create_rent_table(self):
        query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS RENTALS (
        ID SERIAL PRIMARY KEY,
        PRODUCT_ID SERIAL UNIQUE,
        USER_EMAIL VARCHAR(255) NOT NULL,
        RENT_PRODUCT VARCHAR(255) NOT NULL,
        RENT_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        STATUS BOOLEAN NOT NULL DEFAULT FALSE
        );
        ''')
        with self.__database as cursor:
            cursor.execute(query)
        return True

    # rent a bike
    @log_decorator
    def rent_bicycle(self):
        self.rent_products(product_name='bicycle')
        print(f"You rented a bike at {self.__date_now}")
        return True

    @log_decorator
    def rent_power_bank(self):
        self.rent_products(product_name='power_bank')
        print(f"You rented a power bank at {self.__date_now}")
        return True

    @log_decorator
    def my_active_rent(self):
        active_user = get_active_user()
        query = '''
        SELECT * FROM RENTALS
        WHERE USER_EMAIL = %s and STATUS = %s;
        '''
        params = (active_user['email'], False)
        all_product = execute_query(query, params, fetch='all')
        print(all_product)
