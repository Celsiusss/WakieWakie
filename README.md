# WakieWakie

A project to encourage students to wake up!

## Development Setup

Setup a virtual environment and install dependencies

```sh
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Local Database

Setup a PostreSQL database to be used locally (recommend using docker).

Set the correct environment variables using a `.env` file in the root folder of this project.

**Remember to create your database first!**

Run `seed.sql` on your database.

### Run the application

Now run the project locally

```sh
$ uvicorn wakiewakie.main:app --reload
```

## Environment Variables

| Name          | Value                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------ |
| DB_CONNECTION | [Connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) |


