from apps.base.constants import BaseEnum


class Status(BaseEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class SubStage(BaseEnum):
    ONE_DOT_ONE = 1.1
    ONE_DOT_TWO = 1.2
    ONE_DOT_THREE = 1.3
    ONE_DOT_FOUR = 1.4
