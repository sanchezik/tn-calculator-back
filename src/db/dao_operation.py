from src.db import connector_db
from src.util.const import DB_ACTION_SELECT_ONE, DB_ACTION_SELECT_MANY


def get_all():
    statement = "SELECT * FROM public.operation;"
    return connector_db.execute_statement(statement, DB_ACTION_SELECT_MANY)


def get_by_id(op_id):
    statement = "SELECT * FROM public.operation WHERE id = {};".format(op_id)
    return connector_db.execute_statement(statement, DB_ACTION_SELECT_ONE)


def get_by_type(op_type):
    statement = "SELECT * FROM public.operation WHERE type = '{}';".format(op_type)
    return connector_db.execute_statement(statement, DB_ACTION_SELECT_ONE)
