from src.bot.simple.jsons import json_getters
from src.bot.db import database_assistant
from src.bot.telegram import bot


def main():
    scripts = database_assistant.DatabaseScripts()

    bot.start_bot(db_scripts=scripts,
                  bot_token=json_getters.get_token().object)

    scripts.stop()


if __name__ == '__main__':
    main()
