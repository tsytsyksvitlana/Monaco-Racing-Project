from web_app.db.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class Driver(Base):
    __tablename__ = 'drivers'
    id: Mapped[int] = mapped_column(primary_key=True)
    abbr: Mapped[str] = mapped_column(String(length=5), unique=True)
    name: Mapped[str]
    team: Mapped[str]

    def __repr__(self) -> str:
        return (
            f'Driver(id={self.id}, abbr={self.abbr}, '
            f'name={self.name}, team={self.team}'
        )
