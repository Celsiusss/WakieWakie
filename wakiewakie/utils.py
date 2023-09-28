import datetime
from enum import Enum
from typing import Any, Callable

from pytz import timezone

from wakiewakie.data_models.person import CheckinType

TZ = timezone("Europe/Oslo")

def format_time(time: datetime.datetime) -> str:
    """
    Formats a datetime into a human readable string.
    """
    time_utc = timezone("UTC").localize(time, is_dst=False)
    local_time = time_utc.astimezone(TZ)

    if local_time.date() == datetime.date.today():
        return local_time.strftime("today %H:%M")

    return local_time.strftime("%A %H:%M")

def calc_avg_times(times: list[tuple[CheckinType, datetime.datetime]]) -> datetime.timedelta:
    """
    Expects the input list to be sorted by datetime in ASCENDING order.
    """

    total = datetime.timedelta(0)
    valid_days = 0
    last_checkin: datetime.datetime | None = None

    for (t, time) in times:
        if t == CheckinType.CHECKIN:
            last_checkin = time
            #continue
        elif last_checkin == None:
            continue
        diff = time - last_checkin
        total += diff
        valid_days += 1
    
    average = (total / valid_days)
    
    return average

def group_by(list: list, keyfn: Callable[[Any], str]) -> dict:
    out = dict()

    for e in list:
        key = keyfn(e)

        if key not in out:
            out[key] = []
        out[key].append(e)

    return out
