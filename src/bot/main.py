
import os
import sys

from src.bot.bin.jsons import json_getters
from src.bot.bin.jsons import json_writers
import src.bot.db.dbscripts as dbscripts
from src.bot.tgapi import aiohandlers


def main():
    json_writers.write_settings_db(debug=False)

    scripts = dbscripts.Database()

    aiohandlers.start_bot(backend_scripts=scripts,
                          bot_token=json_getters.get_token().object)

    scripts.stop_working()


if __name__ == '__main__':
    main()
