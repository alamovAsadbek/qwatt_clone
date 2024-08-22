from main_files.database.db_setting import Database
from main_files.decorator.decorator_func import log_decorator


class User:
    def __init__(self):
        self.__database = Database()

    @log_decorator
    def create_rent_table(self):
        query='''
        CREATE TABLE IF NOT EXISTS RENTALS (
        ID SERIAL PRIMARY KEY,
        FIRSTNAME VARCHAR(255) NOT NULL,
        LASTNAME VARCHAR(255) NOT NULL,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        PASSWORD VARCHAR(256) NOT NULL,
        IS_LOGIN BOOLEAN DEFAULT FALSE,
        CREATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
        with self.__database as cursor:
            cursor.execute(query)
        return True

    # rent a bike
    @log_decorator
    def rent_bicycle(self):
        pass
