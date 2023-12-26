from pydantic import BaseModel
from fastapi import Body


class LoginRequestSchema(BaseModel):
    """
    登录请求体格式
    """
    
    email: str = Body(regex=r"[\w]+(\.[\w]+)*@[\w]+(\.[\w])+")
    """
    用户邮箱
    """
    
    password: str = Body()
    """
    用户密码 需加密后存储
    """

    verifyCode: str = Body()
    """
    验证码
    """
