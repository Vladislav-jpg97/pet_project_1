import secrets
import string
import ipaddress
import socket
from urllib.parse import urlparse
from fastapi import HTTPException, status


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def generate_slug(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def validate_url_not_private(url: str) -> None:
    """
    Проверяет, что URL не ведет на локальные или приватные IP-адреса (защита от SSRF).
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный URL",
        )

    # Запрещаем явные локалхосты и опасные хосты
    forbidden_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
    if hostname.lower() in forbidden_hosts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Запрещено сокращать ссылки на локальные ресурсы (SSRF защита)",
        )

    try:
        # Пытаемся разрешить хост в IP-адрес
        ip_str = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip_str)

        # Проверяем, является ли IP приватным, петлевым (loopback) или локальным для ссылки
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Запрещено сокращать ссылки на приватные IP-диапазоны",
            )
    except socket.gaierror:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось разрешить доменное имя (несуществующий хост)",
        )
