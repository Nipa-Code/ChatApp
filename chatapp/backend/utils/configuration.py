from urllib.parse import unquote
from decouple import config


class Discord:
    """Any config required for interaction with Discord."""

    CLIENT_ID = config("CLIENT_ID")
    CLIENT_SECRET = config("CLIENT_SECRET")
    # starlette already quotes urls, so the url copied from discord ends up double encoded
    AUTH_URL = config("AUTH_URL", cast=unquote)
    TOKEN_URL = config("TOKEN_URL", default="https://discord.com/api/oauth2/token")
    USER_URL = config("USER_URL", default="https://discord.com/api/users/@me")
    WEBHOOK_URL = config("WEBHOOK_URL")
    API_BASE = "https://discord.com/api/v8"


class Server:
    """General config for the pixels server."""

    BASE_URL = config("BASE_URL", default="http://127.0.0.1:5001")
    JWT_SECRET = config("JWT_SECRET")

    SHOW_DEV_ENDPOINTS = "true" != config("PRODUCTION", default="false")


def build_oauth_token_request(code: str) -> tuple[dict, dict]:
    """Given a code, return a dict of query params needed to complete the OAuth2 flow."""
    query = {
        "client_id": Discord.CLIENT_ID,
        "client_secret": Discord.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{Server.BASE_URL}/callback",
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return query, headers
