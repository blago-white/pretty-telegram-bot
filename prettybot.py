import os
import dotenv

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot import bot


def main_():
    dotenv.main.load_dotenv()
    bot_database_assistant = database_assistant.BotDatabase(namedb=os.environ["DB_NAME"],
                                                            password=os.environ["DB_PASSWORD"],
                                                            user=os.environ["DB_USER"])

    bot.start_bot(bot_database_assistant=bot_database_assistant, bot_token=os.environ["TOKEN"])
    bot_database_assistant.exit()


if __name__ == '__main__':
    main_()
