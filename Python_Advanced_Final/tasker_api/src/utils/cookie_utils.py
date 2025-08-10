from typing import Optional
from starlette.responses import Response

def set_access_token_cookie(response: Response, token: str, max_age: Optional[int] = None):
    """
    Устанавливает JWT-токен в куку для клиента.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=max_age,
    )

def set_refresh_token_cookie(response: Response, token: str, max_age: Optional[int] = None):
    """
    Устанавливает токен обновления в куку.
    """
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=max_age,
    )