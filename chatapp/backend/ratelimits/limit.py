from datetime import timedelta
from aioredis import Redis


async def request_is_limited(r: Redis, key: str, limit: int, period: timedelta):
    """Used to limit requests with redis, return True or False"""
    if await r.setnx(name=key, value=limit):
        await r.expire(key, int(period.total_seconds()))
    bucket_val = await r.get(key)
    print(f"Value of bucket {bucket_val} || {int(bucket_val)}")
    if bucket_val and int(bucket_val) > 0:
        await r.decrby(key, 1)
        return False
    return True
