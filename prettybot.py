import src
from src.prettybot.jsons import json_getters
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot import bot


def main_():
    bot_database_scripts = database_assistant.Database()
    bot.start_bot(db_scripts=bot_database_scripts, bot_token=json_getters.get_token())
    bot_database_scripts.stop()


if __name__ == '__main__':
    main_()
