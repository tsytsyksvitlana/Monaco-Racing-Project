from web_app.db.models.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped


class Race(Base):
    __tablename__ = 'races'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=20))
    year: Mapped[int]
