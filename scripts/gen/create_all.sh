#!/bin/bash

if [ ! -f localhost.env ];
then
    echo "localhost.env file doesn't exist"
else
    export ENV_FILE="localhost.env"
    bash scripts/gen/create_offers.sh
fi