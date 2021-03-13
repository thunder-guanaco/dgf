#!/bin/bash
# This script contains util functions to log print nice error messages

RED="\e[31m"
GREEN="\e[32m"
RESET="\e[0m"

function exit_if_error() {
    command=$1
    return_code=$2
    if [[ "${return_code}" -ne "0" ]]
    then
        echo -e "${RED}[ERROR]${RESET} ${command}"
        exit 1
    else
        echo -e "${GREEN}[OK]${RESET} ${command}"
    fi
}