import secrets
import string


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def generate_slug(length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

print(generate_slug())