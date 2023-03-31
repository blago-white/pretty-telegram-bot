import src
from src.prettybot.json import json_getters
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot import bot


def main_():
    db_settings = json_getters.get_setings_db()
    bot_database_scripts = database_assistant.Database(**db_settings)
    bot.start_bot(db_scripts=bot_database_scripts, bot_token=json_getters.get_token())
    bot_database_scripts.exit()


if __name__ == '__main__':
    main_()
