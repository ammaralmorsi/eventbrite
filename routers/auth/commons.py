from .db.driver import get_db_conn


def is_unique(email):
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": email})
    if logged_user is not None:
        return False
    return True


