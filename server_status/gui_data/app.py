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

@app.route('/ss')
def main_gui():
        return render_template("central_gui.html", server_details = ServerStatus.query.all())

@app.route('/ss/server_ip')
def display_server_data(server_ip):
        return server_ip


if __name__ == "__main__":
        db.create_all()
        app.run(host='0.0.0.0')
