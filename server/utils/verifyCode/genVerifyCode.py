import random
from typing import List


def genVerifyCode() -> str:
    """
    生成验证码
    """

    charStr: str = \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

    verifyCodeList: List[str] = []

    for i in range(6):
        index = random.randint(0, len(charStr)-1)
        verifyCodeList.append(charStr[index])

    verifyCode: str = "".join(verifyCodeList)

    return verifyCode
