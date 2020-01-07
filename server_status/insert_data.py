#!/usr/bin/python3.6

import pymysql
import os
import time
import datetime

data_headings_file = "/opt/Flask_APP/server_status/data_processing/data_categories.txt"
tmp_file = "/opt/Flask_APP/server_status/data_processing/tmp_file.txt"
table_names_dict = {}
date_default_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ind_cat_a_list = []
ind_cat_b_list = []
server_type_details = ""

def threshold_limits(main_data_file):
        disk_threshold=80
        file_unlink(data_headings_file)
        file_unlink(tmp_file)
        with open(main_data_file, "r") as main_data:                            #Reading the main log file
                for line in main_data:
                        if not "required_" in line:
                                with open(tmp_file, "a") as tmp_strings:                #Writing the log file category headings to file
                                        tmp_category = line.split("#")[0]
                                        tmp_strings.write(tmp_category+"\n")
                                        #print("Data category is: %s" %tmp_category.strip())

                already_available_data = set()
                with open(data_headings_file, "a") as data_main_file:           #Writing unique cateogry headings to file
                        with open(tmp_file, "r") as data_strings_read:
                                for cat in data_strings_read:
                                        if cat not in already_available_data:
                                                data_main_file.write(cat)
                                                already_available_data.add(cat)


def table_heading_dict(main_inpt_file, table_name_cmp):
        #for table_heading_file_name in files_list:
        table_heading_file_name = main_inpt_file
        #print("Table heading file name is : %s" % table_heading_file_name)
        #print("File name is : %s" %table_heading_file_name)
        with open(table_heading_file_name, "r") as heading_file:
                rd_line =heading_file.readline().strip()
                while rd_line:
                        tbl_name = rd_line.split('#')[0]
                        if tbl_name == table_name_cmp:
                                if "#header_" in rd_line:
                                        #print("Header value matched: %s" %rd_line)
                                        #tbl_name = rd_line.split('#')[0]
                                        #if tbl_name == table_name_cmp:
                                        print("Header value matched. Table name matched: %s - %s" %(tbl_name, table_name_cmp))
                                        tbl_fields = rd_line.split('#')[1].replace("header_" ,"")
                                        tbl_field_cnt = len(rd_line.split('---'))
                                        print("Table fields are : %s" % tbl_fields.replace("header_", ""))
                                        table_dict_values = table_heading_names(tbl_name, tbl_fields, tbl_field_cnt)
                        rd_line = heading_file.readline().strip()
        return table_dict_values

def table_heading_names(table_name, table_fields, field_cnt):
        table_names_dict.clear()
        #print("Fields count is : %s" % str(field_cnt))
        table_column_names = table_fields.split("---")
        for i in range(field_cnt):
                #print("String" + str(i) + "=" + str(table_column_names[i]))
                table_names_dict["String" + str(i)] = [str(table_column_names[i])]
        #print("Dictionary values are : %s" % table_names_dict)
        #print("Dictionary keys are : %s" % table_names_dict.keys())
        #print("Dictionary values are : %s" % table_names_dict.values())
        return table_names_dict


def file_lines_count(file_name):
        lines_cnt = 0
        with open(file_name, "r") as file_line_count:
                for cnt in file_line_count:
                        lines_cnt += 1
        return lines_cnt

def file_unlink(unlink_file_name):
        try:
                os.unlink(unlink_file_name)
        except Exception as e:
                print(e)

def date_time_values():
        full_date_with_millies = datetime.datetime.now()
        date_time_minutes = full_date_with_millies.strftime("%Y%m%d%H")
        minute = str(full_date_with_millies.minute)
        minute_len = len(str(minute))
        if (minute_len == 1):
                minute = '0' + minute
        minute = str(minute[:-1]) + '0'
        date_minute = str(date_time_minutes) + str(minute)
        return date_minute

def get_process_list(process_file_name, process_name, process_lines_count):
        process_nm=""
        with open(process_file_name, "r") as process_list:
                for k in range(process_lines_count):
                        process_data = process_list.readline()
                        if "required_" in process_data and not "required_server_type" in process_data:
                                if process_name in process_data:
                                        process_nm = process_data.split('=')[1]
        return process_nm.strip()

def server_indicator_color(cat_a_list, cat_b_list, server_details):
        print("-------------------------")
        cat_a_list = list(set(cat_a_list))
        cat_b_list = list(set(cat_b_list))
        #print("cat a indicator list is : %s" %cat_a_list)
        #print("cat b indicator list is : %s" %cat_b_list)

        if "cat_a_True" in cat_a_list:
                cat_a_list.remove("cat_a_False")
        if "cat_b_True" in cat_b_list:
                cat_b_list.remove("cat_b_False")

        if "cat_a_True" in cat_a_list:
                cat_a_list = list(map(lambda final_list_a: final_list_a.replace('cat_a_True', 'a_red'), cat_a_list))
        else:
                cat_a_list = list(map(lambda final_list_a: final_list_a.replace('cat_a_False', 'c_green'), cat_a_list))

        if "cat_b_True" in cat_b_list:
                cat_b_list = list(map(lambda final_list_b: final_list_b.replace('cat_b_True', 'b_yellow'), cat_b_list))
        else:
                cat_b_list = list(map(lambda final_list_b: final_list_b.replace('cat_b_False', 'c_green'), cat_b_list))
        cat_a_list.sort(key=str)
        cat_b_list.sort(key=str)
        print("cat a list is : %s"%(cat_a_list))
        print("cat b list is : %s"%(cat_b_list))

        list_str_a = str(cat_a_list).replace('[', '')
        list_str_a = str(list_str_a).replace(']', '')
        list_str_b = str(cat_b_list).replace('[', '')
        list_str_b = str(list_str_b).replace(']', '')

        cat_a_identifier = list_str_a.find('a_red')
        cat_b_identifier = list_str_b.find('b_yellow')

        if cat_a_identifier >= 0:
                insert_main_gui_data(list_str_a, server_details)
        elif cat_b_identifier >= 0:
                insert_main_gui_data(list_str_b, server_details)
        else:
                insert_main_gui_data(list_str_b, server_details)          # Passing one of the list because both having green identifier
        print("-------------------------")

def delete_main_gui_data():
        db_con_del = pymysql.connect('vmbox1.centos7', 'root', 'onmobile', 'test_data')
        del_cursor = db_con_del.cursor()
        delete_query = "DELETE FROM gui_main_data"
        try:
                del_cursor.execute(delete_query)
                del_cursor.execute("ALTER TABLE gui_main_data AUTO_INCREMENT = 1")
                db_con_del.commit()
                print("Main gui data deleted successfully and auto increment set to 1")
        except Exception as de:
                print("Delete data exception is : %s" %de)
                db_con_del.rollback()
        finally:
                db_con_del.close()


def insert_main_gui_data(gui_cat_list, server_data):
        db_conn_main = pymysql.connect('vmbox1.centos7', 'root', 'onmobile', 'test_data')
        cursor_main = db_conn_main.cursor()
        main_data_insert_query = "INSERT INTO gui_main_data (server_ip, amber_color, server_type, monitor_time) VALUES (%s, \'%s\', \'%s\')" %(gui_cat_list, server_data, date_default_time)
        print("Main gui insert query is : %s" %main_data_insert_query)
        try:
                cursor_main.execute(main_data_insert_query)
                db_conn_main.commit()
                print("Main table data inserted successfully")
        except Exception as e:
                print("Exception is : ", e)
                db_conn_main.rollback()
        finally:
                db_conn_main.close()

def server_type(data_file):
        with open(data_file, "r") as server_type_data:
                for ln in range(file_lines_count(data_file)):
                        rd_line_data = server_type_data.readline()
                        if "required_server_type=" in rd_line_data:
                                server_type_value = rd_line_data.split("=")[1].strip()
                if not server_type_value:
                        server_type_value = "NA"
        return server_type_value

def process_data(category_name, main_data_file, ip_addr):
        ind_cat_a_list.append(ip_addr)
        ind_cat_b_list.append(ip_addr)
        print("Ctegory table name is : %s" %category_name)
        file_unlink(tmp_file)
        main_data_file_lines_count = file_lines_count(main_data_file)
        with open(main_data_file, "r") as fl_open_1:
                for i in range(main_data_file_lines_count):
                        line_data = fl_open_1.readline()
                        with open(tmp_file, "a") as tmp_fl_wrt:
                                if category_name in line_data:
                                        splt_data = line_data.split("#")[1]
                                        if not "header_" in splt_data:
                                                tmp_fl_wrt.write(splt_data)
                                                print("Test data is : %s" % splt_data.strip())

        tmp_file_lines_cnt = file_lines_count(tmp_file)                         #Getting tmp file lines count by using file_lines_count function
        names_dict = table_heading_dict(main_data_file, category_name)
        disk_cat = memory_cat = load_cat = java_cat = mysql_cat = O3_cat = False
        process_data.server_type_details = server_type(main_data_file)

        def remove_blanks():
                headings_list = list(names_dict.values())
                headings_str = str(headings_list).replace('[', '')
                headings_str_end = headings_str.replace(']', '')
                headings_qts = headings_str_end.replace("'", "")
                return "server_ip, " + headings_qts + ", monitor_time, data_insert_time, indicator_status"

        with open(tmp_file, "r") as tmp_file_read:
                for j in range(tmp_file_lines_cnt):
                        line_data1=tmp_file_read.readline()
                        splt_data1=line_data1.strip().split("---")
                        default_ind_color = "NONE"

                        if category_name == "disk_space_stats":
                        #for table_column_name in range(len(splt_data1)):
                                #print("Column %d is : %s" %(table_column_name, splt_data1[table_column_name]))
                                usage_value = splt_data1[4]
                                usage_value = int(str(usage_value).replace('%', ''))
                                print("Usage is : %s" %usage_value)
                                if usage_value >= 80:
                                        disk_indicator_color = "red"
                                        disk_cat = "cat_b_True"
                                elif usage_value < 80 and usage_value >= 60:            # cat_b = disk space, free memory, load average -- color code = yellow
                                        disk_indicator_color = "yellow"                 # cat_c = No issue      -- color code = green
                                        disk_cat = "cat_b_True"
                                else:
                                        disk_indicator_color = "green"
                                        disk_cat = "cat_b_False"
                                print("Disk cat value is : %s" %disk_cat)
                                ind_cat_b_list.append(disk_cat)
                                #pass

                        elif category_name == "free_memory_stats":
                                used_memory = splt_data1[2]
                                total_memory = splt_data1[1]
                                if total_memory == "NA":
                                        total_memory = int(splt_data1[3]) + int(splt_data1[2])
                                print("Userd memory is : %s" %used_memory)
                                print("Total memory is : %s" %total_memory)
                                memory_percent = (int(used_memory)/int(total_memory)) * 100
                                if memory_percent >= 80:
                                        memory_indicator_color = "red"
                                        memory_cat = "cat_b_True"
                                elif memory_percent < 80 and memory_percent >=60:
                                        memory_indicator_color = "yellow"
                                        memory_cat = "cat_b_True"
                                else:
                                        memory_indicator_color = "green"
                                        memory_cat = "cat_b_False"
                                print("Memory percentage is : %d" %memory_percent)
                                print("Memory indicator color is : %s" %memory_indicator_color)
                                print("memory cat is : %s" %memory_cat)
                                ind_cat_b_list.append(memory_cat)

                        elif category_name == "load_average_stats":
                                one_minute_load = int(float(splt_data1[2]))
                                print("Load type is : %d" %one_minute_load)
                                if one_minute_load >= 10:
                                        load_indicator_color = "red"
                                        load_cat = "cat_b_True"
                                elif one_minute_load < 10 and one_minute_load >= 5:
                                        load_indicator_color = "yellow"
                                        load_cat = "cat_b_True"
                                else:
                                        load_indicator_color = "green"
                                        load_cat = "cat_b_False"
                                print("One minute load is : %d" %one_minute_load)
                                print("Load color is : %s" %load_indicator_color)
                                print("load cat is : %s" %load_cat)
                                ind_cat_b_list.append(load_cat)

                        elif category_name == "java_process_stats":
                                process_addrs = splt_data1[5]
                                process_utilization = splt_data1[3]
                                if process_utilization == "NA":
                                        process_utilziation = 0
                                else:
                                        process_utilization = int(splt_data1[3])

                                if process_addrs == "NO_JAVA_PROCESS_RUNNING":
                                        if get_process_list(main_data_file, "java", main_data_file_lines_count) == "yes":
                                                java_indicator_color = "red"
                                                java_cat = "cat_a_True"
                                        else:
                                                java_indicator_color = "green"
                                                java_cat = "cat_a_False"
                                elif process_utilization >= 50:
                                        java_indicator_color = "red"
                                else:
                                        java_indicator_color = "green"
                                        java_cat = "cat_a_False"

                                print("java cat is : %s" %java_cat)
                                ind_cat_a_list.append(java_cat)

                        elif category_name == "mysql_process_stats":
                                process_addrs = splt_data1[5]
                                process_utilization = int(splt_data1[3])
                                if str(process_utilization) == "NA":
                                        process_utilization = 0
                                else:
                                        process_utilization = int(splt_data1[3])

                                if process_addrs == "NO_MYSQL_PROCESS_RUNNING":
                                        if get_process_list(main_data_file, "mysql", main_data_file_lines_count) == "yes":
                                                mysql_indicator_color = "red"
                                                mysql_cat = "cat_a_True"
                                        else:
                                                mysql_indicator_color = "green"
                                                mysql_cat = "cat_a_False"
                                elif process_utilization >=50:
                                        mysql_indicator_color = "red"
                                else:
                                        mysql_indicator_color = "green"
                                        mysql_cat = "cat_a_False"
                                print("mysql cat is : %s" %mysql_cat)
                                ind_cat_a_list.append(mysql_cat)

                        elif category_name == "O3_process_stats":
                                process_addrs = splt_data1[5]
                                process_utilization = splt_data1[3]
                                if str(process_utilization) == "NA":
                                        process_utilization = 0
                                else:
                                        process_utilization = int(splt_data1[3])

                                if process_addrs == "NO_O3_COMPONENTS_RUNNING":
                                        if get_process_list(main_data_file, "O3", main_data_file_lines_count) == "yes":
                                                o3_indicator_color = "red"
                                                O3_cat = "cat_a_True"
                                        else:
                                                o3_indicator_color = "green"
                                                O3_cat = "cat_a_False"
                                elif process_utilization >= 50:
                                        o3_indicator_color = "red"
                                else:
                                        o3_indicator_color = "green"
                                        O3_cat = "cat_a_False"
                                print("O3 cat is : %s" %O3_cat)
                                ind_cat_a_list.append(O3_cat)

                        headings_file_data = remove_blanks()
                        values_str = str(splt_data1).replace('[', '')
                        values_str_end = values_str.replace(']', '')
                        monitor_time = date_time_values()

                        if category_name == "disk_space_stats":
                                insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, disk_indicator_color)
                        elif category_name == "free_memory_stats":
                                insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, memory_indicator_color)
                        elif category_name == "load_average_stats":
                                insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, load_indicator_color)
                        elif category_name == "java_process_stats":
                                if get_process_list(main_data_file, "java", main_data_file_lines_count) == "yes":
                                        insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, java_indicator_color)
                                else:
                                        print("Java process monitoring is not required")
                        elif category_name == "mysql_process_stats":
                                if get_process_list(main_data_file, "mysql", main_data_file_lines_count) == "yes":
                                        insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, mysql_indicator_color)
                                else:
                                        print("Mysql process monitoring is not required")
                        elif category_name == "O3_process_stats":
                                if get_process_list(main_data_file, "O3", main_data_file_lines_count) == "yes":
                                        insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, o3_indicator_color)
                                else:
                                        print("O3 component monitoring is not required")
                        else:
                                insert_data(category_name, headings_file_data, values_str_end, monitor_time, ip_addr, default_ind_color)
        print("cat b indicator list is : %s" %list(set(ind_cat_b_list)))
        print("cat a indicator list is : %s" %list(set(ind_cat_a_list)))
        print("")

def insert_data(tbl_category_name, tbl_headings_data, tbl_values_data, tbl_monitor_time, tbl_ip_addr, tbl_ind_color):
        db_conn = pymysql.connect('vmbox1.centos7', 'root', 'onmobile', 'test_data')
        cursor = db_conn.cursor()
        #insert_query = "INSERT INTO test_table (id, username, email) VALUES ('%d', '%s', '%s')" %(id, username, email)
        insert_query = "INSERT INTO %s (%s) VALUES (\'%s\', %s,\'%s\',\'%s\', \'%s\')" %(tbl_category_name, tbl_headings_data, tbl_ip_addr, tbl_values_data, tbl_monitor_time, date_default_time, tbl_ind_color)

        print("Insert query is : %s" %insert_query)

        try:
                cursor.execute(insert_query)
                db_conn.commit()
                print("Records inserted successfully")
        except Exception as e:
                print("Exception is : ", e)
                db_conn.rollback()
        finally:
                db_conn.close()


files_list = []
def list_paths(path_name):
        for r, d, f in os.walk(path_name):
                for files in f:
                        if 'server_status.log' in files:
                                files_list.append(os.path.join(r,files))
        print("File names are : %s" % files_list)

list_paths("/opt/Flask_APP/server_status/data_processing/server_status_log_files")

def call_process_data(server_log_file):
        threshold_limits(server_log_file)
        table_names_cnt = file_lines_count(data_headings_file)
        ip_addr_fl_name = server_log_file.split("/")[-1]
        ip_addr = ip_addr_fl_name.split("_")[0]
        print("IP Address file name is : %s" %ip_addr_fl_name)
        print("IP Address is : %s" %ip_addr)
        with open(data_headings_file, "r") as table_names:
                tbl_name = table_names.readlines()
                for l in range(len(tbl_name)):
                        process_data(tbl_name[l].strip(), server_log_file, ip_addr)

if __name__ == "__main__":
        delete_main_gui_data()
        os.system("sh /opt/Flask_APP/server_status/data_processing/server_status_log_files/scp_data.sh")
        for list_file_name in files_list:
                print("File name is : %s" %list_file_name)
                call_process_data(list_file_name)
                server_indicator_color(ind_cat_a_list, ind_cat_b_list, process_data.server_type_details)
                ind_cat_a_list.clear()
                ind_cat_b_list.clear()
