import dataclasses

"""

:param status: | .status - bool: if operation complete : True else : False
:param description: | .description - string: if you need error description or description to result
:param object: | .object - object: if you need return the result

"""


@dataclasses.dataclass(frozen=True, eq=True)
class ResultOperation:
    status: bool = True
    object: object = None
    description: str = None
