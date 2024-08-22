from main_files.decorator.decorator_func import log_decorator


class User:
    # rent a bike
    @log_decorator
    def rent_bicycle(self):
        pass
