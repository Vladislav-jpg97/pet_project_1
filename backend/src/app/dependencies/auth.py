from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.dependencies.database import SessionDep
from app.models import User
from app.repositories.user import UserRepository
from app.services.user import UserService


async def get_user_repo(
        session: SessionDep,
) -> UserRepository:
    return UserRepository(session)


UserRepoDep = Annotated[
    UserRepository,
    Depends(get_user_repo)
]


async def get_user_service(
        session: SessionDep,
        user_repo: UserRepoDep
) -> UserService:
    return UserService(session=session, user_repo=user_repo)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]

oauth2_scheme = HTTPBearer()


async def get_current_user(
        user_repo: UserRepoDep,
        credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> User:
    user_id = decode_token(credentials.credentials)
    user = await user_repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]
