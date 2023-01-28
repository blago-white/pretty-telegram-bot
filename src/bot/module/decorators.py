from src.bot.bin import dataclass


def trying(on_exception: str = None):
    """

    :param on_exception: string, return if raised exception

    """

    def wrapper(function):

        def wrapper_(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                return dataclass.ResultOperation(status=False, desc=on_exception if on_exception else e)

        return wrapper_

    return wrapper
