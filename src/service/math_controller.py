from src.db import dao_operations
from src.util.const import *


def do_math(data, cur_user):
    result = {
        "errors": None,
        "result": None
    }

    if not data.get("operation"):
        result["errors"] = ERR_MISSING_PARAMS
        return result
    operation = dao_operations.get_by_type(data.get("operation"))
    if operation is None:
        result["errors"] = ERR_OP_TYPE
        return result

    # todo validate user's balance
    if (operation["type"] in [OPR_ADD, OPR_SBTR, OPR_MLTP, OPR_DIV] and (
            not data.get("param1") or not data.get("param2"))) or (operation["type"] == OPR_SQR and data.get("param1")):
        result["errors"] = ERR_MISSING_PARAMS
        return result

    if operation["type"] == OPR_ADD:
        param1 = int(data.get("param1"))
        param2 = int(data.get("param2"))
        result["result"] = param1 + param2
    elif operation["type"] == OPR_SBTR:
        param1 = int(data.get("param1"))
        param2 = int(data.get("param2"))
        result["result"] = param1 - param2
    elif operation["type"] == OPR_MLTP:
        param1 = int(data.get("param1"))
        param2 = int(data.get("param2"))
        result["result"] = param1 * param2
    elif operation["type"] == OPR_DIV:
        param1 = int(data.get("param1"))
        param2 = int(data.get("param2"))
        result["result"] = param1 / param2
    elif operation["type"] == OPR_SQR:
        param1 = int(data.get("param1"))
        result["result"] = param1 * param1
    elif operation["type"] == OPR_RND:
        # TODO
        pass
    else:
        result["errors"] = ERR_OP_TYPE
        return result

    # todo change user's balance and save

    return result
