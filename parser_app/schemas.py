import faust


class CategoryParam(faust.Record):
    q: str


class UUIDParam(faust.Record):
    _uuid: str
