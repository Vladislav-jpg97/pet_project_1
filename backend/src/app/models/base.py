from sqlalchemy.orm import DeclarativeBase

from app.models.mixins import IdentityMixin


class Base(DeclarativeBase,IdentityMixin):
    pass