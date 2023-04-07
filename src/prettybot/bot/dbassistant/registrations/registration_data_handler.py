from typing import Union, Callable

from . import _age_range_creator
from . import _value_converter

from src.prettybot.bot.dbassistant import database_assistant
from src.config.recording_stages import *


class RegistrationParamsHandler:
    _database_operation_assistant: database_assistant.Database

    def __init__(self, database_operation_assistant: database_assistant.Database) -> None:
        self._database_operation_assistant = database_operation_assistant

    def _get_photo_saving_method(self, record_type: str) -> Union[Callable[[int, str], None], ValueError]:
        """
        :param record_type: type of user recording
        :returns: ValueError if there is no such type in the config else - required method
        """

        if record_type in RECORDING_TYPES_WITH_SAVING_USER_PHOTO:
            return self._database_operation_assistant.save_photo_id

        elif record_type in RECORDING_TYPES_WITH_UPDATING_USER_PHOTO:
            return self._database_operation_assistant.update_photo_id

        return ValueError

    def _save_user_photo(self, user_id: int, file_id: str, record_type: str) -> None:
        saving_method = self._get_photo_saving_method(record_type=record_type)
        if callable(saving_method):
            saving_method(int(user_id), str(file_id))

    def record_user_param(
            self, message_payload: Union[str, int],
            user_id: int,
            record_type: int,
            record_stage: int) -> None:

        if record_stage == PHOTO_STAGE:
            return self._save_user_photo(user_id=user_id, file_id=message_payload, record_type=record_type)

        column_value = _value_converter.convert_user_param_value(user_value=message_payload, record_strage=record_stage)

        if record_type != TYPE_RECORDING[2]:
            self._database_operation_assistant.record_user_searching_param(user_id=user_id,
                                                                           name_param=NAME_COLUMN_BY_LOGSTAGE[
                                                                               record_stage],
                                                                           value_param=column_value)

        if record_stage in SEARCH_PARAM_COLUMNS:
            if record_stage == AGE_STAGE:
                column_value = _age_range_creator.get_age_range_for_db(
                    *_age_range_creator.get_age_range_limits(message_payload=message_payload,
                                                             recording_type=record_type).values()
                )

            self._database_operation_assistant.record_user_searching_param(user_id=user_id,
                                                                           name_param=NAME_WISH_COLUMN_BY_LOGSTAGE[
                                                                               record_stage],
                                                                           value_param=column_value
                                                                           )
