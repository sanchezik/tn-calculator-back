from src.db import connector_db
from src.util.const import DB_ACTION_INS_UPD_DEL


def create(operation_id, user_id, amount, user_balance, operation_response):
    statement = "INSERT INTO public.record(operation_id, user_id, amount, user_balance, operation_response) " \
                "VALUES ({},{},{},{},'{}');".format(operation_id, user_id, amount, user_balance, operation_response)
    return connector_db.execute_statement(statement, DB_ACTION_INS_UPD_DEL)
