from web_app.db.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web_app.db.models.race import Race
    from web_app.db.models.drivers import Driver


class ResultRace(Base):
    __tablename__ = 'results'
    id: Mapped[int] = mapped_column(primary_key=True)
    race_id: Mapped[int] = mapped_column(
        ForeignKey('races.id', ondelete='CASCADE'))
    race: Mapped['Race'] = relationship(backref='results')
    driver_id: Mapped[int] = mapped_column(
        ForeignKey('drivers.id', ondelete='CASCADE'))
    driver: Mapped['Driver'] = relationship(backref='results')
    start: Mapped[int]
    end: Mapped[int]
    position: Mapped[int]
    stage: Mapped[str] = mapped_column(String(length=3))

    def __repr__(self):
        return (
            f'ResultRace(race_id={self.race_id}, '
            f'driver_id={self.driver_id}, start={self.start}, '
            f'end={self.end}, position={self.position}, stage={self.stage}'
        )
