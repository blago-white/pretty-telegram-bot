import os
import dotenv

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot import bot


def main_():
    dotenv.main.load_dotenv()
    bot_database_scripts = database_assistant.Database(namedb=os.environ["DB_NAME"],
                                                       password=os.environ["DB_PASSWORD"],
                                                       user=os.environ["DB_USER"])

    bot.start_bot(db_scripts=bot_database_scripts, bot_token=os.environ["TOKEN"])
    bot_database_scripts.exit()


if __name__ == '__main__':
    main_()
