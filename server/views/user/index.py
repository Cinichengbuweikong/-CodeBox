from typing import Optional
import os

from fastapi import Depends, Form, UploadFile, Body, File, Query
import uuid

from . import router
from depends.userInfoDependence import userInfo
from models.Users import Users
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.users.userInfoResponseSchema import userInfoResponseSchema
from constants import ResopnseOperationResultType, AVATAR_IMG_DIR
from utils.cryptoTool import hash
from utils.getRedisConnect import getRedisConnect


@router.get("/")
async def index(
    user: Users | None = Depends(userInfo),
    uid: Optional[int] | None = Query(default=None)
):
    """
    获取用户信息
    """

    if uid != None:
        targetUser: Users | None = await Users.filter(uid=uid).first()

        if targetUser == None:
            return OpreationResponseSchema(
                code=403,
                result=ResopnseOperationResultType.FAIL,
                reason="user doesn't exists"
            )

        return userInfoResponseSchema(
            uid=str(targetUser.uid),
            username=targetUser.username,
            avatarurl=targetUser.avatarurl,
            coin=targetUser.coin,
            description=targetUser.description,
            email=targetUser.email
        )

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )
    
    return userInfoResponseSchema(
        uid=str(user.uid),
        username=user.username,
        avatarurl=user.avatarurl,
        coin=user.coin,
        description=user.description,
        email=user.email
    )


@router.post("/")
async def modifyUserInfo(
    user: Users = Depends(userInfo),
    username: Optional[str] = Form(default=None),
    password: Optional[str] = Form(default=None),
    avatarimg: Optional[UploadFile] = File(default=None),
    description: Optional[str] = Form(default=None)
):
    """
    修改用户个人信息
    """

    # 检查用户登录了没有
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )
    
    # 修改用户名
    if username != None:
        user.username = username

    # 修改自我介绍
    if description != None:
        user.description = description

    try:
        # 修改密码
        if password != None:
            user.password = hash(password)
        
        # 修改用户头像
        if avatarimg != None and avatarimg.filename != "":
            imgname: str = uuid.uuid1().hex

            imgcontent: bytes = await avatarimg.read()

            if avatarimg.content_type == "image/jpeg":
                imgname = f"{imgname}.jpg"
            elif avatarimg.content_type == "image/png":
                imgname = f"{imgname}.png"

            with open(os.path.join(AVATAR_IMG_DIR, imgname), "wb") as file:
                file.write(imgcontent)

            user.avatarurl = imgname

        await user.save()
    except Exception as e:
        print(e)

        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when saving info"
        )
    
    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.delete("/")
async def destoryUserInfo(
    user: Users | None = Depends(userInfo),
    verifyCode: str = Body(embed=True)
):
    """
    注销用户 即设置此用户的 destory 属性为 true
    同时设置 email 为乱码字符串  也同时设置用户名为乱码
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )

    redisConn = await getRedisConnect()

    async with redisConn.client() as client:
        code = await client.get(user.email)
        await client.delete(user.email)

    if verifyCode != code:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="wrong verifycode"
        )
    
    newusername: str = uuid.uuid1().hex
    newemail: str = f"{uuid.uuid1().hex}@{uuid.uuid1().hex}.com"

    user.username = newusername
    user.email = newemail
    user.destroyed = True
    user.password = ""

    try:
        await user.save()
    except:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when saving info"
        )

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
