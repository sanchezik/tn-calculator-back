import psycopg2
from psycopg2 import extras

from src.util.const import *
from src.util.config import *


def execute_statement(statement, action):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(statement)

        if action == DB_ACTION_SELECT_ONE:
            result = cursor.fetchone()
            cursor.close()
            return result
        elif action == DB_ACTION_SELECT_MANY:
            result = cursor.fetchall()
            cursor.close()
            return result
        elif action == DB_ACTION_INS_UPD_DEL:
            connection.commit()
            cursor.close()
            return RESULT_OK
        else:
            return RESULT_ERROR

    except Exception as error:
        return RESULT_ERROR
    finally:
        if connection:
            connection.close()
