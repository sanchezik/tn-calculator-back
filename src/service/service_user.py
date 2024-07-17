from src.db import dao_user
from src.util.const import ERR_MISSING_PARAMS, ERR_USER_NOT_FOUND, ERR_WRONG_PSWD


def login(form):
    result = {
        "errors": None,
        "user": None
    }

    if not form.get("username") or not form.get("password"):
        result["errors"] = ERR_MISSING_PARAMS
        return result

    user = dao_user.get_by_username(form["username"])

    if user is None:
        result["errors"] = ERR_USER_NOT_FOUND
        return result
    if user["password"] != form["password"]:
        result["errors"] = ERR_WRONG_PSWD
        return result

    result["user"] = user
    return result
