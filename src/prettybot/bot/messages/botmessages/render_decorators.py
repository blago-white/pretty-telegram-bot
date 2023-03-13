from src.prettybot.dataclass import dataclass
from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.db import database_assistant
from src.prettybot.bot.asyncioscripts import delayer

__all__ = ['exception_handler', 'rendering_wrapper']

RENDERER_MAIN_MESSAGES_NAMES = ['render_profile',
                                'render_finding_message',
                                'render_clarify_message',
                                'render_main_message']

RENDERER_DISAPPEAR_MESSAGES_NAMES = ['render_disappearing_message']


def rendering_completer(function):
    async def wrapper(*args, **kwargs):
        renderer_instance = args[0]
        user_id: int = kwargs.get('user_id')
        rendering_result: dict = await function(*args, **kwargs)

        if type(rendering_result) is dict:
            await handle_end_render(user_id=user_id, **rendering_result,
                                    called_function=function,
                                    renderer_instance=renderer_instance)

    return wrapper


async def handle_end_render(
        user_id: int,
        sended_message_id: int,
        called_function,
        renderer_instance,
        retrievable_message_id=None,
        delay_before_deleting=None):
    if called_function.__name__ in RENDERER_MAIN_MESSAGES_NAMES:
        await handle_end_render_main(user_id=user_id,
                                     renderer_instance=renderer_instance,
                                     sended_message_id=sended_message_id)

    elif called_function.__name__ in RENDERER_DISAPPEAR_MESSAGES_NAMES:
        await handle_end_render_disappear(user_id=user_id,
                                          renderer_instance=renderer_instance,
                                          sended_message_id=sended_message_id,
                                          retrievable_message_id=retrievable_message_id,
                                          delay_before_deleting=delay_before_deleting)


async def handle_end_render_main(
        user_id: int,
        sended_message_id: int,
        renderer_instance):
    await renderer_instance.delete_main_message(user_id=user_id)
    renderer_instance.database_operation_assistant.add_main_message_to_db(user_id=user_id, id_message=sended_message_id)


async def handle_end_render_disappear(
        sended_message_id: int,
        retrievable_message_id: int,
        user_id: int,
        delay_before_deleting: int,
        renderer_instance):
    await renderer_instance.message_deleter.delete_message(user_id=user_id, idmes=retrievable_message_id)
    await delayer.start_delay(delay_before_deleting)
    await renderer_instance.message_deleter.delete_message(user_id=user_id, idmes=sended_message_id)
