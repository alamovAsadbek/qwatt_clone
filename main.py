from main_files.decorator.decorator_func import log_decorator
from pages.page.auth import Auth


@log_decorator
def auth_menu():
    text = '''
1. Register 
2. Login
3. Logout
    '''
    print(text)
    try:
        auth = Auth()
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            auth.register()
            auth_menu()
        elif user_input == 2:
            if auth.login():
                user_menu()
            else:
                auth_menu()
        elif user_input == 3:
            auth.logout()
            print("Logged out")
            return
        else:
            print("Invalid input")
            auth_menu()
    except Exception as e:
        print(f'Error: {e}')
        auth_menu()


@log_decorator
def user_menu():
    text = '''
1. Bicycle rental
2. Power bank rental
3. My active rents
4. My inactive rents
5. Profile
6. Logout
    '''
    print(text)
    try:
        user_input: int = int(input("Choose menu: "))
        if user_input == 1:
            pass
        elif user_input == 2:
            pass
        elif user_input == 3:
            pass
        elif user_input == 4:
            pass
        elif user_input == 5:
            pass
        elif user_input == 6:
            pass

    except Exception as e:
        print(f'Error: {e}')
        user_menu()


if __name__ == '__main__':
    auth_menu()
