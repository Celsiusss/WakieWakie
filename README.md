# WakieWakie

A project to encourage students to wake up!

- [WakieWakie](#wakiewakie)
  - [Development Setup](#development-setup)
    - [Local Database](#local-database)
    - [Setting Up PostgreSQL with Docker](#setting-up-postgresql-with-docker)
    - [Run the application](#run-the-application)
  - [Migrations](#migrations)
    - [Add Migration](#add-migration)
  - [Environment Variables](#environment-variables)


## Development Setup

Setup a virtual environment and install dependencies

```sh
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Local Database

Setup a PostreSQL database to be used locally (recommend using docker).

Apply [migrations](#migrations)!

### Setting Up PostgreSQL with Docker

<details>
<summary>Setting Up PostgreSQL with Docker</summary>
This guide provides steps to set up a PostgreSQL database using Docker for the project.

run either 
```sh 
    docker-compose up -d 
```

```sh 
    docker-compose down 
```

**Remember this step!**
</details>

### Run the application

Now run the project locally

```sh
$ uvicorn wakiewakie.main:app --reload
```

## Migrations

Use the provided script to run migrations. It uses the samme `DB_CONNECTION` environment variable as the main application.

```
$ python database.py
```

### Add Migration

To add a new migration, add a file with the naming format `XXXXXX_<name>.sql` to the `migrations` directory, where `XXXXXX` is a number following the last migration number.

## Environment Variables

| Name          | Value                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------ |
| DB_CONNECTION | [Connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) |


