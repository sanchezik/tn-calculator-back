from src.db import dao_user, dao_record, dao_operation
from src.util.const import ERR_MISSING_PARAMS, ERR_USER_NOT_FOUND, ERR_WRONG_PSWD


def login(form):
    result = {
        "errors": None,
        "user": None
    }

    if not form.get("username") or not form.get("password"):
        result["errors"] = ERR_MISSING_PARAMS
        return result

    print('debug: requesting from DB')
    user = dao_user.get_by_username(form["username"])
    print('debug: received: ' + str(user))

    if user is None:
        result["errors"] = ERR_USER_NOT_FOUND
        return result
    if user["password"] != form["password"]:
        result["errors"] = ERR_WRONG_PSWD
        return result

    result["user"] = user
    return result


def get_records(form, uid):
    result = {
        "errors": None,
        "records": []
    }

    sorting_column = form["sort_col"] if form.get("sort_col") else "date"
    page_size = int(form["page_size"]) if form.get("page_size") else 20
    offset = (int(form["page_num"]) - 1) * page_size if form.get("page_num") else 0

    records = dao_record.get(uid, sorting_column, page_size, offset)
    for r in records:
        r["operation"] = dao_operation.get_by_id(r["operation_id"])
    result["records"] = records

    return result
