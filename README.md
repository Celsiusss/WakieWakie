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

# Setting Up PostgreSQL with Docker

This guide provides steps to set up a PostgreSQL database using Docker for the project.

## Run docker container 

run either 
```sh 
    docker-compose up -d 
```

```sh 
    docker-compose down 
```

**Remember this step!**

### Run the application

Now run the project locally

```sh
$ uvicorn wakiewakie.main:app --reload
```

## Environment Variables

| Name          | Value                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------ |
| DB_CONNECTION | [Connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) |


