import time

from src.api import random_org
from src.db import dao_operation, dao_record
from src.util.const import *


def do_math(form, session):
    result = {
        "errors": None,
        "result": None
    }

    # validations
    if not form.get("operation"):
        result["errors"] = ERR_MISSING_PARAMS
        return result
    operation = dao_operation.get_by_type(form.get("operation"))
    if operation is None:
        result["errors"] = ERR_OP_TYPE
        return result

    # check operation cost
    if session['limit'] - operation["cost"] < 0 and time.time() < session['limit_renewal']:
        result["errors"] = ERR_REQUESTS_LIMIT + str(int(session['limit_renewal'] - time.time())) + " sec"
        return result

    # validations
    if (operation["type"] in [OPR_ADD, OPR_SBTR, OPR_MLTP, OPR_DIV] and (
            not form.get("param1") or not form.get("param2"))) or (
            operation["type"] == OPR_SQR and not form.get("param1")):
        result["errors"] = ERR_MISSING_PARAMS
        return result

    param1 = None
    param2 = None
    try:
        if form.get("param1"):
            param1 = int(form.get("param1"))
        if form.get("param2"):
            param2 = int(form.get("param2"))
    except ValueError:
        result["errors"] = ERR_INVALID_DATA
        return result

    if operation["type"] == OPR_ADD:
        result["result"] = param1 + param2
    elif operation["type"] == OPR_SBTR:
        result["result"] = param1 - param2
    elif operation["type"] == OPR_MLTP:
        result["result"] = param1 * param2
    elif operation["type"] == OPR_DIV:
        try:
            result["result"] = param1 / param2
        except ZeroDivisionError as error:
            result["errors"] = str(error)
    elif operation["type"] == OPR_SQR:
        result["result"] = param1 * param1
    elif operation["type"] == OPR_RND:
        random_str = random_org.generate_string()
        if random_str:
            result["result"] = random_str
        else:
            result["errors"] = ERR_REQ_RAND
    else:
        result["errors"] = ERR_OP_TYPE
        return result

    # change user balance
    if time.time() >= session['limit_renewal']:
        session['limit'] = 20
        session['limit_renewal'] = time.time() + 60
    session['limit'] = session['limit'] - operation["cost"]

    dao_record.create(operation["id"], session["user"]["id"], operation["cost"], session['limit'],
                      str(result["result"]))

    return result
