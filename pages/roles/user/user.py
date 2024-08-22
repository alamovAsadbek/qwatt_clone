from main_files.decorator.decorator_func import log_decorator


class User:
    @log_decorator
    def create_rent_table(self):
        pass

    # rent a bike
    @log_decorator
    def rent_bicycle(self):
        pass
