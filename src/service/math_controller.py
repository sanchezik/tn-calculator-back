from src.api import random_org
from src.db import dao_operations
from src.util.const import *


def do_math(form, cur_user):
    result = {
        "errors": None,
        "result": None
    }

    if not form.get("operation"):
        result["errors"] = ERR_MISSING_PARAMS
        return result
    operation = dao_operations.get_by_type(form.get("operation"))
    if operation is None:
        result["errors"] = ERR_OP_TYPE
        return result

    # todo validate user's balance
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

    # todo change user's balance and save

    return result
