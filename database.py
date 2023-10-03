import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION = os.getenv('DB_CONNECTION')

MIGRATIONS_FOLDER = 'migrations'

def run():
    connection = psycopg.connect(DB_CONNECTION)
    cursor = connection.cursor()

    initialize_migration_table(cursor)

    cursor.execute("SELECT migration_num FROM _migrations ORDER BY migration_num DESC;")
    result = cursor.fetchone()
    last_migration = 0

    if result is not None:
        last_migration = result[0]
    
    initialize_migration_table(cursor)
    connection.commit()
    cursor.close()


    apply_migrations(last_migration, connection)


def initialize_migration_table(cursor: psycopg.Cursor):
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS _migrations (
                        id serial primary key,
                        migration_num int not null,
                        run_date timestamp default now()
                    );
                    """)

def apply_migrations(last_migr_num, conn: psycopg.Connection):
    files = os.listdir(MIGRATIONS_FOLDER)

    migrations = dict()


    for file in files:
        try:
            [num, name] = file.split("_", 1)
            num = int(num)
            migrations[num] = file
        except Exception as e:
            print("Error in sql file", file)
            print(e)
            return
    
    unapplied_migrations = list(sorted(filter(lambda n: n > last_migr_num, migrations.keys())))

    if len(unapplied_migrations) == 0:
        print("No unapplied migrations found")
        return

    print(f"Found {len(unapplied_migrations)} unapplied migrations")
    
    cur = conn.cursor()
    with conn.transaction():
        for num in unapplied_migrations:
            sql_file_name = migrations[num]
            sql_content = None
            with open(f"{MIGRATIONS_FOLDER}/{sql_file_name}", "r") as f:
                sql_content = f.read()
            cur.execute(sql_content)
            print(f"Applied {sql_file_name}")
            cur.execute("INSERT INTO _migrations (migration_num) VALUES (%s)", (num,))
    conn.commit();
    cur.close()
    print("Migrations applied successfully")

if __name__ == "__main__":
    run()
