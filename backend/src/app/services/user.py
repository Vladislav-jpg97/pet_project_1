from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegister, UserLogin
from app.core.security import get_password_hash, generate_api_key, verify_password, create_access_token


class UserService:
    def __init__(self, session: AsyncSession, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

    async def create_user(self, user_data: UserRegister) -> User:
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_password_hash(user_data.password)
        api_key = generate_api_key()

        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            api_key=api_key,
        )

        return await self.user_repo.create_user(new_user)

    async def login_user(self, user_data: UserLogin) -> str:
        user = await self.user_repo.get_user_by_email(user_data.email)
        if user is None or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return create_access_token(user.id)
