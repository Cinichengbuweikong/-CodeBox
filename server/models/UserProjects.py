from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class UserProjects(Model):
    """
    用户项目表  User 表中的一条数据对应此表中多条数据
    """

    pid: Field[int] = fields.IntField(pk=True, index=True)
    """
    项目 id
    """

    uid: Field[int] = fields.IntField()
    """
    该项目所有者的 uid
    """

    projectname: Field[str] = fields.CharField(max_length=128)
    """
    项目名
    """

    description: Field[str] = fields.CharField(max_length=512, null=True, default="该项目还没有介绍哟~")
    """
    项目介绍
    """

    effectimg: Field[str] = fields.CharField(max_length=512, null=True, default="default.jpg")
    """
    效果图
    """
    
    name: Field[str] = fields.CharField(max_length=512, null=False)
    """
    项目文件夹名 这是一个唯一值
    """

    class Meta:
        table: str = "userProjects"

