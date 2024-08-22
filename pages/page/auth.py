from main_files.decorator.decorator_func import log_decorator


class Auth:
    @log_decorator
    def login(self):
        pass

    @log_decorator
    def register(self):
        pass

    @log_decorator
    def logout(self):
        pass
