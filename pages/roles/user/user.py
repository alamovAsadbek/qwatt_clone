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
        """
                Inserts a new record into the RENTALS table to rent a product.

                :param product_name: The name of the product being rented.
                :param price: The price of the rental.
        """
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
        """
                Creates the RENTALS table in the database if it does not already exist.
                The table is used to store rental records including product ID, rental price, user email, and rental status.
        """
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
        """
                Rents a bicycle and prints a confirmation message with the rental price and current date/time.
        """
        price = 500
        self.rent_products(product_name='bicycle', price=price)
        print(f"You rented a bike at {self.__date_now}, The price for 1 minute is {price} uzs")
        return True

    @log_decorator
    def rent_power_bank(self):
        """
                Rents a power bank by calling the rent_products method with a fixed price.
        """
        price = 200
        self.rent_products(product_name='power_bank', price=price)
        print(f"You rented a power bank at {self.__date_now}, The price for 1 minute is {price} uzs")
        return True

    @log_decorator
    def my_active_rent(self):
        """
               Retrieves and displays all active rental records for the current user.
               Active rentals are those with a STATUS of False.
        """
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
        """
                Retrieves and displays all inactive rental records for the current user.
                Inactive rentals are those with a STATUS of True.
        """
        active_user = get_active_user()
        query = '''
                SELECT * FROM RENTALS
                WHERE USER_EMAIL = %s and STATUS = %s;
        '''
        params = (active_user['email'], True)
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
    def return_rent(self):
        """
                Allows the user to return a rented product by entering the rental ID.
                This method currently only displays active rentals and prompts for a rental ID.
        """
        active_user = get_active_user()
        self.my_active_rent()
        rent_id: int = int(input("Enter rent ID: "))
        query = '''
        SELECT * FROM RENTALS
        WHERE ID = %s AND USER_EMAIL = %s AND STATUS = FALSE;
        '''
        params = (rent_id, active_user['email'])
        select_product = execute_query(query, params, fetch='one')
        if not select_product:
            print("Error choose rent ID")
            return True
        rent_time = select_product['rent_time']
        if isinstance(rent_time, str):
            rent_time = datetime.strptime(rent_time, '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.now()  # Get the current time
        work_time = current_time - rent_time  # Calculate the duration
        minutes_rented = work_time.total_seconds() / 60  # Convert duration to minutes
        minutes_rented = round(minutes_rented)
        price = minutes_rented * select_product['price']
        data = (f"Rent ID: {select_product['id']}\nRent Product: {select_product['rent_product']}\n"
                f"Rental time: {minutes_rented} minutes\nRent money: {price} uzs\n"
                f"Rent Time: {select_product['rent_time'].strftime('%Y-%m-%d %H:%M:%S')} \n"
                f"Status: {'Inactive' if select_product['status'] else 'Active'}\n"
                )
        print(data)
        card_number = int(input("Enter card number: ").strip())
        print(f'{price} uzs were paid from the {card_number} plastic card')
        query = '''UPDATE rentals SET status=%s WHERE id=%s;'''
        params = (True, rent_id)
        with self.__database as cursor:
            cursor.execute(query, params)
        return True

    @log_decorator
    def profile(self):
        """
                Displays or manages user profile information.
                This method is currently a placeholder and does not perform any actions.
        """
        pass
