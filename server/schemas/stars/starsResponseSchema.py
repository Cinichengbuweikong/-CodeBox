from schemas.operationResponseSchema import OpreationResponseSchema


class StarsResponseSchema(OpreationResponseSchema):
    """
    用于在 /stars 接口中表示 "查询某个项目是否被当前用户收藏了" 的响应体
    """

    star: bool
    """
    用户是否收藏了此项目
    """
