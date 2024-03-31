#!/bin/bash

export PG_CONTAINER_NAME=rieltor_pg_db
export POSTGRES_USER=user
export POSTGRES_DB=name

if [ ! -d scripts/dumps ]; 
then
    echo "dumps folder does not exist"
else
    read -p "Enter unique name of db_dump: " name_of_db_dump
    
    docker cp scripts/dumps/${name_of_db_dump}_db_dump.sql ${PG_CONTAINER_NAME}:/tmp/${name_of_db_dump}_db_dump.sql
    docker exec -t ${PG_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f tmp/${name_of_db_dump}_db_dump.sql
fi