import datetime
import hashlib

from main_files.database.db_setting import Database
from main_files.decorator.decorator_func import log_decorator


class Auth:
    def __init__(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__()
        self.__database = Database()
        create_table_query = '''
                CREATE TABLE IF NOT EXISTS %s (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(256) NOT NULL,
                last_name VARCHAR(256) NOT NULL,
                email VARCHAR(256) NOT NULL UNIQUE,
                password VARCHAR(256) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                );
                '''
        self.__database.execute(create_table_query, ('users',))

    @log_decorator
    def login(self):
        pass

    @log_decorator
    def register(self):
        first_name: str = input("First Name: ")
        last_name: str = input("Last Name: ")
        email: str = input("Email: ")
        password: str = hashlib.md5(input("Password: ").strip().encode('utf-8')).hexdigest()
        confirm_password: str = hashlib.md5(input("Confirm password: ").strip().encode('utf-8')).hexdigest()
        while password != confirm_password:
            print("Passwords do not match")
            password: str = hashlib.md5(input("Password: ").strip().encode('utf-8')).hexdigest()
            confirm_password: str = hashlib.md5(input("Confirm password: ").strip().encode('utf-8')).hexdigest()

    @log_decorator
    def logout(self):
        pass
