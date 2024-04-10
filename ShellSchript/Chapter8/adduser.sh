#!/bin/bash

for hostname in frontend backend

do
    echo $hostname
    sudo useradd -m -s /bin/bash "$hostname" -G dev #작은따옴표x : 변수가 확장되지 않도록 하기 때문에, 변수 내용 대신 문자열 $hostname 을 그대로 사용하게 된다.
    echo "${hostname}:P@ssw0rd" | sudo chpasswd
done