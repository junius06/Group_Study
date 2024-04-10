#!/bin/bash

# 사용자 계정 및 패스워드가 입력되었는지 확인
if [[ -n $1 ]] && [[ -n $2 ]]; then

    UserList=($1)
    Password=($2)

    for (( i = 0; i < ${#UserList[0]}; i++ ))
    do
        if [[ $(cat /etc/passwd | grep ${UserList[$i]} | wc -l) == 0 ]]; then
            useradd ${UserList[$i]}
            echo ${Password[$i]} | passwd ${UserList[$i]} --stdin
        else
            echo "This user ${UserList[$i]} is existing."
        fi
    done
else
    echo -e 'Please input user id and password.\nUsage: adduser-script.sh "user01 user02" "pw01 pw02"'
fi

### 단일서버
for server in "host01 host02 host03"
do
    echo $server
    ssh root@$server "useradd $1"
    ssh root@$server "echo $2 | passwd $1 --stdin"
done