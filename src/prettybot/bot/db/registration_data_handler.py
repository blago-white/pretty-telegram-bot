import psycopg2

from src.prettybot.dataclass import dataclass
from src.prettybot.bot.db import database_assistant
from src.prettybot.scripts import auxiliary
from src.conf.recording_stages import *


class RegistrationDataHandler:

    _database_operation_assistant: database_assistant.DatabaseScripts

    def __init__(self, database_operation_assistant):
        self._database_operation_assistant = database_operation_assistant

    def record_registration_data(
            self,
            message_text: str,
            user_id: int,
            logtype: int,
            logstage: int,
            updating_data=False):

        if logstage != PHOTO_STAGE:
            if logstage != SEX_STAGE:
                self._database_operation_assistant.record_user_param(
                    user_id=user_id,
                    name=NAME_COLUMN_BY_LOGSTAGE[logstage],
                    value="'{}'".format(
                        message_text.replace("'", "''").replace("/", "")
                        if type(message_text) == str else message_text
                    ))

            if logstage in WISHES_COLUMNS:
                if logstage == AGE_STAGE:

                    start_range, stop_range = 0, 0

                    if logtype in TYPE_RECORDING[:2]:
                        start_range = int(message_text) - 5
                        stop_range = int(message_text) + 5

                        if start_range < LOWER_AGE_LIMIT:
                            start_range = LOWER_AGE_LIMIT

                        elif stop_range < LOWER_AGE_LIMIT:
                            stop_range = UPPER_AGE_LIMIT

                    elif logtype == TYPE_RECORDING[2]:
                        age_digits = [i for i in message_text if i.isdigit()][:4]
                        start_range, stop_range = int(''.join(age_digits[:2])), int(''.join(age_digits[2:]))

                    self._database_operation_assistant.record_user_param(
                        user_id=user_id,
                        name='age_wish',
                        value="'{}'::int4range".format(
                            psycopg2.extras.NumericRange(lower=start_range, upper=stop_range, bounds='[]')
                        )
                    )

                    return

                if logstage == CITY_STAGE:
                    message_text = "'" + message_text + "'"

                self._database_operation_assistant.record_user_param(
                    user_id=user_id,
                    name=NAME_COLUMN_BY_LOGSTAGE[logstage] + '_wish',
                    value=message_text
                )

        elif logstage == PHOTO_STAGE:

            try:
                response = self._database_operation_assistant.save_photo(user_id=user_id, file_id=str(message_text),
                                                                         upd=updating_data)

            except TypeError:
                return dataclass.ResultOperation(status=False,
                                                 description='not correct doc - id')

            if type(response) is BaseException:
                return dataclass.ResultOperation(status=False, description='not correct doc - id')

        return dataclass.ResultOperation()
