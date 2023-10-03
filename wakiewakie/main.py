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
                     SELECT p.name, AVG(c.duration) FROM people AS p
                        INNER JOIN checkins AS c ON c.person_id = p.id
                     WHERE EXTRACT(ISODOW FROM c.time) < 6 -- where c.time is less than saturday (mon-fri)
                     GROUP BY p.id;
                     """)
    people: list[PersonEntry] = []

    response = await db.fetchall()
    for r in response:
        person = PersonEntry()
        person.name = r['name']
        person.average_time = format_timedelta(r['avg'])
        people.append(person)
    
    await db.execute("""
                     SELECT p.name, c.type, c.time FROM people AS p
                     INNER JOIN checkins AS c ON c.person_id = p.id
                     ORDER BY c.time DESC
                     LIMIT 20;
                     """)
    recent_log = await db.fetchall()
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
