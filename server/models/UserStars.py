from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class UserStars(Model):
    """
    存储用户的收藏  User 表中一条数据可对应此表中的多条数据
    """

    sid: Field[int] = fields.IntField(pk=True, index=True)
    """
    收藏信息 id
    """

    uid = fields.IntField()
    """
    用户 id  对应 User 表中的 uid
    """

    pid = fields.IntField()
    """
    项目 id  对应 User 表中的 pid
    """

    class Meta:
        table: str = "userStars" 

