#!/bin/bash

repolist=$1
repopath=/var/www/html/repo/
osversion=$(cat /etc/redhat-release | awk '{print $(NF -1)}')

if [[ -z $1 ]]; then
    echo "Please input repository list. You can get repository from [yum repolist]"
    echo "Rhel7 Usage: reposync.sh \"rhel-7-server-rpms\""
    echo "Rhel7 Usage: reposync.sh \"rhel-8-for-x86_64-baseos-rpms\""
    exit;
fi

for repo in $repolist; do
    if [ ${osversion:0:1} == 7]; then
        reposync --gpgcheck -l -n repoid=$repo --download_path=$repopath
        createrepo $repopath$repo
    elif [ ${osversion:0:1 == 8} ]; then
        reposync --download-metadata --repo=$repo -p $repopath
    fi
done