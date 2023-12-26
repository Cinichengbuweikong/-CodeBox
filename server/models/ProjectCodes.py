from tortoise.models import Model
from tortoise import fields
from tortoise.fields import Field

from constants import CodesType


class ProjectCodes(Model):
    """
    存储一个项目中的所有代码的表
    UserProjects 中的一条数据对应此表中的多条数据
    """

    cid: Field[int] = fields.IntField(pk=True, index=True)
    """
    codeid  表示代码数据的 id
    """

    pid: Field[int] = fields.IntField()
    """
    projectid  该数据所属的项目的 id
    """

    name: Field[str] = fields.CharField(max_length=128)
    """
    name  代码文件的名字 代码文件的名字只存储在数据库中 实际文件名由服务自动创建
    """

    pathname: Field[str] = fields.CharField(max_length=256)
    """
    pathname  代码文件存储时的文件名
    """

    type: CodesType = fields.IntEnumField(enum_type=CodesType)
    """
    type  代码文件的类型 取值 CodesType.VUE 或 CodesType.JS
    """

    class Meta:
        table: str = "projectCodes" 

