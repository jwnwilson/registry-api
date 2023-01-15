class DBError(Exception):
    pass


class RecordNotFound(DBError):
    pass


class DuplicateRecord(DBError):
    pass
