import pymysql

def delete_main_gui_data():
        db_con_del = pymysql.connect('vmbox1.centos7', 'root', 'onmobile', 'test_data')
        del_cursor = db_con_del.cursor()
        table_names_list = ['O3_process_stats','disk_space_stats','free_memory_stats','gui_main_data','java_process_stats','load_average_stats','logged_users_stats','mysql_process_stats']
        try:
                for table_name in table_names_list:
                        del_query = "DELETE FROM " + table_name
                        print("Delete query is : %s" %del_query)
                        del_cursor.execute(del_query)
                        db_con_del.commit()
                        print("Main gui data deleted successfully")
        except Exception as de:
                print("Delete data exception is : %s" %de)
                db_con_del.rollback()
        finally:
                db_con_del.close()


if __name__ == "__main__":
        delete_main_gui_data()
