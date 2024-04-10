#!/bin/bash

servers="host01 host02"
sshKey="$HOME/.ssh/id_rsa"
sshPub="$HOME/.ssh/id_rsa.pub"

ssh-keygen -q -N "" -f $sshKey

for server in $servers
do
    echo $server
    sshpass -s "$1" ssh-copy-id -i $sshPub stack@$server
done