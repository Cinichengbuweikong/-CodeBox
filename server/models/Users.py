from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class Users(Model):
    """
    用户表
    """

    uid: Field[int] = fields.IntField(pk=True, index=True)
    """
    用户 id  是用户表的主键 也是用户的身份唯一标识
    """
    
    username: Field[str] = fields.CharField(max_length=64, unique=True)
    """
    用户名
    """

    email: Field[str] = fields.CharField(max_length=128, unique=True)
    """
    用户邮箱 应加密后再存储
    """

    password: Field[str] = fields.CharField(max_length=256)
    """
    用户密码 应加盐哈希后再存储
    """

    avatarurl: Field[str] = fields.CharField(max_length=128, null=True, default="default.jpg")
    """
    用户头像文件名 (带后缀名)
    """

    coin: Field[int] = fields.IntField(null=True, default=0)
    """
    硬币数 默认 0
    """
    
    description: Field[str] = fields.CharField(max_length=512, null=True, default="用户还没有自我介绍哟~")
    """
    用户自我介绍
    """ 
    
    destroyed: Field[bool] = fields.BooleanField(null=True, default=False)
    """
    用户是否已注销
    """

    class Meta:
        table: str = "users"
