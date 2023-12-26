# 让 tortoise orm 根据模型生成数据库中的表
# 每次修改表后都要重新执行此文件
# create database codeBox charset=utf8;

from tortoise import Tortoise, run_async

from models import MODELS_LISTS
from constants import DB_URL


async def init() -> None:
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            'models': [*MODELS_LISTS]
        }
    )

    # 在数据库中生成表
    await Tortoise.generate_schemas()


run_async(init())
