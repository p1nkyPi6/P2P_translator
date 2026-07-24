import inspect
from functools import wraps


def check_closed(field_name='isClose'):
    """
    Запрещает вызов метода, если объект уже «закрыт» (на основе состояния указанного флага - параметра).
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

def validate_types(**expected_types):
    '''
    Проверяет соответствие типов переданных аргументов заданным эталонам перед выполнением функции.
    Выбрасывает TypeError при обнаружении несоответствия.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_arguments = inspect.signature(func).bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            for arg_name, arg_value in bound_arguments.arguments.items():
                if arg_value is None:
                    raise TypeError("data cannot be None")
                
                if arg_name in expected_types:
                    expected_type = expected_types[arg_name]

                    if not isinstance(arg_value, expected_type):
                        raise TypeError(
                            f"'{arg_name}' must be {expected_type.__name__}, "
                            f"got {type(arg_value).__name__}."
                        )

            return func(*args, **kwargs)     
        return wrapper
    return decorator