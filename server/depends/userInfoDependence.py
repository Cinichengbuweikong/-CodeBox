from typing import Optional

from fastapi import Cookie
from models.Users import Users
from jose import jwt

from constants import SALT


async def userInfo(
    token: Optional[str] = Cookie(default=None)
) -> Users | None:
    if not token:
        return None
    
    try:
        data = jwt.decode(token, SALT, "HS256")
    except:
        return None
    
    targetUser: Users | None = await Users.filter(uid=data["uid"]).first()

    if not targetUser:
        return None
    
    return targetUser

