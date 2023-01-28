from src.bot.db.dbconnection import Connections
from src.bot.bin import dataclass
from src.bot.bin.jsons import json_getters


class Execute(Connections):

    TEMPLATES: dict[str] = json_getters.get_all_templates().object

    def complete_transaction(self, *args, number_temp: int, template: str = None):

        if not template and not number_temp:
            return dataclass.ResultOperation(status=False, desc='args-error')

        if not template:
            template = self.TEMPLATES[str(number_temp)]
            template = template.format(*args)

        response = self.execute_query_(sqlquery=template)

        if not response.status:
            return dataclass.ResultOperation(status=False, desc='DB error')

        return dataclass.ResultOperation(status=True, obj=response.object)

