from src.bot.db.dbconnection import ConnectionsAssistant
from src.bot.simple import dataclass
from src.conf import config


class Execute(ConnectionsAssistant):

    TEMPLATES = config.TEMPLATES

    def complete_transaction(self, *args, number_temp: int):

        if not number_temp:
            return dataclass.ResultOperation(status=False, description='args-error')

        template = self.TEMPLATES[number_temp]
        template = template.format(*args)

        response = self.execute_query_(sqlquery=template)

        if not response.status:
            return dataclass.ResultOperation(status=False, description='DB error')

        return dataclass.ResultOperation(status=True, object=response.object)

