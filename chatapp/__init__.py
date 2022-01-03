from chatapp.pool import create_db_pool
import asyncio


async def _create():
    return await create_db_pool()


# asyncio.get_event_loop().run_until_complete(_create())
