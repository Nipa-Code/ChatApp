from fastapi import FastAPI, Request, status
from fastapi.params import Form
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from chatapp.backend.ratelimits import limiter
from chatapp.backend.ratelimits.limiter import Connections
from chatapp.backend.endpoints import authentication, messages, users
from chatapp.backend.utils.auth import auth
from chatapp.log import setup

from starlette.responses import RedirectResponse
import aioredis
import typing as t
import uvicorn
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
URL = os.getenv("DNS_URL")
BASE_URL = os.getenv("BASE_URL")

# fastAPI instance
app = FastAPI()

# Used to handle the other endpoints
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(authentication.router)

# allows html files and used to create a example form
templates = Jinja2Templates(
    directory=r"C:\Users\nipa\projects\chatapp\chatapp\templates"
)

# blacklist process
BLACKLIST = {
    "127.0.0.0",
}


@app.on_event("startup")
async def startup() -> None:
    await Connections.DB_POOL
    app.state.redis_pool = await aioredis.from_url(Connections.REDIS_URL)
    Connections.REDIS_FUTURE.set_result(app.state.redis_pool)


@app.middleware("http")
async def setup_data(request: Request, callnext: t.Callable) -> Response:
    """Get a connection from the pool and a canvas reference for this request."""
    async with Connections.DB_POOL.acquire() as connection:
        request.state.db_conn = connection
        request.state.redis_pool = app.state.redis_pool
        response = await callnext(request)
    request.state.db_conn = None
    return response


@app.get("/")
async def redirect(request: Request):
    return RedirectResponse(url=f"{BASE_URL}/info")


@app.get("/info")
async def info(request: Request):
    return {"message": "You have been redirected to the info page"}


@app.get("/test")
@limiter.limit(1, 30)
async def search(*, search: str):
    """Just returns a user given value."""
    return {"message": search}


@app.get("/form")
@limiter.limit(1, 20)
def form(request: Request):
    """Example form that has no use yet"""
    result = "Type a number"
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": result}
    )


@app.post("/form")
@limiter.limit(1, 20)
def form_post(request: Request, num: int = Form(1)):
    """Posts data to endpoint in order to update the form with the given data"""
    result = num
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": result}
    )


if __name__ == "__main__":
    """Uvicorn server startup"""
    # calls logging
    setup()

    uvicorn.run(
        "chatapp.__main__:app",
        host="0.0.0.0",
        port=5001,
        log_level="info",
        reload=True,
    )
