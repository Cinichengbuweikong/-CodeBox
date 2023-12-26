import datetime

from jose import jwt
from fastapi.responses import JSONResponse

from . import server
from models.Users import Users
from utils.cryptoTool import hash
from utils.getRedisConnect import getRedisConnect
from constants import ResopnseOperationResultType, SALT
from schemas.login.loginRequestSchema import LoginRequestSchema
from schemas.operationResponseSchema import OpreationResponseSchema


@server.post("/login", response_model=OpreationResponseSchema)
async def index(
    userInfo: LoginRequestSchema
):
    targetUser: Users | None = await Users.filter(email=userInfo.email).first()

    # 存在这个用户吗?
    if not targetUser:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="user not found"
        )
    
    # 密码对吗?
    if targetUser.password != hash(userInfo.password):
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="wrong password"
        )
    
    # 验证码对吗?
    redisConn = await getRedisConnect()

    async with redisConn.client() as client:
        verifyCode = await client.get(userInfo.email)

        if userInfo.verifyCode != verifyCode:
            return OpreationResponseSchema(
                code=403,
                result=ResopnseOperationResultType.FAIL,
                reason="wrong verifyCode"
            )
        
        # 删除验证码
        await client.delete(userInfo.email)

    
    # 邮箱正确 密码正确 验证码正确 可以发放 token 了
    expireTime: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=15)

    data = {
        "uid": targetUser.uid,
        "exp": expireTime
    }

    token = jwt.encode(data, SALT, algorithm="HS256")

    response = JSONResponse(content=OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    ).model_dump())

    response.set_cookie(
        "token",
        token,
        expires = expireTime.strftime("%Y/%m/%d"),
        httponly=True,
        samesite="lax",
    )

    return response
