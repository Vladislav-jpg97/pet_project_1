import ipaddress
import secrets
import socket
import string
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

import bcrypt
from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.core.configs import settings


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def generate_slug(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def validate_url_not_private(url: str) -> None:
    """Проверяет, что URL не ведет на локальные или приватные IP-адреса (защита от SSRF)."""
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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля хэшу."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """Создает хэш пароля с ограничением в 72 байта для bcrypt."""
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(user_id: int) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
def decode_token(token: str, expected: str = "access") -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id_str: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id_str is None or token_type != expected:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    return int(user_id_str)
