from typing import Union, Optional
from asyncpg.pool import Pool
import asyncpg
from dotenv import load_dotenv, find_dotenv
import os, asyncio

load_dotenv(find_dotenv())
URL = os.getenv("DNS_URL")


class App:
    """Class for handling and creating 'global' database poolinstance"""

    db: Optional[Pool] = None


# instance of App class
app = App()


async def create_db_pool():
    """
    creates a database pool
    ---
    Arguments -> None
    """
    app.db = await asyncpg.create_pool(dsn=URL)
