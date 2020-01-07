#!/bin/bash

#set -x

files_path="/opt/Flask_APP/server_status/data_processing/server_status_log_files/"
server_ip_list=("10.12.4.10")

for (( i=0; i<${#server_ip_list[@]}; i++ ))
do
        `scp omadmin@${server_ip_list[$i]}:/var/tmp/${server_ip_list[$i]}_server_status.log ${files_path}`
done
