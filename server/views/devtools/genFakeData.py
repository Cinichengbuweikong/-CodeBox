from . import router

from models.Users import Users
from constants import ADMIN_PWD

from utils.cryptoTool import hash


@router.post("/genFakeData")
async def index():
    """
    生成伪数据
    """

    # 生成管理员用户
    adminUser = Users(
        username="admin",
        email="admin@codeBox.com",
        password=hash(ADMIN_PWD)
    )

    await adminUser.save()

    return {
        "msg": "ok"
    }
