from src.bot.simple.jsons import json_writers, json_getters
import src.bot.db.dbscripts as dbscripts
from src.bot.telegram import mainbot


def main():
    json_writers.write_settings_db(debug=False)

    scripts = dbscripts.Database()

    mainbot.start_bot(db_scripts=scripts,
                      bot_token=json_getters.get_token().object)

    scripts.stop_working()


if __name__ == '__main__':
    main()
