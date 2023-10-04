from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import Self
from pydantic import BaseModel

class CheckinType(Enum):
    CHECKIN = 'checkin'
    CHECKOUT = 'checkout'

    def from_str(v: str) -> Self:
        return CheckinType[str.upper(v)]

class PostPerson(BaseModel):
    name: str
    cardno: int

@dataclass
class Checkin:
    id: int = 0
    type: CheckinType = CheckinType.CHECKIN
    time: datetime.datetime = datetime.datetime.min

@dataclass
class PersonEntry:
    days: dict[str, str]
    name: str = ""
    average_time = ""
