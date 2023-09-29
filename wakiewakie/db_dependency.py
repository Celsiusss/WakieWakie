import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

class DbDependency:
    conn: psycopg.AsyncConnection = None

    def __init__(self) -> None:
        pass
    async def start(self):
        self.conn = await psycopg.AsyncConnection.connect(f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host=localhost port=5432")
    async def __call__(self):
        cur = self.conn.cursor(row_factory=dict_row)
        try:
            yield cur
        finally:
            await self.conn.commit()
            await cur.close()
