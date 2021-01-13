
from uuid import uuid4


def get_uuid():
    uuid = str(uuid4()).replace("-", "")
    return uuid
