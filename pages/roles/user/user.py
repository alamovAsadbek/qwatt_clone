from datetime import datetime

from psycopg2 import sql

from main_files.database.db_setting import Database, get_active_user, execute_query
from main_files.decorator.decorator_func import log_decorator


class User:
    def __init__(self):
        self.__database = Database()
        self.__date_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.create_rent_table()

    @log_decorator
    def rent_products(self, product_name: str, price: int):
        self.create_rent_table()
        active_user = get_active_user()
        query = sql.SQL('''
        INSERT INTO RENTALS (PRICE, USER_EMAIL, RENT_PRODUCT)
        VALUES (%s, %s, %s);
        ''')
        params = (price, active_user['email'], product_name)
        with self.__database as cursor:
            cursor.execute(query, params)

    @log_decorator
    def create_rent_table(self):
        query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS RENTALS (
        ID SERIAL PRIMARY KEY,
        PRODUCT_ID SERIAL UNIQUE,
        PRICE BIGINT NOT NULL,
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
        price = 500
        self.rent_products(product_name='bicycle', price=price)
        print(f"You rented a bike at {self.__date_now}, The price for 1 minute is {price} uzs")
        return True

    @log_decorator
    def rent_power_bank(self):
        price = 200
        self.rent_products(product_name='power_bank', price=price)
        print(f"You rented a power bank at {self.__date_now}, The price for 1 minute is {price} uzs")
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
        if not all_product:
            print(f"You have no rent yet")
            return True
        for product in all_product:
            data = (f"Rent ID: {product['id']}\nRent Product: {product['rent_product']}\n"
                    f"Rent Time: {product['rent_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Status: {'Inactive' if product['status'] else 'Active'}\n"
                    )
            print(data)

        return True

    @log_decorator
    def my_inactive_rent(self):
        pass
