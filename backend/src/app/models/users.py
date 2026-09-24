from sqlalchemy.orm import Mapped,mapped_column

from .base import Base
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )