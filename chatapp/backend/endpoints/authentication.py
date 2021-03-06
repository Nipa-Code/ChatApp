import logging
import traceback

from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from httpx import AsyncClient
from starlette.responses import RedirectResponse


from chatapp.backend.utils import auth
from chatapp.backend.utils.auth import Authorization
from chatapp.backend.utils.configuration import (
    Server,
    Discord,
    build_oauth_token_request,
)

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/authorize")
async def authorize() -> Response:
    """
    Redirect the user to Discord authorization, the flow continues in /callback.
    Unlike other endpoints, you should open this one in the browser, since it redirects to the Discord OAuth2 flow.
    """
    return RedirectResponse(url=Discord.AUTH_URL)


@router.get("/show_token")
async def show_token(
    request: Request, token: str = Cookie(None)
) -> Response:  # noqa: B008
    """Show the refresh token from the URL path to the user."""
    template_name = "cookie_disabled.html"
    context = {"request": request}

    if token:
        context["token"] = token
        template_name = "api_token.html"

    return context


@router.get("/callback")
async def auth_callback(request: Request) -> Response:
    """
    Create the user given the authorization code and output the refresh token.
    This endpoint is only used as a redirect target from Discord.
    """
    print(request.query_params)
    try:
        async with AsyncClient() as client:
            token_params, token_headers = build_oauth_token_request(
                request.query_params["code"]
            )
            auth_token = (
                await client.post(
                    Discord.TOKEN_URL, data=token_params, headers=token_headers
                )
            ).json()
            auth_header = {"Authorization": f"Bearer {auth_token['access_token']}"}
            user = (await client.get(Discord.USER_URL, headers=auth_header)).json()
            token, _ = await auth.reset_user_token(request.state.db_conn, user["id"])
        print(Request.query_params)
    except KeyError:
        # Ensure that users don't land on the show_pixel page
        log.error(traceback.format_exc())
        raise HTTPException(401, "Unknown error while creating token")
    except PermissionError:
        raise HTTPException(401, "You are banned")

    # Redirect so that a user doesn't refresh the page and spam discord
    redirect = RedirectResponse("/show_token", status_code=303)
    redirect.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=10,
        path="/show_token",
    )
    return redirect


"""
@router.post("/authenticate", response_model=AccessToken)
async def authenticate(request: Request, body: RefreshToken) -> dict:
    '''
    Authenticate and request an access token.
    Users should replace their local refresh token with the one returned.
    '''
    access, refresh = await auth.generate_access_token(request.state.db_conn, body.refresh_token)
    return {
        "access_token": access,
        "token_type": "Bearer",
        "expires_in": Authorization.ACCESS_EXPIRES_IN,
        # In the future we may use this so that we can regenerate refresh tokens every once in a while
        "refresh_token": refresh,
    }
"""
