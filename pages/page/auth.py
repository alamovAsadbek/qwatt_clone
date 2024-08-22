import datetime
import hashlib

from psycopg2 import sql

from main_files.database.db_setting import Database, execute_query
from main_files.decorator.decorator_func import log_decorator


class Auth:
    def __init__(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__()
        self.__database = Database()

    @log_decorator
    def login(self):
        pass

    @log_decorator
    def register(self):
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier('users'))
        print(execute_query(query, fetch='all'))
        print("Table created successfully")
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
