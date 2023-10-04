import datetime
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Any
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg

from wakiewakie.db_dependency import DbDependency
from wakiewakie.data_models.person import Checkin, PersonEntry, PostPerson
from wakiewakie.utils import CheckinType, calc_avg_times, format_time, format_timedelta, group_by


db_dependency = DbDependency()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_dependency.start()
    yield

app = FastAPI(lifespan=lifespan)

DbDep = Annotated[psycopg.Cursor, Depends(db_dependency)]

app.mount("/css", StaticFiles(directory=f"{os.getcwd()}/wakiewakie/templates/css"), name="css")
templates = Jinja2Templates(directory=f"{os.getcwd()}/wakiewakie/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: DbDep):
    await db.execute("""
                     SELECT
                        p.id, p.name,
                        SUM(c.duration) FILTER (WHERE c.dow = 1) monday,
                        SUM(c.duration) FILTER (WHERE c.dow = 2) tuesday,
                        SUM(c.duration) FILTER (WHERE c.dow = 3) wednesday,
                        SUM(c.duration) FILTER (WHERE c.dow = 4) thursday,
                        SUM(c.duration) FILTER (WHERE c.dow = 5) friday,
                        AVG(c.duration) average,
                        COUNT(*) average_count,
                        EXTRACT(ISODOW FROM now()) total_count
                     FROM people p
                        INNER JOIN checkin_days c ON p.id = c.person_id
                     WHERE c.d >= DATE_TRUNC('week', current_date)              -- limit to current week only
                     GROUP BY p.id;
                     """);
    response = await db.fetchall()
    
    people: list[PersonEntry] = []
    for r in response:
        average: datetime.timedelta = r['average']
        average_count: int = r['average_count']
        total_count: int = int(r['total_count'])

        # if a person has not checked in on some days, factor those days in here
        if total_count > average_count:
            average = average * (average_count / total_count)

        days = {
            'monday': format_timedelta(r['monday']),
            'tuesday': format_timedelta(r['tuesday']),
            'wednesday': format_timedelta(r['wednesday']),
            'thursday': format_timedelta(r['thursday']),
            'friday': format_timedelta(r['friday'])
        }
        person = PersonEntry(days)
        person.name = r['name']
        person.average_time = format_timedelta(average)

        people.append(person)
    
    await db.execute("""
                     SELECT p.name, c.type, c.time FROM people AS p
                     INNER JOIN checkins AS c ON c.person_id = p.id
                     ORDER BY c.time DESC
                     LIMIT 20;
                     """)
    recent_log = await db.fetchall()
    for e in recent_log:
        e['time'] = format_time(e['time'])
    return templates.TemplateResponse("index.html", {"request": request, "people": people, "checkins": recent_log})

@app.post("/person")
async def post_person(person: PostPerson, db: DbDep):
    await db.execute("INSERT INTO people (name, cardno) VALUES (%s, %s)", (person.name, person.cardno))
    print(f"Inserted new person {person}")

@app.post("/checkin")
async def checkin(cardno: int, db: DbDep) -> str:
    await db.execute("SELECT id, name FROM people where cardno = %s;", (cardno,))
    result = await db.fetchone()

    if result is None:
        return "User not found"
    
    person_id = result["id"]
    name = result["name"]

    await db.execute("""
                     SELECT id, type, time FROM checkins
                        WHERE person_id = %s
                        AND time::date = now()::date
                        ORDER BY time DESC;
                     """,
                     (person_id,))
    checkin = await db.fetchone()
    checkin_type = CheckinType.CHECKIN

    if checkin != None:
        prev_type = CheckinType.from_str(checkin["type"])
        checkin_type = CheckinType.CHECKIN if prev_type == CheckinType.CHECKOUT else CheckinType.CHECKOUT
    
    if checkin_type == CheckinType.CHECKOUT:
        # get previous checkin and add the time difference to current checkout
        await db.execute("""
                         INSERT INTO checkins (person_id, type, time, duration)
                         SELECT %s, %s, now(), now() - s.time FROM
                            (
                                SELECT time FROM checkins
                                WHERE person_id = %s
                                AND type = 'checkin' 
                                AND time::date = now()::date
                                ORDER BY time DESC LIMIT 1
                            ) AS s;
                         """,
                (person_id, checkin_type.value, person_id))
    else:
        await db.execute("INSERT INTO checkins (person_id, type, time) VALUES (%s, %s, date_trunc('seconds', now()))",
                     (person_id, checkin_type.value))

    if checkin_type == CheckinType.CHECKIN:
        return f"Good morning {name}"
    else:
        return f"See you tomorrow {name}"
