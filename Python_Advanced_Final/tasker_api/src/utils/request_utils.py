from starlette.requests import Request
from typing import Optional

def get_client_ip(request: Request) -> Optional[str]:
    """
    Извлекает IP-адрес клиента из запроса.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.client.host

def get_user_agent(request: Request) -> str:
    """
    Извлекает строку User-Agent из запроса.
    """
    return request.headers.get("User-Agent", "Unknown")