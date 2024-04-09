# Steps, to run API at localhost

### 1. Clone this repository

```bash
git clone https://github.com/CBoYXD/RietorNotUA-API.git
```

### 2. Start project with [docker compose](https://docs.docker.com/compose/)

1) [Install Docker](https://docs.docker.com/engine/install/) (if not already installed)
2) Start Docker
3) Run project
   
```bash
docker compose up
```

#### Also you need to create database and tables. You have 3 variants:

1) Use alembic
   
```bash
./scripts/alembic/run_migration.sh
```

2) Use postgres dumps **(if you create it before)**
   
```bash
./scripts/postgres/restore.sh
```

After that write name of this dump

3) Any other script you have

### 3. Link to API

You need to use [this link](http://127.0.0.1:8000), for access to API.

## For run tests you needs:

#### Note*: You need to run docker container before you runs the tests

### 1. Create venv

```bash
python -m venv .venv
```

### 2. Install Dependencies

```bash
python -m poetry install --with test --no-root
```

### 3. Set environment variables:

1) Rename .config/db_example.env to db.env and .config/api_example.env to api.env
2) Put all need data in this file ([I recommend this hosting for DataBase](https://vercel.com/))

### 4. Run tests

```bash
python -m pytest .
```

## To use mypy

```bash
mypy --install-types
```

## Also you can use ```scripts/gen/create_all.sh``` for generating data in DataBase 

#### Note*: Before generating data you need create .venv and install all necessary dependencies

## Note!: All scripts must run from root directory of project!

## Good luck! 😁