from schemas.operationResponseSchema import OpreationResponseSchema


class CreateProjectResponseSchema(OpreationResponseSchema):
    pid: int
    """
    新建的项目的 id
    """
