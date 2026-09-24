from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Date
class ReportBase(DeclarativeBase):
    pass

class ClickStatsDaily(ReportBase):
    __tablename__ = 'click_stats_daily'

    link_id: Mapped[int] = mapped_column(ForeignKey('links.id'), primary_key=True, nullable=False)
    date: Mapped[Date] = mapped_column(Date, primary_key=True, nullable=False)
    clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    unique_visitors: Mapped[int] = mapped_column(default=0, nullable=False)