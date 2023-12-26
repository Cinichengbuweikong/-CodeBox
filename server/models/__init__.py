from tortoise.contrib.fastapi import register_tortoise

from views import app
from constants import DB_URL


MODELS_LISTS = [
    "models.Users",
    "models.UserStars",
    "models.UserProjects",
    "models.ProjectCodes",
    "models.TempProjects",
    "models.TempCodes",
    "models.ProjectComments",
    "models.commentLike",
]

# 在 fastapi 中注册使用 tortoise-orm
register_tortoise(
    app,
    db_url=DB_URL,
    modules={
        # tortoise-orm 所需注册使用的模型类们
        "models": [*MODELS_LISTS]
    }
)
