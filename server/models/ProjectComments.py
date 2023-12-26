from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class ProjectComments(Model):
    """
    项目评论表 存储某个项目下的评论
    """

    cid: Field[int] = fields.IntField(pk=True, index=True)
    """
    评论 id
    """

    pid: Field[int] = fields.IntField()
    """
    项目 uid
    """

    uid: Field[int] = fields.IntField()
    """
    评论的用户的 uid
    """

    comment: Field[str] = fields.CharField(max_length=512)
    """
    评论
    """

    date: Field[str] = fields.CharField(max_length=64)
    """
    用户评论日期
    """

    like: Field[int] = fields.IntField(null=True, default=0)
    """
    赞数
    """

    class Meta:
        table: str = "projectComments"

