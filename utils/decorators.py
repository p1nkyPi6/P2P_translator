from functools import wraps

def check_closed(field_name='isClose'):
    """
    Декоратор с параметром — имя свойства для проверки
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, field_name):
                raise ValueError(
                    f"{self.__class__.__name__} must have '{field_name}' attribute to use @check_closed"
                )
            if getattr(self, field_name, False):
                raise RuntimeError(f"Attempt to use a closed {self.__class__.__name__}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator