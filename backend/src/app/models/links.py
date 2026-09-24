from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import TimestampMixin

class Link(Base, TimestampMixin):
    __tablename__ = 'links'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    original_url: Mapped[str] = mapped_column(String, nullable=False)
    short_code: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    clicks_count: Mapped[int] = mapped_column(default=0, nullable=False)