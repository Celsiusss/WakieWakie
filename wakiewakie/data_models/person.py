from dataclasses import dataclass, field
import datetime
from enum import Enum
from pydantic import BaseModel

class CheckinType(Enum):
    CHECKIN = 'checkin'
    CHECKOUT = 'checkout'

class PostPerson(BaseModel):
    name: str
    cardno: int

@dataclass
class Checkin:
    id: int = 0
    type: CheckinType = CheckinType.CHECKIN
    time: datetime.datetime = datetime.datetime.min

@dataclass
class PersonWithCheckins:
    id: str = 0
    name: str = ""
    checkins: list[Checkin] = field(default_factory=list) 
    average_time = 0


