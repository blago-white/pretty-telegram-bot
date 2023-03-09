from src.prettybot.jsons import json_getters
from src.prettybot.bot.db import database_assistant
from src.prettybot.bot import main


def main_():
    scripts = database_assistant.Database()
    main.start_bot(db_scripts=scripts, bot_token=json_getters.get_token())
    scripts.stop()


if __name__ == '__main__':
    main_()
