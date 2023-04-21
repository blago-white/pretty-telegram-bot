from typing import Union


class UsersFastFindingBuffer:
    """
    Use the int(UsersFastFindingBuffer) for getting user id, after this
    action received user id will be deleted from buffer
    """

    _BUFFER = list()

    def add_user(self, user_id: int) -> None:
        self._BUFFER.append(int(user_id))

    def get_user(self) -> Union[int, None]:
        try:
            return self._BUFFER.pop(0)
        except IndexError:
            return
