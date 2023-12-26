from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field


class TempProjects(Model):
    """
    临时项目表 一般来说在如下情况下我们需要创建一个临时项目:
    - 用户在线新建 同时还没点 "发布项目" 的项目
    - 用户正浏览其他人做的项目时所创建的项目 此时用户需要在线编辑代码并看到效果 同时不能影响到项目原作者的代码
    - 用户修改自己项目的代码时

    一个用户可以有多个临时项目
    """

    tpid: Field[int] = fields.IntField(pk=True, index=True)
    """
    临时项目 id
    """

    uid: Field[int] = fields.IntField()
    """
    该临时项目所属的用户的 id
    """

    spid: Field[int] = fields.IntField(null=True)
    """
    该项目所属的源项目的 id
    用户正浏览其他人做的项目时所创建的项目 此时用户需要在线编辑代码并看到效果
    此时 spid 就应该取值用户正浏览的项目的 id
    """

    path: Field[str] = fields.CharField(max_length=512)
    """
    临时项目文件夹的名字
    """

    name: Field[str] = fields.CharField(max_length=512)
    """
    临时项目的名字
    """

    class Meta:
        table = "tempProjects" 

