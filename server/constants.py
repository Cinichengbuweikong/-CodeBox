import os
from enum import Enum, IntEnum, StrEnum


# DB_URL: str = "mysql://root:2c18be2e@mysql:3306/codeBox?charset=utf8"
DB_URL: str = "mysql://codeBox:8161a099@mysql:3306/codeBox?charset=utf8"
"""
数据库 url
"""

SALT: str = "2496BED6ECF492A;.~g_n%` v%_i^&s$u:]^[u~+;941fcy:;9B2338C978450E3B7"
"""
盐
"""

REDIS_URL: str = "redis://redis:6379"
"""
redis 链接
"""

REDIS_PASSWORD: str = "394d9664"
"""
redis 密码
"""

KEY: str = "L<vPEG?@g^o:T{LL"
"""
对称加密的密钥
"""

ADMIN_PWD: str = "Wsfqz^TgIq#E5P(840nC"
"""
管理员用户的密码
"""

IMAP_PWD: str = ""
"""
126 邮箱 imap 服务授权码
"""

EMAIL_ADDR: str = ""
"""
发送邮件时使用的邮件地址
"""

EMAIL_CONTENT: str = "<html> <head> <title>CodeBox 验证码</title> </head>  <body> <h1>你正在 CodeBox 上注册账户, 这是你的验证码.</h1> <h4>你的验证码是: <strong>{}</strong> </h4> <h6>如果你没有注册 CodeBox, 那说明填写邮件地址的人把地址写错了, 请你无视此邮件即可.</h6> </body> </html>"


ASSETS_DIR: str = os.path.join(os.getcwd(), ".assets")
"""
静态文件根目录 包括用户头像 效果图 以及用户新建的项目的根目录
"""

AVATAR_IMG_DIR: str = os.path.join(ASSETS_DIR, "avatars")
"""
用户头像文件存储路径
"""

PROJECT_EFFECTIMG_DIR = os.path.join(ASSETS_DIR, "effects")
"""
项目效果图的存储路径
"""



PROJECT_BASE_DIR: str = os.path.join(os.getcwd(), ASSETS_DIR, "projects", "users")
"""
保存所有工程的根目录
"""

TEMP_PROJECT_BASE_DIR: str = os.path.join(os.getcwd(), ASSETS_DIR, "projects", "temps")
"""
保存所有临时工程的根目录
"""

VUE_DEFAULT_TEMPLATE: str = \
"""<template>
    <h1>这是一个新组件, 现在你可以继续写代码了.</h1>
  	<h2>在离开页面之前请点击下面的 "保存修改" 按钮并等待代码保存完成, 否则你的代码将被丢弃.</h2>
</template>

<script setup lang="ts">
</script>

<style>
</style>"""
"""
新建 Vue 文件时的默认内容
"""


class ProjectType(Enum):
    """
    标记项目类型的枚举类
    """

    NORMAL=0
    """
    普通项目
    """
    
    TEMP=1
    """
    临时项目
    """


class CodesType(IntEnum):
    """
    用于标记当前数据所表示的代码文件的类型
    """
    
    VUE = 0
    JS = 1




class ResopnseOperationResultType(StrEnum):
    """
    表示响应体中 "操作是否成功" 的枚举
    """

    OK = "ok"
    FAIL = "fail"
