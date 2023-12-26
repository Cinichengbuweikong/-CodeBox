from typing import Dict

from redis import asyncio as aioredis
from redis.asyncio import Redis

from constants import REDIS_URL, REDIS_PASSWORD


redis_conn: Dict[int, Redis] = {}


async def getRedisConnect(db: int = 0) -> Redis:
    """
    获取 redis 连接
    db: int 是要使用的数据库 默认为 0
    """

    global redis_conn

    if redis_conn.get(db) != None:
        return redis_conn[db]
    
    redis_conn[db] = aioredis.from_url(
        REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        password=REDIS_PASSWORD,
        db=db
    )

    return redis_conn[db]
