from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, db_user: User) -> User:
        # Репозиторий просто добавляет модель в сессию и фиксирует изменения
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user