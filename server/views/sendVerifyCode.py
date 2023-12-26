from email.message import EmailMessage

# import aiosmtplib

from . import server
from utils.verifyCode.genVerifyCode import genVerifyCode
from utils.getRedisConnect import getRedisConnect
from constants import ResopnseOperationResultType, IMAP_PWD, EMAIL_ADDR, EMAIL_CONTENT
from schemas.verifyCode.verifyCodeRequestSchema import VerifyCodeRequestSchema
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.verifyCode.verifyCodeResponseSchema import verifyCodeResponseSchema
from models.Users import Users


@server.post("/sendVerifyCode")
async def index(
    info: VerifyCodeRequestSchema
):
    if info.email == None and info.uid == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="both email and uid are none"
        )


    redisConn = await getRedisConnect()

    verifyCode = genVerifyCode()

    targetEmail = info.email

    if info.uid != None:
        targetUser: Users | None = await Users.filter(uid=info.uid).first()

        if targetUser != None:
            targetEmail = targetUser.email

    async with redisConn.client() as client:
        await client.set(targetEmail, verifyCode, ex=60)  # type: ignore


    # 在此处设置发送邮件
    # email: EmailMessage = EmailMessage()
    # email["From"] = EMAIL_ADDR
    # email["To"] = targetEmail
    # email.set_content(EMAIL_CONTENT.format(verifyCode))

    # try:
    #     async with aiosmtplib.SMTP(
    #         hostname="smtp.126.com",
    #         port=465,
    #         username=EMAIL_ADDR, 
    #         password=IMAP_PWD,
    #         use_tls=True
    #     ) as smtpClient:
    #         await smtpClient.send_message(email)

    # except Exception as e:
    #     print("error when sending email: ", e)

    # print(f"/sendVerifyCode: {targetEmail} are {verifyCode}")

    return verifyCodeResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason="",
        verifyCode=verifyCode
    )
