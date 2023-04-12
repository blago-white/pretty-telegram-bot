import dbsettings
import bottoken
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot import bot


def main_():
    bot_database_scripts = database_assistant.Database(namedb=dbsettings.namedb,
                                                       password=dbsettings.password,
                                                       user=dbsettings.user)

    bot.start_bot(db_scripts=bot_database_scripts, bot_token=bottoken.token)
    bot_database_scripts.exit()


if __name__ == '__main__':
    main_()
