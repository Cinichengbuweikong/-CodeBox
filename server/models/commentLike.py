from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class CommentLike(Model):
    """
    用户与用户赞的评论表
    """

    lcid: Field[int] = fields.IntField(pk=True, index=True)
    """
    主键
    """

    uid: Field[int] = fields.IntField(null=False)
    """
    用户 id
    """

    cid: Field[int] = fields.IntField(null=False)
    """
    评论 id
    """

    like: Field[bool] = fields.BooleanField(null=False)
    """
    用户是否赞这条评论? 赞则为 True  没赞则为 False
    """

    class Meta:
        table: str = "commentLike"
