#!/bin/bash

read -p "Input instance name : " vmname

echo "== Image List =="
openstack image list -c Name -f value
raed -p "input image name : " image

echo "== Network List =="
openstack network list -c Name -f value
read -p "Input network name : " net

echo "== Flavor List =="
openstack flavor list -c Name -f value
read -p "Input flavor name : " flavor

echo "== Security group List =="
openstack security group list --project $OS_PROJECT_NAME -c Name -f value
read -p "Input security group name : " sec
secgrp=$(openstack security group list --project $OS_PROJECT_NAME -f value -c ID -c Name | grep "$sec\$" | awk '{print $1}')

echo "== Keypair List =="
openstack keypair list -c Name -f value
read -p "input keypair name : " keypair

echo "== Create volume =="
read -p "input volume size : " size
openstack volume create --size $size --image $image --bootable $vmname

echo "Create Instance Starting"
openstack server create \
    --vlume $(openstack volume list --name $vmname -f value -c ID) \
    --flavor $flavor \
    --security-group $secgrp \
    --key-name $keypair \
    --network $net \
    --wait \
    $vmname