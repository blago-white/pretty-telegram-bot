import os
import dotenv

from src import bot


def main():
    dotenv.main.load_dotenv()
    bot_database_assistant = bot.dbassistant.database_assistant.BotDatabase(namedb=os.environ["DB_NAME"],
                                                                            password=os.environ["DB_PASSWORD"],
                                                                            user=os.environ["DB_USER"])

    bot.start_bot(bot_database_assistant=bot_database_assistant, bot_token=os.environ["TOKEN"])
    bot_database_assistant.exit()


if __name__ == '__main__':
    main()
