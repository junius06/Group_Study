#!/bin/bash

conf_path=/etc/ssh/sshd_config

function restart_system()
{
    echo "Restart sshd"
    sudo systemctl restart sshd
}

cp $conf_path ${conf_path}.bak.$(date + %Y%m%d)

case $1 in
    1)
    read -p "Please input port: " port
    exist_conf=$(cat $conf_path | grep -e '^#Port' -e '^Port')
    sed -i "s/$exist_conf/Port $port/g" $conf_path
    restart_system
    ;;
    2)
    read -p "Please input PermitRootLogin yes or no: " rootyn
    exist_conf=$(cat $conf_path | grep -e '^#PermitRootLogin' -e '^PermitRootLogin')
    sed -i "s/^PermitRootLogin $rootyn/g" $conf_path
    restart_system
    ;;
    3)
    read -p "Please input PasswordAuthentication yes or no: " pwyn
    exist_conf=$(cat $conf_path | grep -e '^#PasswordAuthentication' -e '^PasswordAuthentication')
    sed -i "s/$exist_conf/PasswordAuthentication $pwyn/g" $conf_path
    restart_system
    ;;
esac