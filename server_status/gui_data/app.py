from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:onmobile@vmbox1.centos7/test_data'
app.config['SECRET_KEY'] = 'server_status'

db = SQLAlchemy(app)

class ServerStatus(db.Model):
        __tablename__ = "gui_main_data"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        amber_color = db.Column(db.String(10))
        server_type = db.Column(db.String(50))
        monitor_time = db.Column(db.DateTime(timezone=True), default=db.func.now())

        def __init__(self, server_ip, amber_color, server_type, monitor_time):
                self.server_ip = server_ip
                self.amber_color = amber_color
                self.server_type = server_type
                self.monitor_time = monitor_time

class DiskSpaceStats(db.Model):
        __tablename__ = "disk_space_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        drive_name = db.Column(db.String(100))
        total_size = db.Column(db.String(10))
        size_used = db.Column(db.String(10))
        available_size = db.Column(db.String(10))
        use_percent = db.Column(db.String(10))
        monitor_time = db.Column(db.String(15))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, drive_name, total_size, size_used, available_size, use_percent, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.drive_name = drive_name
                self.total_size = total_size
                self.size_used = size_used
                self.available_size = available_size
                self.use_percent = use_percent
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class FreeMemoryStats(db.Model):
        __tablename__ = "free_memory_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        memory_type = db.Column(db.String(40))
        total_memory = db.Column(db.String(5))
        used_memory = db.Column(db.String(5))
        free_memory = db.Column(db.String(5))
        shared_memory = db.Column(db.String(5))
        buffers = db.Column(db.String(5))
        cached = db.Column(db.String(5))
        monitor_time = db.Column(db.String(15))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, memory_type, total_memory, used_memory, free_memory, shared_memory, buffers, cached, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.memory_type = memory_type
                self.total_memory = total_memory
                self.used_memory = used_memory
                self.free_memory = free_memory
                self.shared_memory = shared_memory
                self.buffers = buffers
                self.cached = cached
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class LoadAverageStats(db.Model):
        __tablename__ = "load_average_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        no_of_users = db.Column(db.String(10))
        uptime = db.Column(db.String(150))
        one_minute_average = db.Column(db.String(100))
        five_minute_average = db.Column(db.String(100))
        fifteen_minute_average = db.Column(db.String(100))
        monitor_time = db.Column(db.String(20))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, no_of_users, uptime, one_minute_average, five_minute_average, fifteen_minute_average, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.no_of_users = no_of_users
                self.uptime = uptime
                self.one_minute_average = one_minute_average
                self.five_minute_average = five_minute_average
                self.fifteen_minute_average = fifteen_minute_average
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class LoggedUsersStats(db.Model):
        __tablename__ = "logged_users_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        username = db.Column(db.String(100))
        terminal = db.Column(db.String(100))
        logged_in_from = db.Column(db.String(100))
        login_time = db.Column(db.String(50))
        idle_time = db.Column(db.String(50))
        monitor_time = db.Column(db.String(20))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, username, terminal, logged_in_from, login_time, idle_time, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.username = username
                self.terminal = terminal
                self.logged_in_from = logged_in_from
                self.login_time = login_time
                self.idle_time = idle_time
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class JavaProcessStats(db.Model):
        __tablename__ = "java_process_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        username = db.Column(db.String(100))
        process_id = db.Column(db.String(20))
        parent_process_id = db.Column(db.String(20))
        processor_utilization = db.Column(db.String(40))
        start_time = db.Column(db.String(30))
        process_address = db.Column(db.Text)
        monitor_time = db.Column(db.String(20))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, username, process_id, parent_process_id, processor_utilization, start_time, process_address, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.username = username
                self.process_id = process_id
                self.parent_process_id = parent_process_id
                self.processor_utilization = processor_utilization
                self.start_time = start_time
                self.process_address = process_address
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class MysqlProcessStats(db.Model):
        __tablename__ = "mysql_process_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        username = db.Column(db.String(100))
        process_id = db.Column(db.String(20))
        parent_process_id = db.Column(db.String(20))
        processor_utilization = db.Column(db.String(40))
        start_time = db.Column(db.String(30))
        process_address = db.Column(db.Text)
        monitor_time = db.Column(db.String(20))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, username, process_id, parent_process_id, processor_utilization, start_time, process_address, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.username = username
                self.process_id = process_id
                self.parent_process_id = parent_process_id
                self.processor_utilization = processor_utilization
                self.start_time = start_time
                self.process_address = process_address
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status

class O3ProcessStats(db.Model):
        __tablename__ = "O3_process_stats"
        id = db.Column(db.Integer, primary_key=True)
        server_ip = db.Column(db.String(15))
        username = db.Column(db.String(100))
        process_id = db.Column(db.String(20))
        parent_process_id = db.Column(db.String(20))
        processor_utilization = db.Column(db.String(40))
        start_time = db.Column(db.String(30))
        process_address = db.Column(db.Text)
        monitor_time = db.Column(db.String(20))
        data_insert_time = db.Column(db.DateTime(timezone=True), default=db.func.now())
        indicator_status = db.Column(db.String(20))

        def __init__(self, server_ip, username, process_id, parent_process_id, processor_utilization, start_time, process_address, monitor_time, data_insert_time, indicator_status):
                self.server_ip = server_ip
                self.username = username
                self.process_id = process_id
                self.parent_process_id = parent_process_id
                self.processor_utilization = processor_utilization
                self.start_time = start_time
                self.process_address = process_address
                self.monitor_time = monitor_time
                self.data_insert_time = data_insert_time
                self.indicator_status = indicator_status


@app.route('/ss')
def main_gui():
        return render_template("central_gui.html", server_details = ServerStatus.query.all())

@app.route('/ss/<ip>')
def display_server_data(ip):
        disk_space = DiskSpaceStats.query.filter_by(server_ip=ip).all()
        return render_template("server_details.html", disk_space = disk_space, title_ip = ip)


if __name__ == "__main__":
        db.create_all()
        app.run(host='0.0.0.0')
