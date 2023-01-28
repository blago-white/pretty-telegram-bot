from dataclasses import dataclass


@dataclass
class ResultOperation(object):
    """

    :param status: | .status - bool: if operation complete : True else : False
    :param desc: | .description - string: if you need error description or description to result
    :param obj: | .object - object: if you need return the result

    """

    __isfrozen = False

    def __init__(
            self,
            status: bool = True,
            desc: str = None,
            obj: object = None):

        self.status = bool(status)
        self.object = obj
        self.description = desc

        self._frozening()

    def __getattr__(self, item_):
        if not callable(item_):
            for item_para in list(self.__dict__.items()):
                if item_para[0] == item_:
                    return item_para[1]

    def __setattr__(self, key, value):
        if not self.__isfrozen or key in dict(self.__dict__.items()).keys():
            object.__setattr__(self, key, value)

    def _frozening(self):
        self.__isfrozen = True
