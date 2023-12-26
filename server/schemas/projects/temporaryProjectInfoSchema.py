from schemas.operationResponseSchema import OpreationResponseSchema


class TemporaryProjectInfoSchema(OpreationResponseSchema):
    tpid: int
    """
    新建的临时工程的项目 id
    """
