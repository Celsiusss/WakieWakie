import psycopg
from psycopg.rows import dict_row

class DbDependency:
    conn: psycopg.AsyncConnection = None

    def __init__(self) -> None:
        pass
    async def start(self):
        self.conn = await psycopg.AsyncConnection.connect("dbname=wakiewakie user=postgres password=abc123 host=localhost port=5432")
    async def __call__(self):
        cur = self.conn.cursor(row_factory=dict_row)
        try:
            yield cur
        finally:
            await self.conn.commit()
            await cur.close()
