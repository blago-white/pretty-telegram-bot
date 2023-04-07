from ..config.recording_stages import STAGES_RECORDING, TYPE_RECORDING

TABLES = ('main_messages', 'photos', 'states', 'users', 'users_info', 'users_searching_buffer')

USER_DATA_TABLES = ("users", "states", "users_info", "photos", "users_searching_buffer")

OTHER_TABLES = ("main_messages", )

DEFAULT_RECORD_TYPE = TYPE_RECORDING[0]

DEFAULT_RECORD_STAGE = STAGES_RECORDING[0]

AMOUNT_CITIES = 1138
