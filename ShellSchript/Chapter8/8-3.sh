#!/bin/bash

servers = 'host01 host02 host03'
cmd1 = 'cat /etc/*release | grep ID_LIKE | sed "s/ID_LIKE=//;s/\"//g"'
cmd2 = ''

for server in $servers; do
    ostype = $(sshpass -p $1 ssh root@server $cmd1)

    if [[ $ostype == "fedora" ]]; then
        cmd2 = "yum -y install ntp"
    elif [[ $ostype == "debian" ]]; then
        cmd2 = "apt-get -y insatll ntp"
    else
        echo "You must check OS-type"
    fi
    
    sshpass -p $1 ssh root@server $cmd2
done