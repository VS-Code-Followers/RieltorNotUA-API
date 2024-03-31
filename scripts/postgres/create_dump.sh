#!/bin/bash

export PG_CONTAINER_NAME=rieltor_pg_db
export POSTGRES_USER=user
export POSTGRES_DB=name

if [ ! -d scripts/dumps ]; 
then
    mkdir scripts/dumps
fi


read -p "Create unique name of db_dump: " name_of_db_dump

docker exec -t ${PG_CONTAINER_NAME} pg_dump --username ${POSTGRES_USER} --dbname=${POSTGRES_DB} > scripts/dumps/${name_of_db_dump}_db_dump.sql