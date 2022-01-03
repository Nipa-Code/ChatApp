import fastapi
from fastapi import APIRouter, Request, HTTPException, Response

from chatapp.backend.utils.auth import tokenList, bannedList, auth
from chatapp.backend.errors.error import NonExistentValueError
from chatapp.backend.ratelimits import limiter
from chatapp.backend.ratelimits.limiter import UserRedis
from chatapp.backend.utils.auth import AuthenticationRequired

from aioredis import Redis

router = APIRouter()


@router.get("/check")
@AuthenticationRequired
async def is_open(token: str):
    return {
        "message": f"API is able to communicate with the server with token validation ({token})"
    }


@router.get("/key")
async def get_key(request: Request):
    return {"message": auth().getToken(str(request.client.host))}


@router.get("/redisreset")
async def redis_reset():
    # redis = Redis(host="redis", port=6379, decode_responses=True)
    # await redis.delete("admin")
    ...


@router.get("/user")
@AuthenticationRequired
async def req(token, request: Request):
    """Test endpoint to check is you are authenticated to use API"""
    if token is None or not token:
        raise HTTPException(406, "Incorrect token")
    if token and auth().auth(token):
        return {"message": "you have authenticated with correct credentials"}
    else:
        return {"message": "Authetication failed"}


@router.get("/testing", response_class=Response)
@UserRedis(
    requests=5,
    time_unit=10,
    cooldown=60,
)
async def _test(request: Request) -> Response:
    return Response(content="Hello")


"""
@router.post("/users/create")
async def create_accout(name: str, password: str):
    if not len(name) < 12 and len(name) > 4:
        return {"message": "Your username must be at least 4 characters and less than 12 characters long"}
"""
