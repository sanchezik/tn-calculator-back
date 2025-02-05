from src.db import dao_user, dao_record, dao_operation
from src.util.const import ERR_MISSING_PARAMS, ERR_USER_NOT_FOUND, ERR_WRONG_PSWD, ERR_ACCESS_DENIED, \
    ERR_RECORD_NOT_FOUND


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


def get_records(form, uid):
    result = {
        "errors": None,
        "records": [],
        "pageNumber": None,
        "pageSize": None,
        "totalRecords": None,
        "sortColumn": None
    }

    sorting_column = form["sort_col"] if form.get("sort_col") else "date"
    page_size = int(form["page_size"]) if form.get("page_size") else 20
    offset = (int(form["page_num"]) - 1) * page_size if form.get("page_num") else 0

    records = dao_record.get(uid, sorting_column, page_size, offset)
    for r in records:
        r["operation"] = dao_operation.get_by_id(r["operation_id"])
    result["records"] = records
    result["pageNumber"] = int(form["page_num"]) if form.get("page_num") else 1
    result["pageSize"] = page_size
    result["totalRecords"] = dao_record.get_records_count(uid)['count']
    result["sortColumn"] = sorting_column

    return result


def delete_record(record_id, uid):
    result = {
        "errors": None
    }

    record = dao_record.get_by_id(record_id)
    if record is None:
        result["errors"] = ERR_RECORD_NOT_FOUND
        return result
    if record["user_id"] != uid:
        result["errors"] = ERR_ACCESS_DENIED
        return result
    dao_record.remove(record_id)

    return result
