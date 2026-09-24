from sqlalchemy.orm import DeclarativeBase

from .mixins import IdentityMixin


class Base(DeclarativeBase,IdentityMixin):
    pass