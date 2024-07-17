from src.db import connector_db
from src.util.const import DB_ACTION_SELECT_ONE


def get_by_id(uid):
    statement = "SELECT * FROM public.user WHERE id = {};".format(uid)
    return connector_db.execute_statement(statement, DB_ACTION_SELECT_ONE)
