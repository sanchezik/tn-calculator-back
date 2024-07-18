from src.db import connector_db
from src.util.const import DB_ACTION_INS_UPD_DEL, DB_ACTION_SELECT_MANY


def create(operation_id, user_id, amount, user_balance, operation_response):
    statement = "INSERT INTO public.record(operation_id, user_id, amount, user_balance, operation_response) " \
                "VALUES ({},{},{},{},'{}');".format(operation_id, user_id, amount, user_balance, operation_response)
    return connector_db.execute_statement(statement, DB_ACTION_INS_UPD_DEL)


def get(uid, sorting_column="date", page_size=20, offset=0):
    statement = ("SELECT * FROM public.record WHERE user_id = {} ORDER BY {} LIMIT {} OFFSET {};"
                 "").format(uid, sorting_column, page_size, offset)
    return connector_db.execute_statement(statement, DB_ACTION_SELECT_MANY)
