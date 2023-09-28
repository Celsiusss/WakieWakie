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

## Steps

### 1. **Pull the PostgreSQL Docker Image:**

   Open your terminal and run the following command to pull the latest PostgreSQL Docker image:

```sh
    docker pull postgres
```

### 2. Run a PostgresSQL container 

    If running locally password can be anything 
```sh
    docker run --name mydatabase -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```
   
### 3. Set environment variable 

    Set the correct environment variables using a `.env` file in the root folder of this project.

```sh
    echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres" > env.env
    
```

### 4. run the 'seed.sql' on db 

```sh
    docker cp path/to/seed.sql mydatabase:/seed.sql
```

```sh
    docker exec -it mydatabase psql -U postgres -d postgres -a -f seed.sql
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


