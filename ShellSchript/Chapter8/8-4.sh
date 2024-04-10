#!/bin/bash

servers="host01 host02 host03"
cmd1="timedatectl status | grep 'Time zone'"
cmd2="timedatectl set-timezone $1"

if [[ -z $1 ]] || [[ -z $1 ]]; then
    echo -e 'Please input timezone and password\nUsage: sh set-timezone.sh Seoul/Asia password'
    exit;
fi

for server in $servers
do
    timezone = $(sshpass -p $2 ssh root@server "$cmd1" | awk '{print $3}')
    echo "$server: $timezone"

    if [[ $timezone != $1 ]]
    then
        sshpass -p $2 ssh root@$server $cmd2
        echo "$server timezone changed to $1"
    fi
done