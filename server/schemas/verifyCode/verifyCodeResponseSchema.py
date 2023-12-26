from schemas.operationResponseSchema import OpreationResponseSchema


class verifyCodeResponseSchema(OpreationResponseSchema):
    verifyCode: str
    """
    验证码
    """
