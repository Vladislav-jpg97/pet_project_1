from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class DeviceTypeEnum(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    BOT = "bot"

class Click(Base):
    __tablename__ = 'clicks'

    link_id: Mapped[int] = mapped_column(ForeignKey('links.id'), nullable=False, index=True)
    clicked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    ip_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    referer: Mapped[str | None] = mapped_column(String, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    device_type: Mapped[DeviceTypeEnum] = mapped_column(
        SQLEnum(
            DeviceTypeEnum,
            name="device_type_enum",
            create_type=True
        ),
        nullable=False
    )