#!/bin/bash

IFS=

read -p "Enter amount of photos in offers: " photo_nums

if [[ $photo_nums =~ ^[0-9]+$ ]];
then
    read -p "Enter general amount for each type of offers (press enter if you want a more detailed setting): " gen_num

    if [[ $gen_num == "" ]];
    then 

        read -p "Enter amout of flat-type offers: " num_flat 
        if [[ $num_flat =~ ^[0-9]+$ ]];
        then

            read -p "Enter amout of house-type offers: " num_house
            if [[ $num_house =~ ^[0-9]+$ ]];
            then
            
                read -p "Enter amout of office-type offers: " num_office
                if [[ $num_office =~ ^[0-9]+$ ]];
                then
                    python scripts/gen/src/gen_offers.py --photo_num $photo_nums \
                        --flat_num $num_flat --house_num $num_house \
                        --office_num $num_office
                else
                    echo "Invalid input"
                fi

            else
                echo "Invalid input"
            fi

        else
            echo "Invalid input"
        fi

    elif [[ $gen_num =~ ^[0-9]+$ ]];
    then
        python scripts/gen/src/gen_offers.py --gen_num $gen_num --photo_num $photo_nums
    else
        echo "Invalid input"
    fi
else
    echo "Invalid input"
fi