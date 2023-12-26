from typing import List

from . import server
from utils.getRedisConnect import getRedisConnect
from utils.cryptoTool import hash
from constants import ResopnseOperationResultType
from schemas.signup.signupRequestSchema import SignupRequestSchema
from schemas.operationResponseSchema import OpreationResponseSchema
from models.Users import Users


@server.post(
    "/signup",
    response_model=OpreationResponseSchema
)
async def index(
    userInfo: SignupRequestSchema
):
    # 检查验证码
    redisConn = await getRedisConnect()

    async with redisConn.client() as client:
        verifyCode = await client.get(userInfo.email)
    
    if userInfo.verifyCode != verifyCode:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="wrong verifyCode" 
        )
    

    # 检查名字是否重复
    currentUser: Users | None = await Users.filter(username=userInfo.username).first()

    if currentUser != None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="duplicate name" 
        )
    
    currentUser = await Users.filter(email=userInfo.email).first()

    if currentUser != None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user already registered" 
        )

    
    # 都通过后即可储存用户信息
    email = userInfo.email
    password = hash(userInfo.password)

    newUser = Users(
        username=userInfo.username,
        email=email,
        password=password
    )

    await newUser.save()


    # 删除 redis 中存储的验证码
    async with redisConn.client() as client:
        verifyCode = await client.delete(userInfo.email)

    
    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
