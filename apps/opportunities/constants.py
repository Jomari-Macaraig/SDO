from apps.base.constants import BaseEnum


class Stage(BaseEnum):
    INITIAL = "INITIAL"
    SCOPING = "SCOPING"
    BID = "BID"
    PROJECT = "PROJECT"
    OPERATIONS = "OPERATIONS"


class DocumentType(BaseEnum):
    SERVICE_DELIVERY_OUTPUT = "SERVICE_DELIVERY_OUTPUT"
    STATEMENT_OF_WORK = "STATEMENT_OF_WORK"
