#!/bin/bash

#set -x

server_ip="10.12.3.86"

log_fl="/var/tmp/${server_ip}_server_status.log"
config_file="/root/SCRIPTS/SERVER_STATUS/config_data.txt"
java_list=('RBTGatherer' 'RBTDaemonManager' 'RbtTCPServer' 'voldemort.server.VoldemortServer' 'RBTTomcat')
mysql_list=('/usr/bin/mysqld_safe' '/usr/sbin/mysqld')

if [[ ! -f $log_fl ]]
then
        touch $log_fl
        chmod 777 $log_fl
        echo "$(cat $config_file | grep 'required')" >> $log_fl

else
        cat /dev/null >  $log_fl
        echo "$(cat $config_file | grep 'required')" >> $log_fl
        chmod 777 $log_fl
fi

function disk_space_stats()
{
        disk_drives=($(df -P | grep -v Used | awk '{print $6}'))
        echo "disk_space_stats#header_drive_name---total_size---size_used---available_size---use_percent" >> $log_fl
        for (( i=0; i<${#disk_drives[@]}; i++ ))
        do
                #echo "Disk drive ${disk_drives[$i]} stats:"
                #echo "-------------------------------------"
                #echo "Mounted On: ${disk_drives[$i]}"
                drive_size=$(df -Ph ${disk_drives[$i]} | grep -v Used | awk '{print $2}' | sed '/^\s*$/d')
                drive_used=$(df -Ph ${disk_drives[$i]} | grep -v Used | awk '{print $3}' | sed '/^\s*$/d')
                drive_avail=$(df -Ph ${disk_drives[$i]} | grep -v Used | awk '{print $4}' | sed '/^\s*$/d')
                drive_pcent=$(df -Ph ${disk_drives[$i]} | grep -v Used | awk '{print $5}' | sed '/^\s*$/d')
                #echo "Total size: ${drive_size}"
                #echo "Used size: ${drive_used}"
                #echo "Available size: ${drive_avail}"
                #echo "Percent used: ${drive_pcent}"
                #echo "Drive_name---Total_size---Size_used---Available_size---Use_percentage"
                echo "disk_space_stats#${disk_drives[$i]}---${drive_size}---${drive_used}---${drive_avail}---${drive_pcent}" >> $log_fl
                #echo ""
        done
}

function free_memory_stats()
{
        echo "free_memory_stats#header_memory_type---total_memory---used_memory---free_memory---shared_memory---buffers---cached" >> $log_fl
        memory_stats=$(free -g | awk '/Mem:/ {print ($2==""?"NA":$2)"---"($3==""?"NA":$3)"---"($4==""?"NA":$4)"---"($5==""?"NA":$5)"---"($6==""?"NA":$6)"---"($7==""?"NA":$7)}')
        buffers_stats=$(free -g | awk '/buffers\/cache:/ {print "NA---"($3==""?"NA":$3)"---"($4==""?"NA":$4)"---"($5==""?"NA":$5)"---"($6==""?"NA":$6)"---"($7==""?"NA":$7)}')
        swap_stats=$(free -g | awk '/Swap:/ {print ($2==""?"NA":$2)"---"($3==""?"NA":$3)"---"($4==""?"NA":$4)"---"($5==""?"NA":$5)"---"($6==""?"NA":$6)"---"($7==""?"NA":$7)}')
        echo "free_memory_stats#Memory---${memory_stats}" >> $log_fl
        echo "free_memory_stats#Buffers/Cache---${buffers_stats}" >> $log_fl
        echo "free_memory_stats#Swap---${swap_stats}" >> $log_fl
}

function load_average_stats()
{
        echo "load_average_stats#header_no_of_users---uptime---one_minute_average---five_minute_average---fifteen_minute_average" >> $log_fl
        uptime_stats=$(uptime | grep -ohe 'up .*user*' | awk '{gsub ( "user*","" ); print $0 }' | sed 's/,//g' | sed -r 's/(\S+\s+){1}//' | awk '{$NF=""}1')
        no_of_users_stats=$(uptime | grep -ohe '[0-9.*] user[s,]'| sed 's/,//g')
        load_average_stats=$(uptime | grep -ohe 'load average[s:][: ].*' | sed 's/,//g' | awk '{ print $3"---"$4"---"$5}')
        echo "load_average_stats#${no_of_users_stats}---${uptime_stats}---${load_average_stats}" | sed 's/\ ---/---/g' >> $log_fl
}

function logged_users_stats()
{
        echo "logged_users_stats#header_username---terminal---logged_in_from---login_time---idle_time" >> $log_fl
        logged_user_count=$(w | egrep -v 'load|USER' | wc -l)
        if [[ ${logged_user_count} -ge 1 ]]
        then
                login_user_stats=$(w| egrep -v 'load|USER' | sed 's/^/logged_users_stats#/g' | awk '{if ($2~"tty" || $2~":0") print $1"---"$2"---DIRECT_LOGIN---"$4"---"$5; else print $1"---"$2"---"$3"---"$4"---"$5}')
        else
                login_user_stats="logged_users_stats#NA---NA---NO_USERS_LOGGED_IN---NA---NA"
        fi
        echo "${login_user_stats}" >> $log_fl
}

function java_process_stats()
{
        java_process_cnt=${#java_list[@]}
        echo "Java process list is : ${java_process_cnt}"
        echo "java_process_stats#header_username---process_id---parent_process_id---processor_utilization---start_time---process_address" >> $log_fl
        if [[ $java_process_cnt -ge 1 ]]
        then
                for (( i=0; i<${#java_list[@]}; i++ ))
                do
                        java_process_name=$(/bin/ps -ef | grep java | grep "${java_list[$i]}" | grep -v grep | sed '/^\s*$/d' | awk -vOFS=, '{print $1"---"$2"---"$3"---"$4"---"$5;$1=$2=$3=$4=$5=$6=$7="";print "---"$0}' | sed '/^\s*$/d'|  sed 's/,//g' | tr '\n' '#' | sed 's/#---/---/g' | tr '#' '\n' | sed 's/^/java_process_stats#/g' | egrep -v 'seds|#/g')
                        java_process_data=$(echo $java_process_name | awk -F '---' -v process_nm="${java_list[$i]}" '{print $1"---"$2"---"$3"---"$4"---"$5"---"process_nm}')
                        echo "${java_process_data}" >> $log_fl
                done
        else
                java_process_cnt=0
                echo "java_process_stats#NA---NA---NA---NA---NA---NO_JAVA_PROCESS_RUNNING" >> $log_fl
        fi
}

function mysql_process_stats()
{       mysql_process_cnt=${#mysql_list[@]}
        echo "mysql_process_stats#header_username---process_id---parent_process_id---processor_utilization---start_time---process_address" >> $log_fl
        if [[ $mysql_process_cnt -ge 1 ]]
        then
                for (( j=0; j<${#mysql_list[@]}; j++ ))
                do
                        mysql_cnt=$(ps -ef | grep mysql | grep ${mysql_list[$j]} | grep -v grep | wc -l)
                        if [[ ${mysql_cnt} -ge 1 ]]
                        then
                                mysql_process_stats=$( ps -ef | grep mysql | grep ${mysql_list[$j]} | grep -v grep | awk -vOFS=, '{print $1"---"$2"---"$3"---"$4"---"$5;$1=$2=$3=$4=$5=$6=$7="";print "---"$0}' | sed '/^\s*$/d'|  sed 's/,//g' | tr '\n' '#' | sed 's/#---/---/g' | tr '#' '\n' | sed 's/^/mysql_process_stats#/g' | egrep -v 'seds|#/g')
                                mysql_process_data=$(echo ${mysql_process_stats} | awk -F '---' -v process_nm="${mysql_list[$j]}" '{print $1"---"$2"---"$3"---"$4"---"$5"---"process_nm}')
                        else
                                mysql_process_data="mysql_process_stats#0---0---0---0---0---NO_MYSQL_PROCESS_RUNNING"
                        fi
                        echo "${mysql_process_data}" >> $log_fl
                done
        else
                mysql_process_cnt=0
                echo "mysql_process_stats#NA---NA---NA---NA---NA---NO_MYSQL_PROCESS_RUNNING" >> $log_fl
        fi
}

function ozone_process_stats()
{
        o3_process_cnt=$(ps -ef | grep O3 | grep -v grep | wc -l)
        echo "O3_process_stats#header_username---process_id---parent_process_id---processor_utilization---start_time---process_address" >> $log_fl
        if [[ o3_process_cnt -ge 1 ]]
        then
                O3_process_stats=$(ps -ef | grep O3 | grep -v grep | awk -vOFS=, '{print $1"---"$2"---"$3"---"$4"---"$5;$1=$2=$3=$4=$5=$6=$7="";print "---"$0}' |  sed '/^\s*$/d' |   sed 's/,//g' | tr '\n' '#' | sed 's/#---/---/g' | tr '#' '\n'  | sed 's/^/O3_process_stats#/g' | egrep -v 'seds|#/g')
                echo "${O3_process_stats}" >> $log_fl
        else
                o3_process_cnt=0
                echo "O3_process_stats#NA---NA---NA---NA---NA---NO_O3_COMPONENTS_RUNNING" >> $log_fl
        fi
}

function disk_controler_status()
{
        disk_ctrl_sts=$(hpacucli ctrl all show config | grep -i failed)
}

disk_space_stats
free_memory_stats
load_average_stats
logged_users_stats
java_process_stats
mysql_process_stats
ozone_process_stats
chmod 777 $log_fl
