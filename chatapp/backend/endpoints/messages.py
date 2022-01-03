from fastapi import APIRouter, Request

from chatapp.backend.utils.auth import (
    tokenList,
    bannedList,
    auth,
    AuthenticationRequired,
)
from chatapp.backend.errors.error import NonExistentValueError
from chatapp.backend.ratelimits import limiter

import logging
from datetime import datetime

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/messages")
@AuthenticationRequired
async def messages_get(request: Request, token: str, message: str):
    log.info(f"GET request to endpoint /messages from client {request.client.host}")
    return {"content": message, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@router.post("/messages")
@AuthenticationRequired
async def messages_post(token: str, request: Request, message: str = None):
    log.info(f"POST request to endpoint /messages from client {request.client.host}")
