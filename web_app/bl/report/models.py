from dataclasses import dataclass
from typing import TypedDict


class DriverTimeTeamType(TypedDict):
    time: float
    team: str
    driver_id: str
    driver: str


@dataclass
class MessageData:
    pos: int
    name: str
    team: str
    time: str


@dataclass
class DriverData:
    abbr: str
    name: str
    team: str
    start: float
    end: float
    result: float
    position: int | None = None

    def __init__(
        self,
        abbr: str,
        name: str,
        team: str,
        start: float,
        end: float,
        result: float,
        position: int | None = None
    ):
        self.abbr = abbr
        self.name = name
        self.team = team
        self.start = start
        self.end = end
        self.result = result
        self.position = position
