from src.bot.bin import dataclass
import aiogram


def trying(on_exception: str = None):
    """

    :param on_exception: string, return if raised exception

    """

    def wrapper(function):

        def wrapper_(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                return dataclass.ResultOperation(status=False, description=on_exception if on_exception else e)

        return wrapper_

    return wrapper


def unpack_message(handler_func):
    async def wrapper(*args):
        message: aiogram.types.Message

        cls_instance, message = args
        id_user = message.from_user.id

        if message.chat.type == 'private':
            await handler_func(cls_instance, message, id_user)

    return wrapper
